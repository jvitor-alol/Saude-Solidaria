from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, Usuario, Medico
from .forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.senha, form.senha.data):
            # TODO: Criar sessão de usuário
            flash("Login com sucesso.", "success")
            return redirect(url_for('views.home'))
        else:
            flash("Login falhou. Verifique seu email e senha.", "danger")
    return render_template('login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if not validar_usuario_medico(form):
            flash(
                'CRM e Especialidade são obrigatórios para médicos.', 'danger')
            return render_template(
                'register.html', title='Registrar', form=form)

        new_user = criar_usuario(form)

        if form.tipo_usuario.data == 'medico':
            # Insert new_user na database para usar seu id caso seja médico(a)
            db.session.flush()
            criar_medico(new_user.id, form)

        db.session.commit()

        flash(f"Conta criada para {form.nome_usuario.data}.", "success")
        return redirect(url_for('views.home'))

    return render_template('register.html', title='Registrar', form=form)


@auth.route('/logout')
def logout():
    return "<p>LOGOUT</p>"


def validar_usuario_medico(form: RegistrationForm) -> bool:
    if form.tipo_usuario.data == 'medico':
        return form.crm.data and form.especialidade.data
    return True  # Retorna True para usuários comuns


def criar_usuario(form: RegistrationForm) -> Usuario:
    hashed_password = generate_password_hash(form.senha.data)
    new_user = Usuario(
        nome=form.nome.data,
        sobrenome=form.sobrenome.data,
        nome_usuario=form.nome_usuario.data,
        email=form.email.data,
        senha=hashed_password,
        tipo_usuario=form.tipo_usuario.data
    )
    db.session.add(new_user)
    return new_user


def criar_medico(usuario_id: int, form: RegistrationForm) -> None:
    new_medico = Medico(
        usuario_id=usuario_id,
        crm=form.crm.data,
        especialidade=form.especialidade.data
    )
    db.session.add(new_medico)
