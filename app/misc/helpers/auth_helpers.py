from flask_login import current_user
from flask import abort
from http import HTTPStatus
from functools import wraps
from enum import IntEnum

class Role(IntEnum):
    USER = 1
    ADMIN = 2

# Hell naw I'm not doing type annotations for that
def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(HTTPStatus.UNAUTHORIZED)
        if current_user.role.id != Role.ADMIN:
            abort(HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)
    return wrapper