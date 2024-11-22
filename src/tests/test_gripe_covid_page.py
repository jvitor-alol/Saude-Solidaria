def test_gripe_covid_page(client):
    """Testa se a página sobre Gripe e COVID-19 está sendo carregada corretamente"""
    response = client.get('/gripe-covid')
    print(response.data.decode('utf-8'))  # Imprime o HTML da resposta para debugging
    assert response.status_code == 200
    assert 'Gripe e COVID-19' in response.data.decode('utf-8')
