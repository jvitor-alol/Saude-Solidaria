def test_aids_page(client):
    """Testa se a página sobre AIDS está sendo carregada corretamente"""
    response = client.get('/aids_info')
    assert response.status_code == 200
    assert b'Sobre a AIDS' in response.data
