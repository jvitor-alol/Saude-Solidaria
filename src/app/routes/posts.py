from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Post
from ..forms import PostForm, CommentForm
from ..controllers import new_post_controller, new_comment_controller

posts = Blueprint('posts', __name__)


@posts.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.tipo_usuario == 'comum':
        return redirect(url_for('views.home'))

    form = PostForm()
    if form.validate_on_submit():
        new_post_controller(form)
        flash("Postagem criada com sucesso.", 'success')
        return redirect(url_for('views.home'))

    return render_template('edit_post.html', form=form)


@posts.route('/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Você precisa estar logado para comentar.', 'warning')
            return render_template('post.html', post=post, form=form)

        new_comment_controller(form=form, post_id=post_id)
        form.conteudo.data = ''  # Limpa o campo de texto

    return render_template('post.html', post=post, form=form)


@posts.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Postagem deletada', 'success')
    return redirect(url_for('views.home'))
