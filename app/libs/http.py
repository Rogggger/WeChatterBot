from flask import Response
import jsonpickle
from app.libs.errorhandler import compose_error
from app.consts.errors import ERROR_MAP


jsonpickle.load_backend('json', 'dumps', 'loads', ValueError)
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)


def jsonify(raw=None, status_code=200):
    resp = Response(jsonpickle.encode(raw), mimetype='application/json')
    resp.status_code = status_code
    return resp


def error_jsonify(error_code, specifiy_error="", status_code=400):
    error_resp = compose_error(specifiy_error if specifiy_error else ERROR_MAP[error_code], error_code)
    return jsonify(error_resp, status_code)


def jsonify_cors(raw=None, status_code=200):
    res = jsonify(raw, status_code)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    res.headers['Content-Type'] = 'text/plain;charset=UTF-8'
    return res


def error_jsonify_cors(error_code, specifiy_error="", status_code=400):
    error_resp = compose_error(specifiy_error if specifiy_error else ERROR_MAP[error_code], error_code)
    return jsonify_cors(error_resp, status_code)
