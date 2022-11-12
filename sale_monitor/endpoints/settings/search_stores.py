from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers, build_resp

from sale_monitor.kroger.Communicator import Communicator

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('search_stores', __name__)


@bp.route('/search_stores', methods=('POST', 'OPTIONS'))
def search_stores():
    """
        Expects {'zipcode': <>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    payload: dict = request.json['payload']
    zipcode: str = payload['zipcode']
    print(f'Searching locations with zipcode: {zipcode}')
    ret = Communicator.search_locations(zipcode)
    if ret[0]:
        print(f'Problem in search_stores endpoint: {ret}')
        return build_resp(ret[1], status_code=500)
    print(f'Success in search_stores')
    return ret[1], 200
