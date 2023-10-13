#sqlite3 /tmp/test.db
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy(session_options={"expire_on_commit": False})

def create_app(config_name='development'):
    app = Flask(__name__)
    #CORS
    CORS(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    #DB
    db.init_app(app)

    register_modules(app)

    return app

def register_modules(app):
    from api.init_game import init_game_bp
    app.register_blueprint(init_game_bp, url_prefix='/init_game')