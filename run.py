from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.db import mongo
import logging
from config import DevelopmentConfig
from app.views.operations import api


def create_app(config_class=DevelopmentConfig):
    print("Creating app...")
    app = Flask(__name__)
    app.config.from_object(config_class)

    print("Database init...")
    mongo.init_app(app)

    logging.basicConfig(level=logging.DEBUG)

    @app.route('/')
    def home():
        return "Hello World!"

    app.register_blueprint(api)
    print("Blueprint registered")

    return app


if __name__ == "__main__":
    print("Starting process...")
    app = create_app()
    print("App created")
    app.run(debug=True)
