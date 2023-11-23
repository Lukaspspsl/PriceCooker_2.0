from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.db import mongo
import logging
from config import DevelopmentConfig
from flask_login import LoginManager
from app.views.operations import api
from app.views.home import home
from app.auth.auth import auth_bp
from app.views.userloader import login_manager

def create_app(config_class=DevelopmentConfig):
    print("Creating app...")
    app = Flask(__name__)
    app.config.from_object(config_class)

    print("Database init...")
    mongo.init_app(app)

    login_manager.init_app(app)

    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging enabled")

    app.register_blueprint(api, url_prefix="/")
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth/")
    print("Blueprint registered")

    return app


if __name__ == "__main__":
    print("Starting process...")
    app = create_app()
    print("App created")
    app.run(debug=True)
