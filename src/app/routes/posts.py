from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from ..forms import PostForm
from ..controllers import new_post_controller

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

    return render_template('post.html', form=form)
