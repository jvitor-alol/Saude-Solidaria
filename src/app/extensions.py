from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_babel import Babel
from flask_login import LoginManager

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
bootstrap = Bootstrap5()
ckeditor = CKEditor()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Faça o login para acessar essa página."


def init_extensions(app: Flask) -> None:
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
