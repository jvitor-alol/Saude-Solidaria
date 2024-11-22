from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from flask_babel import format_datetime

from ..models import Post
from ..forms import RegistrationForm, UpdateAccountForm
from ..controllers import register_user, update_user, get_user_data
from ..controllers.helpers import get_medico
from ..models.historico import Historico


views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    postagens = Post.query.all()

    # Formata a data para exibição
    for post in postagens:
        post.data_formatada = format_datetime(
            post.data_publicacao, "EEEE, d 'de' MMMM 'de' yyyy")

    return render_template('home.html', postagens=postagens)


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

@views.route('/dengue')
def dengue_info():
    return render_template('dengue_info.html')


@views.route('/contato')
def contato():
    return render_template('contato.html')



@views.route('/enviar-contato', methods=['POST'])
def enviar_contato():
    try:
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        # Processamento
        return redirect(url_for('views.obrigado'))
    except Exception as e:
        flash(f'Ocorreu um erro: {str(e)}', 'danger')
        return redirect(url_for('views.contato'))


@views.route('/aids_info')
def aids_info():
    return render_template('aids_info.html')


@views.route('/saude_mental_info')
def saude_mental_info():
    return render_template('saude_mental_info.html')

@views.route('/gripe-covid')
def gripe_covid_info():
    return render_template('gripe-covid_info.html')


@views.route('/cancer_de_pele_info')
def cancer_de_pele_info():
    return render_template('cancer_de_pele_info.html')


@views.route('/campanha_do_sono_info')
def campanha_do_sono_info():
    return render_template('campanha_do_sono_info.html')


from flask import render_template

@views.route('/historico')
def historico():
    # Exemplo de dados a serem exibidos (isto pode vir de um banco de dados, por exemplo)
    historico_data = [
        {'id': 1, 'data': '19/11/2024', 'descricao': 'Exemplo de entrada no histórico'},
        {'id': 2, 'data': '18/11/2024', 'descricao': 'Outra entrada no histórico'},
    ]
    return render_template('historico.html', historico_data=historico_data)


