
from flask import Flask
from init import db, ma, bcrypt, jwt
from controller.auth_controller import auth_bp
from controller.cli_controller import db_commands
from controller.playlist_controller import playlist_bp
import os


def create_app():

    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(playlist_bp)
    return app
