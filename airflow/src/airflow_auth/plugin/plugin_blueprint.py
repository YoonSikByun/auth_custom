from flask import Blueprint

bp = Blueprint(
               "test_plugin",
               __name__,
               template_folder="templates", # registers airflow/plugins/templates as a Jinja template folder
               )
               
               
class TestAppBuilderBaseView(AppBuilderBaseView):
    default_view = "test"

    @expose("/", methods=['GET', 'POST'])
    def test(self):
        return self.render_template("env.html", content="DEV")