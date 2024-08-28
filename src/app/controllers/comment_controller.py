from flask_login import current_user
from bleach import clean

from ..forms import CommentForm
from ..models import Comentario
from ..extensions import db


def new_comment_controller(form: CommentForm, post_id: int) -> None:
    clean_conteudo = clean(form.conteudo.data)

    comentario = Comentario(
        conteudo=clean_conteudo,
        autor_id=current_user.id,
        post_id=post_id
    )

    db.session.add(comentario)
    db.session.commit()
