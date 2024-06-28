from flask_appbuilder.security.views import AuthView
# from airflow.www.views import AirflowBaseView
from typing import Any, Callable
from flask_appbuilder import expose
from flask import redirect, session, g, make_response
from flask_login import login_user
import logging
from airflow.auth.managers.fab.security_manager.override import FabAirflowSecurityManagerOverride

class AuthRemoteUserView(AuthView):
    
    @expose("/login/")
    def login(self):
        print('login ####################################')
        if g.user is not None and g.user.is_authenticated:
            logging.info(f"{g.user.username} already logged in")
            return redirect(self.appbuilder.get_url_for_index)

        # username = self.get_username_from_header()
        username = 'admin'
        # self.get_or_create_user(username)
        user = self.appbuilder.sm.auth_user_remote_user(username)
        login_user(user)
        session.pop("_flashes", None)

        return redirect(self.appbuilder.get_url_for_index)

    @expose("/logout/", methods=["POST"])
    def logout(self):
        res = make_response('log out')
        return res

    # def get_or_create_user(self, username):
    #     user = self.appbuilder.sm.find_user(username)

    #     if user is None:
    #         user = self.appbuilder.sm.add_user(
    #             username,
    #             username,
    #             "-",  # dummy last name
    #             f"{username}@squareup.com",
    #             self.get_or_create_roles_from_headers(),
    #             "password",  # dummy password
    #         )

    #     return user

class SecurityManager(FabAirflowSecurityManagerOverride):
    # authremoteuserview = AuthRemoteUserView
    auth_view = AuthRemoteUserView

    # def __init__(self, wsgi_app: Callable) -> None:
    #     super().__init__(wsgi_app)
    #     print("__init__ ###############################################")
    #     self.wsgi_app = wsgi_app

    # def __call__(self, environ: dict, start_response: Callable) -> Any:
    #     print("__call__ ###############################################")
    #     # Custom authenticating logic here
    #     # ...
    #     # environ["REMOTE_USER"] = "username"
    #     return self.wsgi_app(environ, start_response)

    def register_views(self):
        print("register_views ###############################################")
        """Register views specific to AWS auth manager."""
        self.appbuilder.add_view_no_menu(AuthRemoteUserView())
