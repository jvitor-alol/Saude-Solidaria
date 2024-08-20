import os
import secrets
from typing import Any

from flask import url_for
from PIL import Image

from ..config import BASE_DIR

TEMP_IMAGES_DIR = 'images/tmp'
TEMP_IMAGES_DIR_ABS = os.path.join(BASE_DIR, 'static', TEMP_IMAGES_DIR)


def salvar_imagem_temporario(form_picture: Any) -> str:
    random_hex = secrets.token_hex(8)
    extensao_arquivo = os.path.splitext(form_picture.filename)[1]

    temp_file_name = os.path.join(
        TEMP_IMAGES_DIR, (random_hex + extensao_arquivo))
    temp_file_path = os.path.join(BASE_DIR, 'static', temp_file_name)

    if not os.path.exists(TEMP_IMAGES_DIR_ABS):
        os.mkdir(TEMP_IMAGES_DIR_ABS)

    # Redimensiona a imagem antes de salvar
    tamanho_max = (500, 500)
    imagem = Image.open(form_picture)
    imagem.thumbnail(tamanho_max)
    imagem.save(temp_file_path)

    return url_for('static', filename=temp_file_name)

# TODO: Criar a lógica de upload de imagens para o S3
