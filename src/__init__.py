from flask import Flask

from config import configurations
from .auth import auth
from .views import views
from .models import db, migrate


def create_app(config='default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()
