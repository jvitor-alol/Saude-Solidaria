from flask import redirect, url_for, Response
from flask_login import current_user
from flask_ckeditor.utils import cleanify
from bleach import clean

from .helpers import validar_autor_post
from ..extensions import db
from ..models import Post
from ..forms import PostForm
from ..controllers import salvar_imagem_temporario

ALLOWED_TAGS = [
    'a', 'abbr', 'b', 'blockquote', 'code',
    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img', 'span'
]


def new_post_controller(form: PostForm) -> Post:
    titulo = clean(form.titulo.data)
    categoria = form.categoria.data
    conteudo = cleanify(form.conteudo.data, allow_tags=ALLOWED_TAGS)

    nova_postagem = Post(
        titulo=titulo,
        conteudo=conteudo,
        categoria=categoria,
        autor_id=current_user.id
    )

    if form.foto_cover.data:
        cover = salvar_imagem_temporario(form.foto_cover.data, resize=False)
        nova_postagem.foto_cover = cover

    db.session.add(nova_postagem)
    db.session.commit()

    return nova_postagem


def delete_post_controller(post_id: int) -> None:
    post = validar_autor_post(post_id)

    db.session.delete(post)
    db.session.commit()


def edit_post_controller(post_id: int, form: PostForm) -> Response:
    post = validar_autor_post(post_id)

    post.titulo = clean(form.titulo.data)
    post.categoria = form.categoria.data
    post.conteudo = cleanify(form.conteudo.data, allow_tags=ALLOWED_TAGS)

    if form.foto_cover.data:
        cover = salvar_imagem_temporario(form.foto_cover.data, resize=False)
        post.foto_cover = cover

    db.session.commit()

    return redirect(url_for('posts.view_post', post_id=post.id))


def get_post_data(post_id: int, form: PostForm) -> None:
    post = validar_autor_post(post_id)

    form.titulo.data = post.titulo
    form.categoria.data = post.categoria
    form.conteudo.data = post.conteudo
