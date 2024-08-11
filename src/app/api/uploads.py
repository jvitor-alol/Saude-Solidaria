import os

from flask import jsonify, request
from werkzeug.utils import secure_filename

from api import api
from .utils import allowed_file


@api.route('/upload', methods=['POST'])
def upload_image():
    raise NotImplementedError

    # TODO: Criar a lógica de upload de imagens para o S3
    if 'image' not in request.files:
        return (
            jsonify({'error': 'Nenhum arquivo encontrado na requisição'}),
            400)

    file = request.files['image']
    if file.filename == '':
        return (jsonify({'error': 'Nenhum arquivo selecionado'}), 400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(api.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return (
            jsonify({'message': f'Imagem {filename} enviada com sucesso!'}),
            200)

    return (jsonify({'error': 'Tipo de arquivo inválido'}), 400)
