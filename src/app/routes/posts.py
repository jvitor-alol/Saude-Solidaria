from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from ..models import Post
from ..forms import PostForm, CommentForm
from ..controllers import new_post_controller, new_comment_controller
from ..controllers import delete_post_controller, get_post_data
from ..controllers import edit_post_controller

posts = Blueprint('posts', __name__)


@posts.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.tipo_usuario == 'comum':
        return redirect(url_for('views.home'))

    title = h1 = 'Nova Postagem'

    form = PostForm()
    if form.validate_on_submit():
        post = new_post_controller(form)
        flash("Postagem criada.", 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))

    return render_template('edit_post.html', form=form, title=title, h1=h1)


@posts.route('/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.titulo
    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Você precisa estar logado para comentar.', 'warning')
            return render_template('post.html', post=post, form=form)

        new_comment_controller(form=form, post_id=post_id)
        form.conteudo.data = ''  # Limpa o campo de texto

    return render_template('post.html', post=post, form=form, title=title)


@posts.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    delete_post_controller(post_id)

    flash('Postagem deletada', 'success')
    return redirect(url_for('views.home'))


@posts.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    title = h1 = 'Editar Postagem'

    if form.validate_on_submit():
        return edit_post_controller(post_id, form)
    elif request.method == 'GET':
        get_post_data(post_id, form)

    return render_template('edit_post.html', form=form, title=title, h1=h1)
