from mlflow.server import app
from mlflow.server.auth import create_app as create_app_orinal
from flask import Flask
from flask_cors import CORS
from flask import Flask, Response, redirect, make_response, request
import base64

from mlflow.server.auth import store

# import logging
# logging.basicConfig(filename='/opt/mlflow/.mlruns/mlflow.log',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

# g_mlflow_custom_logger = logging.getLogger('mlflow-custom')

SESSION_ID = 'session_id'

def create_app(app: Flask = app):
    org_app = create_app_orinal(app)

    CORS(org_app)
    # g_mlflow_custom_logger.debug('--------------- start create_app_orinal')
    org_app.add_url_rule(
        rule='/mlflow/logout',
        view_func=make_logout_response,
        methods=["GET"],
    )
    return org_app

def make_logout_response() -> Response:
    response = make_response('Logout completed.')
    response.set_cookie(key=SESSION_ID, value='', expires=None, httponly=True)
    return response

from werkzeug.datastructures import Authorization
from typing import Union

def authenticate_request_auth() -> Union[Authorization, Response]:
    # g_mlflow_custom_logger.debug('--------------- start authenticate_request_auth')
    connection = request.cookies.get(SESSION_ID)
    # g_mlflow_custom_logger.debug(f'--------------- get cookes connection : {connection}')

    username = ''
    password = ''

    if not connection:
        connection = request.args.get('query_data')

        if not connection:
            return make_session_fail_response()

        username = connection.split(':')[0]
        password = connection.split(':')[1]
    
        if not store.authenticate_user(username, password):
            return make_session_fail_response()

        response = redirect("/mlflow", code=303)
        response.set_cookie(key=SESSION_ID, value=connection, expires=None, httponly=True)

        return response

    if connection is None:
        return make_session_fail_response()

    username = connection.split(':')[0]
    password = connection.split(':')[1]

    token = f'{username}:{password}'
    token = bytes(token, 'utf-8')
    token = base64.encodebytes(token).decode("utf-8")
    auth = Authorization.from_header(f"Basic {token}")

    if store.authenticate_user(username, password):
        return auth
    else:
        # let user attempt login again
        return make_session_fail_response()

def make_session_fail_response() -> Response:
    res = make_response(
        "인증되지 않은 사용자입니다. 관리자에게 문의해주십시오."
    )
    res.status_code = 401
    return res
