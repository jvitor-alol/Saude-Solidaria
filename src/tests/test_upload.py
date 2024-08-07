import os
import json

def test_register_user(client, app):
    # Exemplo de teste simples para garantir que o ambiente de teste está configurado
    assert 1 == 1

def test_upload_image(client, logged_in_client):
    # Teste para fazer upload de uma imagem
    image_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'images', 'image.png')
    assert os.path.exists(image_path), f"Image not found at {image_path}"
    
    with open(image_path, 'rb') as img:
        data = {
            'image': img
        }
        response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        
        # Verifique se a imagem foi salva corretamente no servidor
        response_json = json.loads(response.data.decode('utf-8'))
        assert 'success' in response_json
        assert 'image.png' in response_json['success']
