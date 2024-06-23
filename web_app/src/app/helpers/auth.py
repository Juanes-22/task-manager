from ..models.auth import JWTTokenBlockList
from flask_jwt_extended import (
    get_jwt
)


def is_jwt_token_in_blacklist(jwt_data):
    jti = jwt_data["jti"]
    token = JWTTokenBlockList.get_by_jti(jti)
    return token is not None


def add_jwt_token_to_blacklist(jwt_data):
    jwt = get_jwt()
    jti = jwt["jti"]

    token = JWTTokenBlockList(jti=jti)
    token.save()
