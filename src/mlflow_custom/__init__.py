from mlflow.server import app
from mlflow.server.auth import create_app as create_app_orinal
from flask import Flask
from flask_cors import CORS
from flask import Flask, Response, redirect, jsonify, make_response, render_template_string, render_template, request
# from jinja2 import TemplateNotFound
# import logging
from pathlib import Path
# import mlflow_custom

import os

# logging.basicConfig(filename='/opt/mlflow/.mlruns/mlflow.log',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

# g_mlflow_custom_logger = logging.getLogger('mlflow-custom')

def create_app(app: Flask = app):
    CORS(app)
    # g_mlflow_custom_logger.debug('--------------- start create_app_orinal')
    app.add_url_rule(
        rule='/mlflow/login',
        view_func=make_login_response,
        methods=["GET"],
    )
    # g_mlflow_custom_logger.debug('--------------- end create_app_orinal')

    # return app
    return create_app_orinal(app)

def make_login_response() -> Response:
    # g_mlflow_custom_logger.debug('make_basic')

    # try:
        return redirect("/mlflow", code=303)
    # except TemplateNotFound:
    #     res = make_response('Not found templates.')
    #     res.status_code = 404
    # res.status_code = 200

    # return res

# def make_login_response() -> Response:
#     g_mlflow_custom_logger.debug('make_basic')
    
#     module_path = os.path.abspath(mlflow_custom.__file__)
#     module_dir = os.path.dirname(os.path.abspath(module_path))
#     html_file = os.path.join(module_dir, 'templates', 'index.html')
    
#     file_path = Path(html_file)    
#     file_content = file_path.read_text()

#     try:
#         res = make_response(render_template_string(file_content))
#     except TemplateNotFound:
#         res = make_response('Not found templates.')
#         res.status_code = 404
#     res.status_code = 200

#     return res
