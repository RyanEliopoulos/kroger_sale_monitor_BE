from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers, build_resp

from sale_monitor.kroger.Communicator import Communicator

import json
import math
from flask import (
    Blueprint, request, session, jsonify, Response
)

from typing import Union

bp = Blueprint('search_products', __name__)


@bp.route('/search_products', methods=('GET', 'OPTIONS'))
def search_products():
    """
        Expects either query parameters of the following
        IF initial_query
            {'search_term': <>, 'initial_query': true, 'page_size': <>}
        ELSE
            {'search_term': <>, 'initial_query': false, 'page_size', 'page': <>}

        If initial_query this endpoint will calculate the # of pages needed to fulfill the request
        Ideally the page info calculated every call to compensate for any changes happening on Krogers
        end but I don't feel like being that thorough.

        We need to make sure that a locationId exists.

        Returns:
            IF initial_query:
                {'pages': <>, 'data': <Kroger API data>}
            ELSE
                {'data': <Kroger API data>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp

    location_id: str = session.get('location_id', None)
    if location_id is None:
        print('Error in search_products endpoint: session has no location id')
        return {'error': 'Must select a location first'}, 403

    # It is a GET so no body allowed I guess. Query string only.
    search_term: str = request.args.get('search_term')
    page_size: int = int(request.args.get('page_size'))
    page: Union[str, None] = request.args.get('page')
    is_init_query: Union[bool, None] = request.args.get('initial_query')

    if is_init_query:
        print('In search_products endpoint with initial query to Kroger')
        # Need to calculate pagination details for client
        ret = Communicator.search_products(search_term,
                                           session.get('location_id'),
                                           page_size,
                                           1)
        if ret[0]:
            print(f'Probelm in search_products endpoint: {ret}')
            return ret[1], 500
        print('Success in search_products endpoint. Here are the \'meta\' fields')
        # Calculating pagination details.
        meta: Union[dict, None] = ret[1].get('meta', None)
        if meta is None:  # Search had zero matches
            print('In search_products endpoint. No results from Kroger')
            return {'pages': 0, 'data': []}, 200

        #@TODO remove this. Just for reference
        from sale_monitor.utils.image_sizes import image_sizing
        image_sizing(ret[1]['data'])
        print(ret[1]['meta'])
        total: int = int(ret[1]['meta']['pagination']['total'])
        pages: int = math.ceil(total / page_size)
        data: dict = ret[1]['data']
        return {'pages': pages, 'data': data}, 200
    else:
        # Client provides the pagination details
        print('In search_products endpoint, not initial query to kroger.')
        ret = Communicator.search_products(search_term,
                                           session.get('location_id'),
                                           page_size,
                                           int(page))
        if ret[0]:
            print(f'Error in search_products endpoint: {ret}')
            return ret[1], 500
        print('Success in search_products endpoint')
        return ret[1]['data'], 200



