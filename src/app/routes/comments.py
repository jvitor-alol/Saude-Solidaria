from datetime import datetime, timezone

from flask import Blueprint, abort, request, url_for, redirect, flash
from flask_login import login_required, current_user
from bleach import clean

from ..models import Comentario
from ..extensions import db

comments = Blueprint('comments', __name__)


@comments.route('/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comentario = Comentario.query.get_or_404(comment_id)
    if comentario.autor != current_user:
        abort(403)

    db.session.delete(comentario)
    db.session.commit()

    flash('Comentário deletado', 'success')
    return redirect(request.referrer or url_for('views.home'))


@comments.route('/<int:comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(comment_id):
    comentario = Comentario.query.get_or_404(comment_id)
    if comentario.autor != current_user:
        abort(403)

    novo_conteudo = clean(request.form.get('conteudo'))
    comentario.conteudo = novo_conteudo
    comentario.ultima_atualizacao = datetime.now(timezone.utc)
    comentario.editado = True

    db.session.commit()

    return redirect(request.referrer or url_for('views.home'))
