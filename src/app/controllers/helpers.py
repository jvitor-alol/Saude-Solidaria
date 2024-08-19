import re

from flask_login import current_user
from bleach import clean

from ..models import Usuario, Medico
from ..forms import RegistrationForm
from ..extensions import login_manager, bcrypt, db


@login_manager.user_loader
def load_user(user_id: int) -> Usuario:
    return Usuario.query.get(user_id)


def validar_usuario_medico(form: RegistrationForm) -> bool:
    if form.tipo_usuario.data == 'medico':
        return form.crm.data and form.especialidade.data
    return True  # Retorna True para usuários comuns


def criar_usuario(form: RegistrationForm) -> Usuario:
    hashed_password = bcrypt.generate_password_hash(form.senha.data) \
        .decode('utf-8')
    new_user = Usuario(
        nome=clean(form.nome.data),
        sobrenome=clean(form.sobrenome.data),
        nome_usuario=clean(form.nome_usuario.data),
        email=clean(form.email.data),
        senha=hashed_password,
        tipo_usuario=form.tipo_usuario.data
    )
    db.session.add(new_user)
    return new_user


def criar_medico(usuario_id: int, form: RegistrationForm) -> None:
    new_medico = Medico(
        usuario_id=usuario_id,
        crm=clean(form.crm.data),
        especialidade=form.especialidade.data
    )
    db.session.add(new_medico)


def get_medico() -> Medico:
    if current_user.tipo_usuario == 'medico':
        return current_user.medico
    return None


def normalizar_telefone(telefone: str) -> str:
    telefone = str(telefone)  # Força o cast para evitar TypeErrors
    telefone_normalizado = re.sub(r'[^\d+]', '', telefone)
    return telefone_normalizado
