from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None, **kwargs):
    payload = dict(
        error=HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
        status='fail',
        **kwargs
    )
    payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message=None, **kwargs):
    return error_response(400, message, **kwargs)


def unauthorized(message=None, **kwargs):
    return error_response(401, message, **kwargs)


def forbidden(message=None, **kwargs):
    return error_response(403, message, **kwargs)


def not_found(message=None, **kwargs):
    return error_response(404, message, **kwargs)
