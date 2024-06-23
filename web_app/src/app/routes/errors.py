from flask import Blueprint, jsonify, current_app

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
from ..extensions import jwt

from ..exceptions import BusinessError
from ..helpers.errors import log_error

errors_bp = Blueprint("errors", __name__)


def get_error_message(exc, default_message):
    if current_app.config["ENV"] != "production":
        return f"{default_message}: {exc}"
    return default_message


@errors_bp.app_errorhandler(BusinessError)
def handle_business_error(exc):
    log_error(exc, print_traceback=True)
    return jsonify({"error": exc.message}), exc.status_code


@errors_bp.app_errorhandler(HTTPException)
def handle_http_exception(exc):
    log_error(exc)
    return jsonify({"error": exc.description}), exc.code


@errors_bp.app_errorhandler(Exception)
def handle_unexpected_error(exc):
    log_error(exc, print_traceback=True)
    error_message = get_error_message(exc, "An unexpected error occurred")
    return jsonify({"error": error_message}), HTTP_500_INTERNAL_SERVER_ERROR


@errors_bp.app_errorhandler(HTTP_403_FORBIDDEN)
def handle_forbidden(exc):
    log_error(exc)
    return jsonify({"error": "Forbidden"}), exc.code


@errors_bp.app_errorhandler(HTTP_404_NOT_FOUND)
def handle_not_found(exc):
    log_error(exc)
    return jsonify({"error": "Not found"}), exc.code


@errors_bp.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(exc):
    log_error(exc, print_traceback=True)
    db.session.rollback()
    error_message = get_error_message(exc, "A database error occurred")
    return jsonify({"error": error_message}), HTTP_500_INTERNAL_SERVER_ERROR


@errors_bp.app_errorhandler(ValidationError)
def handle_invalid_data(exc):
    log_error(exc)
    return jsonify({"error": exc.messages}), HTTP_400_BAD_REQUEST


@jwt.invalid_token_loader
def handle_invalid_token(exc):
    log_error(exc)
    error_message = get_error_message(exc, "Invalid token")
    return jsonify({"error": error_message}), HTTP_400_BAD_REQUEST


@jwt.unauthorized_loader
def handle_missing_token(exc):
    log_error(exc)
    error_message = get_error_message(exc, "Unauthorized: missing token")
    return jsonify({"error": error_message}), HTTP_401_UNAUTHORIZED


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_data):
    return jsonify({"error": "Token expired"}), HTTP_400_BAD_REQUEST
