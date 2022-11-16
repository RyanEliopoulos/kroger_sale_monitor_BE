from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers
from sale_monitor.endpoints.utils import build_resp

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('start_session', __name__)


@bp.route('/start_session', methods=('GET', 'OPTIONS'))
def start_session():
    """
        Basically the 'log in' endpoint. Returns all of the data for the given
        email address. Creates the account if it doesn't already exist.
    """
    print('In start_session')
    if request.method == 'OPTIONS':
        print('in get_all preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    email: str = request.args.get('email')
    ret = DBInterface.get_all(email)
    if ret[0]:
        return build_resp(ret[1], 500)
    if ret[1]['data'] is None:
        # Account does not exist.
        print(f'Account does not exist')
        ret = DBInterface.add_account(email)
        if ret[0]:
            print(f'Error creating new account: {ret}')
            return build_resp(ret[1], 500)
        ret = DBInterface.get_all(email)
        if ret[0]:
            return build_resp(ret[1], 500)
    # Email is tied to an account
    data_dict = ret[1]['data']
    session['location_id'] = data_dict['location_id']
    session['email'] = data_dict['email']
    return build_resp(ret[1]['data'], 200)
