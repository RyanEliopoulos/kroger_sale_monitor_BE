from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('new_watched', __name__)


@bp.route('/new_watched', methods=('POST', 'OPTIONS'))
def new_watched():
    """ Adds a new watched product to the db.
        Returns the primary key of the watched_products entry as
        {'new_watched_id': <id>}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    payload: dict = request.json['payload']
    ret = DBInterface.new_watched(session.get('contact_id'),
                                  payload['upc'],
                                  payload['target_price'])
    if ret[0]:
        print(f'Error in new_watched endpoint: {ret}')
        resp = Response(response=json.dumps(ret[1]))
        resp.status_code = 500
        add_cors_headers(resp)
        return resp
    else:
        # Returns the 'id' primary key value of the watched_products primary key
        print('Success in new_watched endpoint')
        resp = Response(response=json.dumps(ret[1]))
        resp.status_code = 200
        add_cors_headers(resp)
