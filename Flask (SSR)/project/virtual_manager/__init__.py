import os
from flask import Flask

from virtual_manager.helpers import usd, format_field_name

# Configure application
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'virtual_manager.sqlite'),
    )

    # Custom filter
    app.jinja_env.filters["usd"] = usd
    app.jinja_env.filters["field"] = format_field_name

    if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_pyfile('config.py', silent=True)
    else:
      # load the test config if passed in
      app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
      os.makedirs(app.instance_path)
    except OSError:
      pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
      return 'Hello, World!'

    from . import db
    db.init_app(app)

    from virtual_manager import src
    app.register_blueprint(src.index.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(src.auth.bp)
    app.register_blueprint(src.items.bp)

    return app
