from app.models import Post


def test_delete_post(logged_in_md, app):
    response = logged_in_md.post(
        '/post/new',
        data={
            'titulo': 'Post para Deletar',
            'categoria': 'clinica geral',
            'conteudo': 'Lorem ipsum'
        },
        follow_redirects=True
    )

    post = Post.query.filter_by(titulo='Post para Deletar').first()
    app.logger.info(post)

    assert post is not None

    # Exclui o post
    response = logged_in_md.post(
        f'/post/{post.id}/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Postagem deletada' in response.data
    assert b'Post para Deletar' not in response.data


def test_create_post(logged_in_md, app):
    response = logged_in_md.post(
        '/post/new',
        data={
            'titulo': 'Post de teste',
            'categoria': 'clinica geral',
            'conteudo': 'Lorem ipsum'
        },
        follow_redirects=True
    )

    post = Post.query.filter_by(titulo='Post de teste').first()
    app.logger.info(post)

    assert post is not None
    assert response.status_code == 200
    assert b'Post de teste' in response.data
