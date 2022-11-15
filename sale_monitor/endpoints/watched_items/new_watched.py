from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers
from sale_monitor.endpoints.utils import build_resp
from sale_monitor.utils.quantize import quantize

import json

from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('new_watched', __name__)


@bp.route('/new_watched', methods=('POST', 'OPTIONS'))
def new_watched():
    """ Adds a new watched product to the db.
        Expects:
        {
          'product_description': <>,
         'product_upc': <>,
         'normal_price': <>,
         'promo_price': <>,
         'target_price': <>,
         'image_url': <>
        }

        Returns the above  plus
            'id' (primary key of watched_products entry)
            'date_last_checked': String MM/DD the pricing was last checked for the product.
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    # Truncating incoming price values.
    # str because float removes trailing zeroes.
    normal_price: str = str(quantize(request.json['normal_price']))
    promo_price: str = str(quantize(request.json['promo_price']))
    target_price: str = str(quantize(request.json['target_price']))
    print(f'The target price: {target_price}')

    ret = DBInterface.new_watched(session.get('email'),
                                  request.json['product_upc'],
                                  request.json['product_description'],
                                  request.json['image_url'],
                                  normal_price,
                                  promo_price,
                                  target_price)

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
        return build_resp(product_dict, 200)
