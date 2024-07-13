from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect

from config import configurations
from .models import db, migrate
from .auth import auth, bcrypt
from .views import views

bootstrap = Bootstrap5()
csrf = CSRFProtect()


def create_app(config='default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    # Inicialização de extensões
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    # Registro de Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app


def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()
