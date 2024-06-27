# Install instructions:
# * Place file inside of Airflow path. For example: /usr/local/lib/python3.6/site-packages/airflow/custom/auth/backends/custom_ldap_auth.py
# * In airflow.cfg, reference field api.auth_backend = airflow.custom.auth.backends.custom_ldap_auth
# * Rewrite logic for function `requires_authentication()` to suit your own needs. This implementation checks to see if the
#   LDAP user's role is equal to the "owner" field.

from functools import wraps
import base64

from typing import Any, Callable, TypeVar, cast
from flask import Response, make_response
from flask_appbuilder.security.sqla.models import User
from werkzeug.security import check_password_hash

from airflow.utils.db import create_session
from airflow.utils.log.logging_mixin import LoggingMixin

_log = LoggingMixin().log
CLIENT_AUTH: tuple[str, str] | Any | None = None
T = TypeVar("T", bound=Callable)

def init_app(_):
    """Initializes authentication backend"""
    print('###################################### init ######################################')
    _log.debug('##############################################################')

def _authenticate_password(username, password):
    with create_session() as session:
        user = session.query(User).filter(User.username == username).first()
        if not user:
            _log.info(f'[API] Received an unauthorized API call. User "{username}" does not exist.')
            return False

        existing_password_hash = user.password
        authenticate = check_password_hash(existing_password_hash, password)

        if not authenticate:
            _log.info(f"[API] Received an unauthorized API call. Incorrect password for user: {username}")

        return authenticate

def _forbidden():
    return Response("Forbidden", 403)

def requires_authentication(function: T):
    """Decorator for functions that require authentication"""

    @wraps(function)
    def decorated(*args, **kwargs):
        from flask import request

        header = request.headers.get("Authorization")
        if not header:
            _log.debug(
                "[API] Received an invalid API call. No Authorization header present."
            )
            return _forbidden()

        userpass = "".join(header.split()[1:])
        username, password = base64.b64decode(userpass).decode("utf-8").split(":", 1)

        if not _authenticate_password(username, password):
            return _forbidden()

        response = function(*args, **kwargs)
        response = make_response(response)

        return response

    return decorated
