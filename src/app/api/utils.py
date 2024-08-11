import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    """Função para verificar extensões de arquivo permitidas"""
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS
