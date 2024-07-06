import os

from flask import Flask
from dotenv import load_dotenv

from .views import views
from .auth import auth

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
