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


def init_app(_):
    """Initializes authentication backend"""


def _authenticate_password(username, password):
    with create_session() as session:
        user = session.query(User).filter(User.username == username).first()
        if not user:
            _log.info(
                f'[API] Received an unauthorized API call. User "{username}" does not exist.'
            )
            return False
        existing_password_hash = user.password
        authenticate = check_password_hash(existing_password_hash, password)
        if not authenticate:
            _log.info(
                f"[API] Received an unauthorized API call. Incorrect password for user: {username}"
            )
        return authenticate


def _authenticate_function_call(username, function, args, kwargs):
    function_name = function.__name__
    if function_name == "trigger_dag":
        return _authenticate_function_call__trigger_dag(
            username, function, args, kwargs
        )
    elif function_name in ("create_pool", "delete_pool"):
        _log.info(
            f"[API] Received an unauthorized API call by {username}. Cannot call functions create_pool() or delete_pool()."
        )
        return False
    else:
        return True


def _authenticate_function_call__trigger_dag(username, function, args, kwargs):
    dag_id = kwargs.get("dag_id")
    if not dag_id:
        _log.info(
            f"[API] Received an invalid API call by {username}. No dag_id specified."
        )
        return False
    with create_session() as session:
        # TODO: Use the ORM instead of a direct query.
        is_dag_owner = session.execute(
            """
            SELECT 1
            FROM
                ab_user
                INNER JOIN ab_user_role ON 
                    ab_user.id = ab_user_role.user_id
                INNER JOIN ab_role ON 
                    ab_user_role.role_id = ab_role.id
                INNER JOIN dag ON
                    ab_role.name = dag.owners
            WHERE
                ab_user.username = :username
                AND dag_id = :dag_id
            """,
            {"username": username, "dag_id": dag_id},
        )
        authorized = is_dag_owner.rowcount > 0
        if not authorized:
            _log.info(
                f"[API] Received an unauthorized API call by {username}. Not authorized to run dag_id: {dag_id}"
            )
        else:
            _log.info(
                f"[API] Successfully authorizing {username} to create a DagRun for {dag_id}"
            )
        return authorized


def _forbidden():
    return Response("Forbidden", 403)


def requires_authentication(function):
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
        if not _authenticate_function_call(username, function, args, kwargs):
            return _forbidden()

        response = function(*args, **kwargs)
        response = make_response(response)
        return response

    return decorated