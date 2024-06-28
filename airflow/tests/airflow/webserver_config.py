"""Default configuration for the Airflow webserver."""

from __future__ import annotations

import os

from airflow.www.fab_security.manager import AUTH_REMOTE_USER

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

from airflow_auth.custom2 import AirflowAstroSecurityManager

# https://github.com/astronomer/astronomer-fab-securitymanager/blob/main/src/astronomer/flask_appbuilder/security.py

AUTH_TYPE = AUTH_REMOTE_USER
SECURITY_MANAGER_CLASS = AirflowAstroSecurityManager

# from typing import Any, Callable

# from flask import current_app
# from flask_appbuilder.const import AUTH_REMOTE_USER
# from flask import redirect, session, g, Request
# from flask_appbuilder import expose
# from flask_login import login_user

# class CustomMiddleware:
#     def __init__(self, wsgi_app: Callable) -> None:
#         print('__init__ ###############################')
#         self.wsgi_app = wsgi_app

#     def __call__(self, environ: dict, start_response: Callable) -> Any:
#         print('__call__ ###############################')
#         request = Request(environ)
#         first_path = request.path.lstrip("/").partition("/")[0]
#         print(f'first_path : {first_path}')
#         # print(f'environ["REMOTE_USER"] : {environ["REMOTE_USER"]}')
#         environ["nav_middleware.app_name"] = first_path
#         environ["REMOTE_USER"] = "aaaaa"
#         return self.wsgi_app(environ, start_response)
#         # Custom authenticating logic here
#         # ...
#         environ["REMOTE_USER"] = "username"
        
#         return self.wsgi_app(environ, start_response)

#     @expose("/login/")
#     def login(self):
#         if g.user is not None and g.user.is_authenticated:
#             return redirect(self.appbuilder.get_url_for_index)

#         # username = self.get_username_from_header()
#         username = 'admin'
#         # self.get_or_create_user(username)
#         user = self.appbuilder.sm.auth_user_remote_user(username)
#         login_user(user)
#         session.pop("_flashes", None)

#         return redirect(self.appbuilder.get_url_for_index)

# current_app.wsgi_app = CustomMiddleware(current_app.wsgi_app)
