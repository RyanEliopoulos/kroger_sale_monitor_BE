from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers, build_resp
from sale_monitor.utils.quantize import quantize

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('updated_watched', __name__)


@bp.route('/update_watched', methods=('POST', 'OPTIONS'))
def update_watched():
    """
        Expects {'targetPrice': <>, 'watched_product_id': <>}

        Returns: {'target_price': <truncated_target_price>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    target_price: str = str(quantize(request.json['target_price']))
    ret = DBInterface.update_watched(request.json['watched_product_id'],
                                     target_price)
    if ret[0]:
        print(f'Error in update_watched endpoint: {ret}')
        return build_resp(ret[1], 500)
    print('Success in update_watched endpoint')
    resp = build_resp({'target_price': target_price}, 200)
    return resp
