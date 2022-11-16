from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers
from sale_monitor.endpoints.utils import build_resp
from sale_monitor.utils.quantize import quantize

import json

from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('has_session', __name__)


@bp.route('/has_session', methods=('GET', 'OPTIONS'))
def has_session():
    """ """
    print('in has_session')
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    currently_has_session = session.get('email') is not None
    return_dict = {}
    if currently_has_session:
        email = session.get('email')
        ret = DBInterface.get_all(email)
        if ret[0]:
            return build_resp(ret[1], 500)
        return_dict = ret[1]
    return_dict['has_session'] = currently_has_session
    print(f'has session: {currently_has_session}')
    print(f'return dict: {return_dict}')
    return build_resp(return_dict, 200)
