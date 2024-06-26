from mlflow.server import app
from mlflow.server.auth import create_app as create_app_orinal
from flask import Flask
from flask_cors import CORS
from flask import Flask, Response, redirect, make_response, request
import base64

from mlflow.server.auth.sqlalchemy_store import SqlAlchemyStore
from mlflow.server.auth import store

import logging
logging.basicConfig(filename='/opt/mlflow/.mlruns/mlflow.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

g_mlflow_custom_logger = logging.getLogger('mlflow-custom')

SESSION_ID = 'session_id'

def create_app(app: Flask = app):
    org_app = create_app_orinal(app)

    CORS(org_app)
    g_mlflow_custom_logger.debug('--------------- start create_app_orinal')
    # org_app.add_url_rule(
    #     rule='/mlflow/start',
    #     view_func=make_login_response,
    #     methods=["GET"],
    # )
    # g_mlflow_custom_logger.debug('--------------- end create_app_orinal')

    # return app

    return org_app

# def make_login_response() -> Response:
    
#     return response

from werkzeug.datastructures import Authorization
from typing import Union

def authenticate_request_auth() -> Union[Authorization, Response]:
    g_mlflow_custom_logger.debug('--------------- start authenticate_request_auth')
    connection = request.cookies.get(SESSION_ID)
    g_mlflow_custom_logger.debug(f'--------------- get cookes connection : {connection}')

    username = ''
    password = ''

    if not connection:
        connection = request.args.get('query_data')
        g_mlflow_custom_logger.debug(f'--------------- get_param : {connection}')

        if not connection:
            return make_session_fail_response()

        username = connection.split(':')[0]
        password = connection.split(':')[1]
        g_mlflow_custom_logger.debug(f'--------------- get_param username : [{username}]')
        g_mlflow_custom_logger.debug(f'--------------- get_param password : [{password}]')
    
        if not store.authenticate_user(username, password):
            return make_session_fail_response()

        response = redirect("/mlflow", code=303)
        response.set_cookie(key=SESSION_ID, value=connection, expires=None, httponly=True)
        g_mlflow_custom_logger.debug(f'--------------- set_cookie : {connection}')

        return response

    if connection is None:
        return make_session_fail_response()

    username = connection.split(':')[0]
    password = connection.split(':')[1]

    g_mlflow_custom_logger.debug(f'--------------- username : [{username}]')
    g_mlflow_custom_logger.debug(f'--------------- password : [{password}]')

    token = f'{username}:{password}'
    token = bytes(token, 'utf-8')
    token = base64.encodebytes(token).decode("utf-8")
    auth = Authorization.from_header(f"Basic {token}")

    g_mlflow_custom_logger.debug(f'--------------- auth.username : {auth.username}')
    g_mlflow_custom_logger.debug(f'--------------- auth.password : {auth.password}')

    if store.authenticate_user(username, password):
        return auth
    else:
        # let user attempt login again
        return make_session_fail_response()

def make_session_fail_response() -> Response:
    res = make_response(
        "인증되지 않은 사용자입니다."
        "관리자에게 문의해주십시오."
    )
    res.status_code = 401
    return res
