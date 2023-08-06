import json
import traceback
from urllib.parse import urljoin, urlparse

import sqlalchemy
from flask import Response, abort, current_app, jsonify, request
from link_header import Link, LinkHeader
from slugify import slugify
from sqlalchemy.orm.exc import NoResultFound
from webargs.flaskparser import use_kwargs

from flask_taxonomies.constants import (
    INCLUDE_DELETED,
    INCLUDE_DESCENDANTS,
    INCLUDE_DESCENDANTS_COUNT,
    INCLUDE_SELF,
    INCLUDE_STATUS,
)
from flask_taxonomies.marshmallow import (
    HeaderSchema,
    MoveHeaderSchema,
    PaginatedQuerySchema,
)
from flask_taxonomies.models import TaxonomyTerm, TaxonomyTermBusyError, TermStatusEnum
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.routing import accept_fallback
from flask_taxonomies.term_identification import TermIdentification

from .common import blueprint, build_descendants, json_abort, with_prefer
from .paginator import Paginator


@blueprint.route('/<code>/<path:slug>', strict_slashes=False)
@use_kwargs(HeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def get_taxonomy_term(code=None, slug=None, prefer=None, page=None, size=None, status_code=200,
                      q=None):
    try:
        taxonomy = current_flask_taxonomies.get_taxonomy(code)
        prefer = taxonomy.merge_select(prefer)

        current_flask_taxonomies.permissions.taxonomy_term_read.enforce(request=request,
                                                                        taxonomy=taxonomy,
                                                                        slug=slug)

        if INCLUDE_DELETED in prefer:
            status_cond = sqlalchemy.sql.true()
        else:
            status_cond = TaxonomyTerm.status == TermStatusEnum.alive

        return_descendants = INCLUDE_DESCENDANTS in prefer

        if return_descendants:
            query = current_flask_taxonomies.descendants_or_self(
                TermIdentification(taxonomy=code, slug=slug),
                levels=prefer.options.get('levels', None),
                status_cond=status_cond,
                return_descendants_count=INCLUDE_DESCENDANTS_COUNT in prefer,
                return_descendants_busy_count=INCLUDE_STATUS in prefer
            )
        else:
            query = current_flask_taxonomies.filter_term(
                TermIdentification(taxonomy=code, slug=slug),
                status_cond=status_cond,
                return_descendants_count=INCLUDE_DESCENDANTS_COUNT in prefer,
                return_descendants_busy_count=INCLUDE_STATUS in prefer
            )
        if q:
            query = current_flask_taxonomies.apply_term_query(query, q, code)
        paginator = Paginator(
            prefer,
            query, page if return_descendants else None,
            size if return_descendants else None,
            json_converter=lambda data:
            build_descendants(data, prefer, root_slug=None),
            allow_empty=INCLUDE_SELF not in prefer, single_result=INCLUDE_SELF in prefer,
            has_query=q is not None
        )

        return paginator.jsonify(status_code=status_code)

    except NoResultFound:
        term = current_flask_taxonomies.filter_term(
            TermIdentification(taxonomy=code, slug=slug),
            status_cond=sqlalchemy.sql.true()
        ).one_or_none()
        if not term:
            json_abort(404, {
                "message": "%s was not found on the server" % request.url,
                "reason": "does-not-exist"
            })
        elif term.obsoleted_by_id:
            obsoleted_by = term.obsoleted_by
            obsoleted_by_links = obsoleted_by.links()
            return Response(json.dumps({
                'links': term.links(representation=prefer).envelope,
                'status': 'moved'
            }), status=301, headers={
                'Location': obsoleted_by_links.headers['self'],
                'Link': str(LinkHeader([Link(v, rel=k) for k, v in
                                        term.links(representation=prefer).envelope.items()]))
            }, content_type='application/json')
        else:
            json_abort(410, {
                "message": "%s was not found on the server" % request.url,
                "reason": "deleted"
            })
    except:
        traceback.print_exc()
        raise


@blueprint.route('/<code>/<path:slug>', methods=['PUT'], strict_slashes=False)
@use_kwargs(HeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def create_update_taxonomy_term(code=None, slug=None, prefer=None, page=None, size=None, q=None):
    if q:
        json_abort(422, {
            'message': 'Query not appropriate when creating or updating term',
            'reason': 'search-query-not-allowed'
        })
    if_none_match = request.headers.get('If-None-Match', None) == '*'
    if_match = request.headers.get('If-Match', None) == '*'
    return _create_update_taxonomy_term_internal(code, slug, prefer, page, size,
                                                 request.json,
                                                 if_none_match=if_none_match,
                                                 if_match=if_match)


def _create_update_taxonomy_term_internal(code, slug, prefer, page, size, extra_data,
                                          if_none_match=False, if_match=False):
    try:
        taxonomy = current_flask_taxonomies.get_taxonomy(code)
        prefer = taxonomy.merge_select(prefer)

        if INCLUDE_DELETED in prefer:
            status_cond = sqlalchemy.sql.true()
        else:
            status_cond = TaxonomyTerm.status == TermStatusEnum.alive

        slug = '/'.join(slugify(x) for x in slug.split('/'))

        ti = TermIdentification(taxonomy=code, slug=slug)
        term = original_term = current_flask_taxonomies.filter_term(ti,
                                                                    status_cond=sqlalchemy.sql.true()).one_or_none()

        if term and INCLUDE_DELETED not in prefer:
            if term.status != TermStatusEnum.alive:
                term = None

        if if_none_match and term:
            json_abort(412, {
                'message': 'The taxonomy already contains a term on this slug. ' +
                           'As If-None-Match: \'*\' has been requested, not modifying the term',
                'reason': 'term-exists'
            })

        if if_match and not term:
            json_abort(412, {
                'message': 'The taxonomy does not contain a term on this slug. ' +
                           'As If-Match: \'*\' has been requested, not creating a new term',
                'reason': 'term-does-not-exist'
            })

        if term:
            current_flask_taxonomies.permissions.taxonomy_term_update.enforce(request=request,
                                                                              taxonomy=taxonomy,
                                                                              term=term)
            current_flask_taxonomies.update_term(
                term,
                status_cond=status_cond,
                extra_data=extra_data
            )
            status_code = 200
        else:
            if original_term:
                # there is a deleted term, so return a 409 Conflict
                json_abort(409, {
                    'message': 'The taxonomy already contains a deleted term on this slug. '
                               'To reuse the term, repeat the operation with `del` in '
                               'representation:include.',
                    'reason': 'deleted-term-exists'
                })

            current_flask_taxonomies.permissions.taxonomy_term_create.enforce(request=request,
                                                                              taxonomy=taxonomy,
                                                                              slug=slug)
            current_flask_taxonomies.create_term(
                ti,
                extra_data=extra_data
            )
            status_code = 201

        current_flask_taxonomies.commit()

        return get_taxonomy_term(code=code, slug=slug, prefer=prefer, page=page, size=size,
                                 status_code=status_code)

    except NoResultFound:
        json_abort(404, {})
    except:
        traceback.print_exc()
        raise


@blueprint.route('/<code>/<path:slug>', methods=['POST'], strict_slashes=False)
@accept_fallback('content_type')
@use_kwargs(MoveHeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def create_taxonomy_term_post(code=None, slug=None, prefer=None, page=None, size=None, q=None):
    if q:
        json_abort(422, {
            'message': 'Query not appropriate when creating or updating term',
            'reason': 'search-query-not-allowed'
        })
    if_none_match = request.headers.get('If-None-Match', None) == '*'
    if_match = request.headers.get('If-Match', None) == '*'
    extra_data = {**request.json}
    if 'slug' not in extra_data:
        return Response('slug missing in payload', status=400)
    _slug = extra_data.pop('slug')
    return _create_update_taxonomy_term_internal(code, slug + '/' + _slug, prefer, page, size,
                                                 extra_data, if_none_match=if_none_match,
                                                 if_match=if_match)


@blueprint.route('/<code>', methods=['POST'], strict_slashes=False)
@use_kwargs(HeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def create_taxonomy_term_post_on_root(code=None, slug=None, prefer=None, page=None, size=None,
                                      q=None):
    if q:
        json_abort(422, {
            'message': 'Query not appropriate when creating or updating term',
            'reason': 'search-query-not-allowed'
        })
    extra_data = {**request.json}
    if 'slug' not in extra_data:
        return Response('slug missing in payload', status=400)
    _slug = extra_data.pop('slug')
    return _create_update_taxonomy_term_internal(code, urljoin(slug, _slug), prefer, page, size,
                                                 extra_data)


@blueprint.route('/<code>/<path:slug>', methods=['PATCH'], strict_slashes=False)
@use_kwargs(HeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def patch_taxonomy_term(code=None, slug=None, prefer=None, page=None, size=None, q=None):
    if q:
        json_abort(422, {
            'message': 'Query not appropriate when creating or updating term',
            'reason': 'search-query-not-allowed'
        })
    taxonomy = current_flask_taxonomies.get_taxonomy(code, fail=False)
    if not taxonomy:
        json_abort(404, {})
    prefer = taxonomy.merge_select(prefer)

    if INCLUDE_DELETED in prefer:
        status_cond = sqlalchemy.sql.true()
    else:
        status_cond = TaxonomyTerm.status == TermStatusEnum.alive

    ti = TermIdentification(taxonomy=code, slug=slug)
    term = current_flask_taxonomies.filter_term(ti, status_cond=status_cond).one_or_none()

    if not term:
        abort(404)

    current_flask_taxonomies.permissions.taxonomy_term_update.enforce(request=request,
                                                                      taxonomy=taxonomy, term=term)

    current_flask_taxonomies.update_term(
        term,
        status_cond=status_cond,
        extra_data=request.json,
        patch=True,
        status=TermStatusEnum.alive  # make it alive if it  was deleted
    )
    current_flask_taxonomies.commit()

    return get_taxonomy_term(code=code, slug=slug, prefer=prefer, page=page, size=size)


@blueprint.route('/<code>/<path:slug>', methods=['DELETE'], strict_slashes=False)
@use_kwargs(HeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def delete_taxonomy_term(code=None, slug=None, prefer=None, page=None, size=None, q=None):
    if q:
        json_abort(422, {
            'message': 'Query not appropriate when deleting term',
            'reason': 'search-query-not-allowed'
        })
    try:
        taxonomy = current_flask_taxonomies.get_taxonomy(code)
        ti = TermIdentification(taxonomy=code, slug=slug)
        term = current_flask_taxonomies.filter_term(ti).one()

        current_flask_taxonomies.permissions.taxonomy_term_delete.enforce(request=request,
                                                                          taxonomy=taxonomy,
                                                                          term=term)
        term = current_flask_taxonomies.delete_term(TermIdentification(taxonomy=code, slug=slug),
                                                    remove_after_delete=False)
        current_flask_taxonomies.commit()

    except TaxonomyTermBusyError as e:
        return json_abort(412, {
            'message': str(e),
            'reason': 'term-busy'
        })
    except NoResultFound as e:
        return json_abort(404, {})
    return jsonify(term.json(representation=prefer))


@create_taxonomy_term_post.support('application/vnd.move')
@use_kwargs(MoveHeaderSchema, locations=("headers",))
@use_kwargs(PaginatedQuerySchema, locations=("query",))
@with_prefer
def taxonomy_move_term(code=None, slug=None, prefer=None, page=None, size=None, destination='',
                       rename='', q=None):
    """Move term into a new parent or rename it."""
    if q:
        json_abort(422, {
            'message': 'Query not appropriate when moving term',
            'reason': 'search-query-not-allowed'
        })

    try:
        taxonomy = current_flask_taxonomies.get_taxonomy(code)
        ti = TermIdentification(taxonomy=taxonomy, slug=slug)
        term = current_flask_taxonomies.filter_term(ti).one()

        current_flask_taxonomies.permissions.taxonomy_term_move.enforce(
            request=request, taxonomy=taxonomy, term=term,
            destination=destination, rename=rename)
    except NoResultFound as e:
        return json_abort(404, {})

    if destination:
        if destination.startswith('http'):
            destination_path = urlparse(destination).path
            url_prefix = current_app.config['FLASK_TAXONOMIES_URL_PREFIX']
            if not destination_path.startswith(url_prefix):
                abort(400,
                      'Destination not part of this server as it '
                      'does not start with config.FLASK_TAXONOMIES_URL_PREFIX')
            destination_path = destination_path[len(url_prefix):]
            destination_path = destination_path.split('/', maxsplit=1)
            if len(destination_path) > 1:
                destination_taxonomy, destination_slug = destination_path
            else:
                destination_taxonomy = destination_path[0]
                destination_slug = None
        else:
            destination_taxonomy = code
            destination_slug = destination
            if destination_slug.startswith('/'):
                destination_slug = destination_slug[1:]
        if not current_flask_taxonomies.filter_term(
                TermIdentification(taxonomy=code, slug=slug)).count():
            abort(404, 'Term %s/%s does not exist' % (code, slug))

        try:
            old_term, new_term = current_flask_taxonomies.move_term(
                TermIdentification(taxonomy=code, slug=slug),
                new_parent=TermIdentification(taxonomy=destination_taxonomy,
                                              slug=destination_slug) if destination_slug else '',
                remove_after_delete=False)  # do not remove the original node from the database,
            # just mark it as deleted
        except TaxonomyTermBusyError as e:
            return json_abort(412, {
                'message': str(e),
                'reason': 'term-busy'
            })
    elif rename:
        new_slug = slug
        if new_slug.endswith('/'):
            new_slug = new_slug[:-1]
        if '/' in new_slug:
            new_slug = new_slug.rsplit('/')[0]
            new_slug = new_slug + '/' + rename
        else:
            new_slug = rename
        try:
            old_term, new_term = current_flask_taxonomies.rename_term(
                TermIdentification(taxonomy=code, slug=slug),
                new_slug=new_slug,
                remove_after_delete=False)  # do not remove the original node from the database, just mark it as deleted
        except TaxonomyTermBusyError as e:
            return json_abort(412, {
                'message': str(e),
                'reason': 'term-busy'
            })
        destination_taxonomy = code
    else:
        abort(400, 'Pass either `destination` or `rename` parameters ')
        return  # just to make pycharm happy

    current_flask_taxonomies.commit()

    return get_taxonomy_term(code=destination_taxonomy, slug=new_term.slug,
                             prefer=prefer, page=page, size=size)
