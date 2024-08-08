import os
import secrets
from typing import Any

from ..config import BASE_DIR

TEMP_IMAGES_DIR = 'static/images/tmp'
TEMP_IMAGES_DIR_ABS = os.path.join(BASE_DIR, TEMP_IMAGES_DIR)


def salvar_imagem_temporario(form_picture: Any) -> str:
    random_hex = secrets.token_hex(8)
    file_extension = os.path.splitext(form_picture.filename)[1]

    temp_file_name = os.path.join(
        TEMP_IMAGES_DIR, (random_hex + file_extension))
    temp_file_path = os.path.join(BASE_DIR, temp_file_name)

    if not os.path.exists(TEMP_IMAGES_DIR_ABS):
        os.mkdir(TEMP_IMAGES_DIR_ABS)

    form_picture.save(temp_file_path)
    return temp_file_name

# TODO: Criar a lógica de upload de imagens para o S3
