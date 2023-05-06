from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from security.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login.login_to'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # autopep8: off
    from security.main.routes import main
    from security.users.routes import users
    from security.login.routes import login
    from security.errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(login)
    app.register_blueprint(errors)

    return app
