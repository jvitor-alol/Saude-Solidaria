from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from ..forms import RegistrationForm, UpdateAccountForm
from ..controllers import register_user, update_user, get_user_data
from ..controllers.helpers import get_medico


views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html')


@views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        return register_user(form=form)

    return render_template('register.html', title='Registrar', form=form)


@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    medico = get_medico()
    if form.validate_on_submit():
        update_user(form=form)
    elif request.method == 'GET':
        get_user_data(form=form)
    return render_template(
        'account.html',
        title='Conta', form=form, crm=medico.crm if medico else None)
