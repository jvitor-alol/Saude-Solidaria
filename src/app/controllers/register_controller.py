from typing import Union

from flask import flash, redirect, url_for, render_template, Response

from .helpers import validar_usuario_medico, criar_usuario, criar_medico
from ..extensions import db
from ..forms import RegistrationForm


def register_user_controller(form: RegistrationForm) -> Union[Response, str]:
    if not validar_usuario_medico(form):
        flash(
            "CRM e Especialidade são obrigatórios para médicos.", 'danger')
        return render_template(
            'register.html', title='Registrar', form=form)

    new_user = criar_usuario(form)

    if form.tipo_usuario.data == 'medico':
        # Insere new_user na database para usar seu id caso seja médico(a)
        db.session.flush()
        criar_medico(new_user.id, form)

    db.session.commit()
    flash(f"Conta criada para {form.nome_usuario.data}.", 'success')
    return redirect(url_for('views.home'))
