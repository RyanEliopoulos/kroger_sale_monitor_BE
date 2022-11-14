from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers
from sale_monitor.endpoints.utils import build_resp

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('new_watched', __name__)


@bp.route('/new_watched', methods=('POST', 'OPTIONS'))
def new_watched():
    """ Adds a new watched product to the db.
        Returns a complete product object
        {'id': <id>,
         'product_upc': <>,
         'target_price': <>,
         'last_discount_rate: <>
        }
        Expecting: {'product_upc': <>, 'target_price': <>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    ret = DBInterface.new_watched(session.get('contact_id'),
                                  request.json['product_upc'],
                                  request.json['target_price'])
    if ret[0]:
        print(f'Error in new_watched endpoint: {ret}')
        resp = Response(response=json.dumps(ret[1]))
        resp.status_code = 500
        add_cors_headers(resp)
        return resp
    else:
        # Returns the 'id' primary key value of the watched_products primary key
        print('Success in new_watched endpoint')
        product_id: str = ret[1]['new_watched_id']
        ret = DBInterface.get_product(product_id)
        if ret[0]:
            print(f'Error pulling the new product details: {ret}')
            return build_resp(ret[1], 500)
        product_dict: dict = ret[1]
        product_dict['id'] = product_id
        return build_resp(product_dict, 200)
