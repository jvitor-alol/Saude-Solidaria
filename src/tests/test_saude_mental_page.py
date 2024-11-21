def test_saude_mental_page(client):
    """Testa se a página sobre Saúde Mental está sendo carregada corretamente"""
    response = client.get('/saude_mental_info')
    print(response.data.decode('utf-8'))  # Imprime o HTML da resposta
    assert response.status_code == 200
    assert 'Saúde Mental' in response.data.decode('utf-8')

