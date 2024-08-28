from flask import Blueprint, abort, request, url_for, redirect, flash
from flask_login import login_required, current_user

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
