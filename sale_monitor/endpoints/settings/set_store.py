from sale_monitor.database.db import DBInterface
from sale_monitor.endpoints.utils import add_cors_headers

import json
from flask import (
    Blueprint, request, session, jsonify, Response
)

bp = Blueprint('set_store', __name__)


@bp.route('/set_store', methods=('GET', 'OPTIONS'))
def set_store():
    """ Expects: {'location_id': <>, 'chain': <>, 'address1': <>,
                    'city': <>, 'state': <>, 'zipcode': <>}
    """

    if request.method == 'OPTIONS':
        print('in set_store preflight')
        # Preflighting
        resp = Response()
        add_cors_headers(resp)
        return resp
    payload: dict = request.json['payload']
    #@TODO Add some sort of guard clause here for contact_id
    # Made that unnecessary by inserting an intial entry in schema.sql?
    ret = DBInterface.set_store(session.get('contact_id'),
                                payload['location_id'],
                                payload['chain'],
                                payload['address1'],
                                payload['city'],
                                payload['state'],
                                payload['zipcode'])
    if ret[1]:
        print(f'Error in set_store endpoint: {ret}')
        resp = Response(response=json.dumps(ret[1]))
        resp.status_code = 500
        add_cors_headers(resp)
        return resp
    else:
        print('Success in set_store endpoint')
        return 200, {}
