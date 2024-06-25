from mlflow.server import app
from mlflow.server.auth import create_app as create_app_orinal
from flask import Flask
from flask_cors import CORS
from flask import Flask, Response, flash, jsonify, make_response, render_template_string, render_template, request

import logging

logging.basicConfig(filename='/opt/mlflow/.mlruns/mlflow.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

g_mlflow_custom_logger = logging.getLogger('mlflow-custom')

def create_app(app: Flask = app):
    CORS(app)
    g_mlflow_custom_logger.debug('--------------- start create_app_orinal')
    app.add_url_rule(
        rule='/mlflow/login',
        view_func=make_login_response,
        methods=["GET"],
    )
    g_mlflow_custom_logger.debug('--------------- end create_app_orinal')
    return create_app_orinal(app)

def make_login_response() -> Response:
    g_mlflow_custom_logger.debug('make_basic')
    # res = make_response("Success login...")
    # res.status_code = 200
    # return res
    res = make_response(render_template('index.html'))
    res.status_code = 200
    return res

# @app.after_request
# def do_something_whenever_a_request_has_been_handled(response):
#     # we have a response to manipulate, always return one
#     return response