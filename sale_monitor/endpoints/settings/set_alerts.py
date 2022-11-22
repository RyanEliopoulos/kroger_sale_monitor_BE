from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers, build_resp

from sale_monitor.kroger.Communicator import Communicator

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('set_alerts', __name__)


@bp.route('/set_alerts', methods=('POST', 'OPTIONS'))
def set_alerts():
    """
        {'receive_alerts': '<bool>'}
    """
    if request.method == 'OPTIONS':
        print('in new_watched preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    receive_alerts: str = request.json['receive_alerts']
    print(f'Value of receive_alerts: {receive_alerts}')
    ret = DBInterface.set_receive_alerts(session.get('email'), receive_alerts)
    if ret[0]:
        return build_resp(ret[1], 500)
    return {}, 200
