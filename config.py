"""Class-based Flask app configuration."""
from os import environ, path, urandom

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Configuration from environment variables."""
    def __init__(self):
       logging.basicConfig(level=logging.DEBUG)

    SECRET_KEY = environ.get("SECRET_KEY", default=urandom(16))
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = "zmoodapi.py"

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

