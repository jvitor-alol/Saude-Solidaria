from flask import Blueprint, redirect, url_for, abort, flash
from flask_login import current_user, login_required

from ..models import Usuario
from ..extensions import db


users = Blueprint('users', __name__)


@users.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    if current_user.id != user_id:
        abort(403)

    if usuario.tipo_usuario == 'medico':
        db.session.delete(usuario.medico)
    db.session.delete(usuario)
    db.session.commit()

    flash("Usuário deletado com sucesso.", 'success')
    return redirect(url_for('auth.logout'))
