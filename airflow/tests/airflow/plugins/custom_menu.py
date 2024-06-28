from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint
from flask_appbuilder import expose, BaseView as AppBuilderBaseView


bp = Blueprint(
               "test_plugin",
               __name__,
               template_folder="templates" # registers airflow/plugins/templates as a Jinja template folder
               )

class TestAppBuilderBaseView(AppBuilderBaseView):
    default_view = "test"
    @expose("/", methods=['GET', 'POST'])
    def test(self):
        return self.render_template("env.html", content="DEV")

v_appbuilder_view = TestAppBuilderBaseView()
v_appbuilder_package = {
    "name": "Test", # this is the name of the link displayed
    "category": "DEV", # This is the name of the tab under which we have our view
    "view": v_appbuilder_view
}

class AirflowTestPlugin(AirflowPlugin):
    name = "test_plugin"
    operators = []
    flask_blueprints = [bp]
    hooks = []
    executors = []
    admin_views = []
    appbuilder_views = [v_appbuilder_package]
