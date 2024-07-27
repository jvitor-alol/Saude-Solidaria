from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, logout_user

from ..controllers import login_user_controller
from ..forms import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = LoginForm()
    if form.validate_on_submit():
        return login_user_controller(form=form)

    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))
