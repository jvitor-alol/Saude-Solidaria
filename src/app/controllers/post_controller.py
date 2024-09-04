from flask_login import current_user
from flask_ckeditor.utils import cleanify
from bleach import clean

from ..extensions import db
from ..models import Post
from ..forms import PostForm


def new_post_controller(form: PostForm) -> Post:
    titulo = clean(form.titulo.data)
    categoria = form.categoria.data
    conteudo = cleanify(form.conteudo.data)

    nova_postagem = Post(
        titulo=titulo,
        conteudo=conteudo,
        categoria=categoria,
        autor_id=current_user.id
    )

    db.session.add(nova_postagem)
    db.session.commit()

    return nova_postagem
