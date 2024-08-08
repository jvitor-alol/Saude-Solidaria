from flask import flash, redirect, url_for, Response
from flask_login import current_user

from ..extensions import db
from ..forms import UpdateAccountForm
from ..controllers import salvar_imagem_temporario
from ..controllers.helpers import normalizar_telefone


def update_user(form: UpdateAccountForm) -> Response:
    current_user.nome = form.nome.data
    current_user.sobrenome = form.sobrenome.data
    current_user.nome_usuario = form.nome_usuario.data
    current_user.email = form.email.data
    current_user.telefone = normalizar_telefone(form.telefone.data)
    current_user.cidade = form.cidade.data
    current_user.estado = form.estado.data
    current_user.pais = form.pais.data
    current_user.data_nascimento = form.data_nascimento.data
    current_user.genero = form.genero.data
    current_user.bio = form.bio.data
    current_user.notificacoes = form.notificacoes.data

    if form.foto_perfil.data:
        path_foto_perfil = salvar_imagem_temporario(form.foto_perfil.data)
        current_user.foto_perfil = path_foto_perfil

    if current_user.tipo_usuario == 'medico':
        current_user.medico.especialidade = form.especialidade.data

    db.session.commit()
    flash("Dados atualizados com sucesso!", "success")
    return redirect(url_for('views.account'))


def get_user_data(form: UpdateAccountForm) -> None:
    form.nome.data = current_user.nome
    form.sobrenome.data = current_user.sobrenome
    form.nome_usuario.data = current_user.nome_usuario
    form.email.data = current_user.email
    form.telefone.data = current_user.telefone
    form.cidade.data = current_user.cidade
    form.estado.data = current_user.estado
    form.pais.data = current_user.pais
    form.data_nascimento.data = current_user.data_nascimento
    form.genero.data = current_user.genero
    form.bio.data = current_user.bio
    form.notificacoes.data = current_user.notificacoes
    if current_user.tipo_usuario == 'medico':
        form.especialidade.data = current_user.medico.especialidade
