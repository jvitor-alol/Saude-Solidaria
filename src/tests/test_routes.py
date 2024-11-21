def test_dengue_route(client):
    response = client.get('/dengue')
    assert response.status_code == 200
