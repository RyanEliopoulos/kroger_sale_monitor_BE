from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('set_email', __name__)


@bp.route('/set_email', methods=('POST', 'OPTIONS'))
def set_email():
    """ Updates contact email """
    if request.method == 'OPTIONS':
        print('in set_email preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    print('In set_email endpint.')
    print(request.json['email'])
    new_email: str = request.json['email']
    print(f'session email is {session.get("email")}')
    ret = DBInterface.set_email(session.get('email'), new_email)
    if ret[0]:
        print(f'Error in set_email endpoint: {ret}')
        resp = Response(response=json.dumps(ret[1]))
        resp.status_code = 500
        add_cors_headers(resp)
        return resp
    session['email'] = new_email
    print('Success in set_email endpoint')
    return {}, 200