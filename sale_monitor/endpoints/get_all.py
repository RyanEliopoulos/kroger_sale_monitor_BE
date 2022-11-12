from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('get_all', __name__)


@bp.route('/get_all', methods=('GET', 'OPTIONS'))
def get_all():
    """ Returns {'data': <data>}, which may be None if initial contact info is not present.
        Upon failure returns {'error': <error}
    """
    if request.method == 'OPTIONS':
        print('in get_all preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    # Retrieving data
    ret = DBInterface.get_all()
    if ret is None:
        # Missing contact information. Yet to perform initial setup
        resp = Response(response=json.dumps({'data': None}))
        resp.status_code = 200
        add_cors_headers(resp)
        return resp
    elif ret[1]:
        # Error
        print(f'get_all endpoint got error from db: {ret}')
        resp = Response(response=json.dumps({'error': ret[1]['error']}))
        resp.status_code = 500
        add_cors_headers(resp)
        return resp
    else:
        # Successfully pulled the information from the database
        # Sending data to client and updating session cookie
        data_dict: dict = ret[1]['data']
        print(f'Successfully pulled data for get_all endpoint: {data_dict}')
        session['contact_id'] = data_dict['contact_id']
        session['location_id'] = data_dict['location_id']
        resp = Response(response=json.dumps({'data': data_dict}))
        resp.status_code = 200
        add_cors_headers(resp)
        return resp
