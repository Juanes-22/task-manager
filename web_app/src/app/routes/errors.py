from flask import Blueprint, jsonify
import traceback

from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..constants.http_status_codes import (
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)

from ..extensions import db
#from ..extensions import basic_auth
from ..exceptions import BusinessError


errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(BusinessError)
def handle_business_error(exc):
    return jsonify({"error": exc.message}), exc.status_code


@errors_bp.app_errorhandler(HTTPException)
def handle_http_exception(exc):
    return jsonify({"error": exc.description}), exc.code


@errors_bp.app_errorhandler(Exception)
def handle_unexpected_error(exc):
    traceback.print_exc()
    return jsonify({"error": f"Unexpected error: {exc}"}), HTTP_500_INTERNAL_SERVER_ERROR


@errors_bp.app_errorhandler(HTTP_403_FORBIDDEN)
def handle_forbidden(exc):
    return jsonify({"error": "Forbidden"}), exc.code


@errors_bp.app_errorhandler(HTTP_404_NOT_FOUND)
def handle_not_found(exc):
    return jsonify({"error": "Not found"}), exc.code


@errors_bp.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(exc):
    db.session.rollback()
    return (
        jsonify({"error": f"Database error: {exc}"}),
        HTTP_500_INTERNAL_SERVER_ERROR,
    )


@errors_bp.app_errorhandler(ValidationError)
def handle_invalid_data(exc):
    return jsonify({"error": exc.messages}), HTTP_400_BAD_REQUEST


# @basic_auth.error_handler
# def unauthorized():
#     return jsonify({"error": "Unauthorized access"}), HTTP_401_UNAUTHORIZED
