def test_delete_post(client, login):
    # Simulando o login
    login('test_user', 'test_password')
    
    # Crie um post
    client.post('/create_post', data=dict(
        title='Post para Deletar',
        content='Conteúdo'
    ), follow_redirects=True)

    # Exclua o post criado
    response = client.post('/delete_post/1', follow_redirects=True)

    # Verifique se o post foi deletado com sucesso
    assert response.status_code == 200
    assert b'Post para Deletar' not in response.data
