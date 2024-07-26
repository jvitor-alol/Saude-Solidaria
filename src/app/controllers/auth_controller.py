from datetime import datetime, timezone

from flask import flash, redirect, url_for, request, Response
from flask_login import login_user

from ..extensions import bcrypt, db
from ..models import Usuario
from ..forms import LoginForm


def login_user_controller(form: LoginForm) -> Response:
    user = Usuario.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.senha, form.senha.data):
        login_user(user=user, remember=form.lembre_de_mim.data)
        user.ultimo_login = datetime.now(timezone.utc)
        db.session.commit()
        next_page = request.args.get('next')
        return redirect(next_page) if next_page \
            else redirect(url_for('views.home'))
    flash("Login falhou. Verifique seu email e senha.", 'danger')
