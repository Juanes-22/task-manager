from .models import User
from ..common.exceptions import BusinessError

from ..constants.http_status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)


class AuthServices:

    def register(self, user: User) -> None:
        existing_user = User.get_by_email(user.email)
        if existing_user:
            raise BusinessError(
                message="User already exists",
                status_code=HTTP_409_CONFLICT,
            )
        
        user.hash_password()
        user.save()

    def login(self, email: str, password: str) -> User:
        user = User.get_by_email(email)
        if not user:
            raise BusinessError(
                message="User does not exist",
                status_code=HTTP_404_NOT_FOUND,
            )
        
        if not user.is_password_valid(password):
            raise BusinessError(
                message="Password is not valid",
                status_code=HTTP_404_NOT_FOUND,
            )
        
        return user
