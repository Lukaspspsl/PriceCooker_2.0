import os
import logging


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Other production-specific settings


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Other test-specific settings


class LoggingConfig(Config):
    """Logging configuration."""


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
