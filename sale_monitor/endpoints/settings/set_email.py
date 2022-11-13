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
    new_email: str = request.json.get('email')
    #@TODO make sure this works. Add a guard to catch API calls missing the contact_id
    # (above unnecessary since schema.sql is inserting the one and only entry, so one will always be present.
    ret = DBInterface.set_email(session.get('contact_id'), new_email)
    if ret[0]:
        print(f'Error in set_email endpoint: {ret}')
        resp = Response(response=json.dumps(ret[1]))
        resp.status_code = 500
        add_cors_headers(resp)
        return resp
    print('Success in set_email endpoint')
    return {}, 200