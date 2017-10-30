from . import api
from flask import jsonify


@api.errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(404)
def notfound(message):
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response


@api.errorhandler(500)
def internaleror(message):
    response = jsonify({'error': 'internal server error', 'message': message})
    response.status_code = 500
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response
