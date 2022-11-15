from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers, build_resp

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('delete_watched', __name__)


@bp.route('/delete_watched', methods=('POST', 'OPTIONS'))
def delete_watched():
    """
        Expects {'watched_product_id': <>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    ret = DBInterface.delete_watched(request.json['watched_product_id'])
    if ret[0]:
        print(f'problem in delete_watched endpoint: {ret}')
        return build_resp(ret[1], 500)
    else:
        print('Success in delete_watched endpoint')
        return {}, 200