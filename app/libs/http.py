from flask import Response
import jsonpickle
from app.libs.errorhandler import compose_error
from app.consts.errors import ERROR_MAP


def jsonify(raw=None, status_code=200):
    resp = Response(jsonpickle.encode(raw), mimetype='application/json')
    resp.status_code = status_code
    return resp


def error_jsonify(error_code, specifiy_error="", status_code=400):
    error_resp = compose_error(specifiy_error if specifiy_error else ERROR_MAP[error_code], error_code)
    return jsonify(error_resp, status_code)
