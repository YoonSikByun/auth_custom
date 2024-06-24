from mlflow.server import app
from flask import Flask
from flask_cors import CORS
from flask import Flask, Response, flash, jsonify, make_response, render_template_string, request


def create_app(app: Flask = app):
    CORS(app)
    print('---------------')
    app.add_url_rule(
        rule='/mlflow/login',
        view_func=make_basic_response,
        methods=["GET"],
    )
    print('---------------')
    return app



def make_basic_response() -> Response:
    print('make_basic')
    res = make_response(
        "custom login page"
    )
    res.status_code = 200
    # res.headers["WWW-Authenticate"] = 'Basic realm="mlflow"'
    return res

@app.after_request
def do_something_whenever_a_request_has_been_handled(response):
    # we have a response to manipulate, always return one
    return response