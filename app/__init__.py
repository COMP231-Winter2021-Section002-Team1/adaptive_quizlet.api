
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='../static')

    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.from_object(__name__)
    Session(app)
    db.init_app(app)
    from main_blue_print import main
    app.register_blueprint(main, url_prefix='/')

    return app
