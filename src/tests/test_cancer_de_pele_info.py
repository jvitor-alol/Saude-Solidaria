import pytest

def test_cancer_de_pele_info_route(client):
    response = client.get('/cancer_de_pele_info')
    assert response.status_code == 200
    assert b"Cancer de Pele" in response.data
    assert b"Sintomas e Sinais" in response.data
    assert b"Proteja-se e cuide da sua pele!" in response.data
