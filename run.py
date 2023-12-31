from dotenv import load_dotenv
from app.scraping.scheduler import periodical_scraper
from flask import Flask
from app.db import mongo
import logging
from config import DevelopmentConfig

from app.views.operations import api
from app.views.home import home
from app.auth.auth import auth_bp
from app.views.userloader import login_manager
from threading import Thread
import time

load_dotenv()


def run_periodically(interval, func, app):
    def inner_func():
        while True:
            func(app)
            time.sleep(interval)

    thread = Thread(target=inner_func)
    thread.start()


def create_app(config_class=DevelopmentConfig):
    print("Creating app...")
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # app.config['LOGIN_URL'] = 'auth.login'

    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging enabled")

    app.register_blueprint(api, url_prefix="/")
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth/")

    run_periodically(600, periodical_scraper, app) #3600

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
