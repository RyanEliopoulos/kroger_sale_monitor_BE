from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers, build_resp

from sale_monitor.kroger.Communicator import Communicator

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('search_products', __name__)


@bp.route('/search_products', methods=('POST', 'OPTIONS'))
def search_products():
    """
        Expects {'search_term': <>, page: <>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    search_term = request.json['payload']['search_term']
    page = request.json['payload']['page']
    if len(search_term) < 3:
        print(f'Problem in search_products endpoint: search term too short: {search_term}')
        return build_resp({'error': 'search term too short'}, 400)
    ret = Communicator.search_products(search_term,
                                       session.get('location_id'),
                                       page)
    if ret[0]:
        print(f'Error in search_products endpoint: {ret}')
        return build_resp(ret[1], 500)
    print('Success in search search_products endpoint')
    return ret[1], 200