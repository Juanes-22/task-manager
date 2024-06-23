from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    jwt_required,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
)

from ..schemas.auth import UserResponseSchema, UserRegisterSchema, UserLoginSchema
from ..models.auth import User, JWTTokenBlockList
from ..services.auth_services import AuthServices
from ..helpers.auth import add_jwt_token_to_blacklist

from ..constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

auth_service = AuthServices()


@auth_bp.post("/register")
def register():
    data = request.json
    schema = UserRegisterSchema()
    user: User = schema.load(data)
    auth_service.register(user)
    return jsonify({"message": "User succesfuly registered!"}), HTTP_201_CREATED


@auth_bp.get("/me")
@jwt_required()
def me():
    current_user = get_jwt_identity()
    schema = UserResponseSchema()
    serialized_user = schema.dump(current_user)
    return serialized_user, HTTP_200_OK


@auth_bp.post("/login")
def login():
    data = request.json
    schema = UserLoginSchema()
    user_creds = schema.load(data)

    user = auth_service.login(user_creds["email"], user_creds["password"])
    identity = {"id": user.id, "email": user.email, "username": user.username}
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({"message": "Login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, HTTP_200_OK


@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = jsonify({"message": "Access token refreshed"})
    set_access_cookies(response, access_token)
    return response, HTTP_200_OK


@auth_bp.route("/logout", methods=["POST"])
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()
    token_type = jwt["type"]

    # revoke token
    add_jwt_token_to_blacklist(jwt)

    response = jsonify(
        {"message": f"Successfully logged out: {token_type} token revoked"}
    )
    unset_jwt_cookies(response)
    return response, HTTP_200_OK
