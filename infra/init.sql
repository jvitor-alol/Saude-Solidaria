START TRANSACTION;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    nome_usuario VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    cidade VARCHAR(100),
    estado VARCHAR(100),
    pais VARCHAR(100) DEFAULT 'Brasil',
    data_nascimento DATE,
    genero VARCHAR(20),
    foto_perfil TEXT, -- url da foto de perfil
    bio TEXT,
    data_registro TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'ativo',
    notificacoes BOOLEAN DEFAULT TRUE,
    tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'comum' -- 'comum' ou 'medico'
);

CREATE TABLE medicos (
    usuario_id INT PRIMARY KEY REFERENCES usuarios(id),
    crm VARCHAR(50) NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT NOT NULL,
	estrelas SMALLINT DEFAULT 0,
	num_votos INT DEFAULT 0,
    data_publicacao TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMPTZ,
    autor_id INT NOT NULL REFERENCES usuarios(id)
);

CREATE TABLE comentarios (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    estrelas SMALLINT DEFAULT 0,
	num_votos INT DEFAULT 0,
    data_comentario TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    autor_id INT NOT NULL REFERENCES usuarios(id),
    post_id INT NOT NULL REFERENCES posts(id)
);

CREATE TABLE favoritos (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id),
    post_id INT NOT NULL REFERENCES posts(id),
    data_adicao TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ler_mais_tarde (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id),
    post_id INT NOT NULL REFERENCES posts(id),
    data_adicao TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id),
    post_id INT NOT NULL REFERENCES posts(id),
    motivo TEXT NOT NULL,
	descricao TEXT,
    data_report TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indíces para otimizar consultas no banco de dados
CREATE INDEX idx_usuarios_nome_usuario ON usuarios (nome_usuario);
CREATE INDEX idx_usuarios_email ON usuarios (email);
CREATE INDEX idx_usuarios_tipo_usuario ON usuarios (tipo_usuario);
CREATE INDEX idx_medicos_crm ON medicos (crm);
CREATE INDEX idx_posts_autor_id ON posts (autor_id);
CREATE INDEX idx_posts_data_publicacao ON posts (data_publicacao);

COMMIT;