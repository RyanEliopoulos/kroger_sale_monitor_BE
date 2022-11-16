import json

from flask import (
     Response
)


def add_cors_headers(resp: Response) -> Response:
    # Preflighting
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type"
    return resp


def build_resp(response, status_code) -> Response:
    resp = Response(response=json.dumps(response))
    resp.status_code = status_code
    add_cors_headers(resp)
    return resp





