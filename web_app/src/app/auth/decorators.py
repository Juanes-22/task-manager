from functools import wraps
from typing import Callable, Union
from flask import abort
from flask_jwt_extended import get_current_user

from .models import User

from ..constants.http_status_codes import HTTP_403_FORBIDDEN

import logging


def auth_role(role: Union[str, list[str]]) -> Callable:
    """
    Decorator to check if the current user has the required role(s).

    This decorator must be used after the `jwt_required` decorator to ensure
    the user is authenticated before checking their roles.

    Args:
        role (Union[str, List[str]]): A role or list of roles to check against the current user.

    Returns:
        Callable: The decorated function if the user has the required role(s), otherwise aborts with HTTP 403.
    """

    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user: User = get_current_user()
            roles = [role] if isinstance(role, str) else role
            if not any(current_user.has_role(r) for r in roles):
                logging.error(f"Current user missing any of roles {roles}")
                abort(HTTP_403_FORBIDDEN)
            return fn(*args, **kwargs)

        return decorator

    return wrapper
