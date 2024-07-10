from flask import Blueprint, render_template, flash, redirect, url_for

from .forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.email.data == 'admin@admin.com' and
                form.password.data == 'admin'):
            flash("Login com sucesso.", "success")
            return redirect(url_for('views.home'))
        else:
            flash("Login falhou. Verifique o email e a senha.", "danger")
    return render_template('login.html', title='Login', form=form)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Conta criada para {form.username.data}.", "success")
        return redirect(url_for('views.home'))
    return render_template('sign_up.html', title='Registrar', form=form)

@auth.route('/logout')
def logout():
    return "<p>LOGOUT</p>"