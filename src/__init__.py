from flask import Flask

from .auth import auth
from .views import views
from config import configurations


def create_app(config='default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
