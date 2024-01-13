import os
from flask import Flask
from flask_session import Session

from virtual_manager.helpers import usd

# Configure application
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'virtual_manager.sqlite'),
    )

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    test_config = None
    
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

    from . import db
    db.init_app(app)

    from virtual_manager import src
    app.register_blueprint(src.index.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(src.auth.bp)
    app.register_blueprint(src.items.bp)

    return app