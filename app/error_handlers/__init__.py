import logging as logger

from flask import Blueprint, jsonify

from app.auth.handlers import auth
from app.entities.basic_error import BasicError

from app.entities.basic_schema import BasicSchema, BasicResponseSchema

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def error_handler(error):
    basic_error = error if isinstance(error, BasicError) \
        else BasicError(message='Internal Server Error')
    basic_response = BasicSchema(error=basic_error)
    response = jsonify(BasicResponseSchema().dump(basic_response))
    response.status_code = basic_error.status

    logger.warning(f'Error was occurred: {error}')

    return response


@auth.error_handler
def auth_error(status):
    message = 'Unauthorized Access' if status == 401 else 'Forbidden'
    basic_error = BasicError(message=message, status=status)
    basic_response = BasicSchema(error=basic_error)
    response = jsonify(BasicResponseSchema().dump(basic_response))
    response.status_code = basic_error.status

    logger.warning(f'Error was occurred: {basic_error}')

    return response
