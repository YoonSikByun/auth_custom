# Copyright 2019 Astronomer Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
import functools
import json
from logging import getLogger
import os
from time import monotonic_ns
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import airflow
from airflow.exceptions import AirflowConfigException
from flask import abort, flash, redirect, request, session, url_for, make_response
from flask_appbuilder.security.manager import AUTH_REMOTE_USER
from flask_appbuilder.security.views import AuthView, expose
from flask_login import current_user, login_user, logout_user
from packaging.version import Version
from airflow.configuration import conf
from airflow.utils.airflow_flask_app import get_airflow_app

try:
    from airflow.www.security import EXISTING_ROLES, AirflowSecurityManager
except ImportError:
    # Airflow not installed, likely we are running setup.py to _install_ things
    class AirflowSecurityManager(object):
        def __init__(self, appbuilder):
            pass
    EXISTING_ROLES = []

log = getLogger(__name__)

AIRFLOW_VERSION_TUPLE = Version(airflow.__version__).release

class AstroSecurityManagerMixin(object):
    def __init__(self, appbuilder):
        base_url = conf.get(section="webserver", key="base_url")
        super().__init__(appbuilder)
        if self.auth_type == AUTH_REMOTE_USER:
            print(f'AUTH_REMOTE_USER [base_url : {base_url}]########################')
            self.authremoteuserview = AuthAstroJWTView

    def before_request(self):
        print(f'[{request.path}] before_request ########################')
        if request.path == '/health':
            return super().before_request()

        # username='admin'
        # email='admin@amdin'

        # if current_user.is_anonymous:
        #     print('current_user.is_anonymous ########################')
        #     user = self.find_user(username=username)
        #     if user is None:
        #         abort(401)

        #     # Similar to the upstream FAB security managers, update
        #     # authentication stats so user admins can view them without
        #     # having to dig through webserver logs
        #     if not user.login_count:
        #         user.login_count = 0
        #     user.login_count += 1
        #     user.last_login = datetime.datetime.now()
        #     user.fail_login_count = 0

        #     self.get_session.add(user)
        #     self.get_session.commit()
        #     if not login_user(user):
        #         print('raise RuntimeError("Error logging user in!") current_user.is_anonymous ########################')
        #         raise RuntimeError("Error logging user in!")
        #     # session["roles"] = claims['roles']
        #     print('pass current_user.is_anonymous ########################')
        # else:
        #     print('/login ########################')
        # #     session_roles = session['roles']
        # #     # claim_roles = claims['roles']
        # #     if set(session_roles) != set(claim_roles):
        # #         logout_user()
        # #         flash('Your permission set has changed. You have been redirected to the Airflow homepage with your new permission set.')
        #     logout_user()
        #     return redirect('/login/')
        #     # abort(401)

        super().before_request()

class AirflowAstroSecurityManager(AstroSecurityManagerMixin, AirflowSecurityManager):
    def __init__(self, appbuilder):
        print('AirflowAstroSecurityManager ########################')
        kwargs = {
            'appbuilder': appbuilder,
        }
        super().__init__(**kwargs)


    def before_request(self):
        return super().before_request()


class AuthAstroJWTView(AuthView):
    # @expose("/access-denied/")
    @expose("/login/")
    def login(self):
        print('login ########################')
        res = make_response('login page....')
        username = 'admin'
        find_user = get_airflow_app().appbuilder.sm.find_user
        user = find_user(username=username)
        print(f'user : {user} ##########################')
        if not login_user(user):
            print('raise RuntimeError("Error logging user in!") current_user.is_anonymous ########################')
            raise RuntimeError("Error logging user in!")
        res.status_code = 200
        return redirect('/home')
        # return abort(403)
        return res
    @expose("/test-page/")
    def test_page(self):
        print('test-page ########################')
        res = make_response('test page....')
        res.status_code = 200
        # return abort(403)
        return res