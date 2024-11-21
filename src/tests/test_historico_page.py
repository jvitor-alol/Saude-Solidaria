def test_historico_page(client):
    """Testa se a página do Histórico está sendo carregada corretamente e se os dados aparecem"""
    response = client.get('/historico')
    print(response.data.decode('utf-8'))  # Imprime o HTML da resposta para depuração
    
    # Verifica se a resposta tem status 200
    assert response.status_code == 200
    
    # Verifica se a página contém o título "Histórico"
    assert 'Histórico' in response.data.decode('utf-8')
    
    # Verifica se os dados de exemplo estão sendo exibidos
    assert '19/11/2024' in response.data.decode('utf-8')
    assert 'Exemplo de entrada no histórico' in response.data.decode('utf-8')
    assert '18/11/2024' in response.data.decode('utf-8')
    assert 'Outra entrada no histórico' in response.data.decode('utf-8')
