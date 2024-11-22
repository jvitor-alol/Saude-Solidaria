import pytest

def test_campanha_do_sono_info_route(client):
    response = client.get('/campanha_do_sono_info')
    assert response.status_code == 200
    assert b"Informa\xc3\xa7\xc3\xb5es: Campanha do Sono" in response.data  # "Informações: Campanha do Sono"
    assert b"Por Que Dormimos?" in response.data
    assert b"Curiosidades sobre o Sono" in response.data
    assert b"Pratique uma Boa Higiene do Sono!" in response.data
