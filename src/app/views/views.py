from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os

from ..controllers import register_user_controller
from ..forms import RegistrationForm

views = Blueprint('views', __name__)

# Pasta onde os uploads serão salvos temporariamente
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Configurando o upload folder na aplicação
views.config = {}
views.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        return register_user_controller(form=form)

    return render_template('register.html', title='Registrar', form=form)


@views.route('/account')
@login_required
def account():
    return render_template('account.html', title='Conta')


def allowed_file(filename):
    """Função para verificar extensões de arquivo permitidas (exemplo para imagens)"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhum arquivo encontrado na requisição'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(views.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': f'Imagem {filename} enviada com sucesso!'}), 200

    return jsonify({'error': 'Tipo de arquivo inválido'}), 400
