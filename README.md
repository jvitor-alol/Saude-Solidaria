# Projeto Integrador IV

<p align="center">
  <h1 align="center"> 
	⚕️ Saúde Solidária ⚕️
  </h1>
</p>

<p align="center">
 <img alt="Status Em Desenvolvimento" src="https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-orange">
</p>

<p align="center">
 <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/jvitor-alol/Saude-Solidaria?color=%2304D361">
 <img alt="Repository size" src="https://img.shields.io/github/repo-size/jvitor-alol/Saude-Solidaria"> 
 <a href="https://github.com/jvitor-alol/Saude-Solidaria/commits/main/">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/jvitor-alol/Saude-Solidaria">
 </a>
</p>

<p align="center">
 <a href="#-sobre-o-projeto">Sobre</a> •
 <a href="#-objetivo-do-projeto">Objetivo</a> •	
 <a href="#-Pré-Requisitos">Pré-Requisitos</a> •
 <a href="#-Banco de Dados">Banco de Dados</a> • 
 <a href="#-como-executar-o-projeto">Como executar</a> • 
 <a href="#-contribuidores">Contribuidores</a> 

</p>

## 💻 Sobre o projeto
  Projeto sendo desenvolvido por estudantes de graduação em Análise e Desenvolvimento de Sistemas pelo SENAC.

## 🔘 Objetivo do projeto
  Temos visto que a saúde preventiva tornou-se uma preocupação global devido a pandemia, o medo de uma nova doença desconhecida está na mente da população. Este projeto visa criar uma ferramenta que ofereça ampla e unificada informação e conscientização sobre saúde preventiva, sem discriminação de idade e gênero. Sendo sáude física ou mental, devemos nos cuidar diariamente, nosso projeto mostrará ao indivíduo como cuidar de si da melhor forma.


## 🎨 Layout

O layout da aplicação está disponível no Figma:

<a href="https://www.figma.com/files/project/77994470/%F0%9F%93%84-Templates-para-Projetos%2C-Eventos-e-Cursos?fuid=1110596132085818429">
  <img alt="Made by Cubos Academy" src="https://img.shields.io/badge/Acessar%20Layout%20-Figma-%2304D361">
</a>


## Banco de Dados
   <img src="MER.jpeg" width="700px"/>

### Usuários e Médicos:

Relacionamento: 1:1
 
Justificativa: Um usuário pode ser um médico, mas um médico é um usuário. Cada registro na tabela usuarios pode ter, no máximo, um registro correspondente na tabela medicos, e vice-versa.
 
### Usuários e Posts:

Relacionamento: 1

Justificativa: Um usuário pode criar vários posts, mas cada post é criado por um único usuário.

### Posts e Comentários:

Relacionamento: 1

Justificativa: Um post pode ter muitos comentários, mas cada comentário pertence a um único post.

### Usuários e Comentários:

Relacionamento: 1

Justificativa: Um usuário pode escrever muitos comentários, mas cada comentário é escrito por um único usuário.

### Usuários e Favoritos:

Relacionamento: 1

Justificativa: Um usuário pode adicionar vários posts aos favoritos, mas cada entrada nos favoritos está associada a um único usuário.

### Usuários e Ler_mais_tarde:

Relacionamento: 1

Justificativa: Um usuário pode adicionar vários posts à lista de leitura para depois, mas cada entrada na lista de leitura está associada a um único usuário.

### Usuários e Reports:

Relacionamento: 1

Justificativa: Um usuário pode fazer várias denúncias (reports), mas cada denúncia é feita por um único usuário.

### Posts e Favoritos, Ler mais tarde e Reports:

Relacionamento: 1

Justificativa: Cada post pode ser favoritado, adicionado à lista de leitura ou denunciado por vários usuários.

### Favoritos, Ler mais tarde, Reports:

Relacionamento: n

Justificativa: Um usuário pode favoritar, salvar para ler depois ou reportar múltiplos posts, e cada post pode ser favoritado, salvo ou reportado por múltiplos usuários.


## Script

```env
CREATE TABLE usuarios (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  sobrenome VARCHAR(255) NOT NULL,
  nome_usuario VARCHAR(100) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  telefone VARCHAR(20),
  cidade VARCHAR(100),
  estado VARCHAR(100),
  pais VARCHAR(100) DEFAULT 'Brasil',
  data_nascimento DATE,
  genero VARCHAR(20),
  foto_perfil TEXT NOT NULL,
  bio TEXT,
  data_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultimo_login DATETIME,
  status VARCHAR(20) DEFAULT 'ativo',
  notificacoes BOOLEAN DEFAULT TRUE,
  tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'comum',
  PRIMARY KEY (id)
);

CREATE TABLE medicos (
  usuario_id INT NOT NULL,
  crm VARCHAR(50) NOT NULL,
  especialidade VARCHAR(100) NOT NULL,
  PRIMARY KEY (usuario_id),
  CONSTRAINT fk_medicos_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

CREATE TABLE posts (
  id INT NOT NULL AUTO_INCREMENT,
  titulo VARCHAR(255) NOT NULL,
  conteudo TEXT NOT NULL,
  estrelas SMALLINT DEFAULT 0,
  num_votos INT DEFAULT 0,
  data_publicacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultima_atualizacao DATETIME,
  autor_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_posts_usuarios FOREIGN KEY (autor_id) REFERENCES usuarios (id)
);

CREATE TABLE comentarios (
  id INT NOT NULL AUTO_INCREMENT,
  texto TEXT NOT NULL,
  estrelas SMALLINT DEFAULT 0,
  num_votos INT DEFAULT 0,
  data_comentario DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  autor_id INT NOT NULL,
  post_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_comentarios_usuarios FOREIGN KEY (autor_id) REFERENCES usuarios (id),
  CONSTRAINT fk_comentarios_posts FOREIGN KEY (post_id) REFERENCES posts (id)
);

CREATE TABLE favoritos (
  id INT NOT NULL AUTO_INCREMENT,
  usuario_id INT NOT NULL,
  post_id INT NOT NULL,
  data_adicao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_favoritos_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
  CONSTRAINT fk_favoritos_posts FOREIGN KEY (post_id) REFERENCES posts (id)
);

CREATE TABLE ler_mais_tarde (
  id INT NOT NULL AUTO_INCREMENT,
  usuario_id INT NOT NULL,
  post_id INT NOT NULL,
  data_adicao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_ler_mais_tarde_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
  CONSTRAINT fk_ler_mais_tarde_posts FOREIGN KEY (post_id) REFERENCES posts (id)
);

CREATE TABLE reports (
  id INT NOT NULL AUTO_INCREMENT,
  usuario_id INT NOT NULL,
  post_id INT NOT NULL,
  motivo TEXT NOT NULL,
  descricao TEXT,
  data_report DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_reports_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
  CONSTRAINT fk_reports_posts FOREIGN KEY (post_id) REFERENCES posts (id)
);
```
## ⚙️ Pré-Requisitos
  - [Docker](https://docs.docker.com/guides/getting-started/)
  - [Docker Compose](https://docs.docker.com/compose/)

## 🛣️ Como executar o projeto
- Clone o repositório
- Crie um arquivo .env na raíz do repositório com as seguintes variáveis de ambiente configuradas (modifique usuários, senhas e chaves de acordo):

  ```env
  FLASK_APP=run.py
  FLASK_CONFIG=production
  SECRET_KEY=<flask-secret-key>
  POSTGRES_USER=flask_app
  PGUSER=${POSTGRES_USER}
  POSTGRES_PASSWORD=<super-secret-password>
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  POSTGRES_DB=saude_solidaria
  DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
  PGADMIN_DEFAULT_EMAIL=<admin@pgadmin.com>
  PGADMIN_DEFAULT_PASSWORD=<password>
  TZ=America/Sao_Paulo
  ```
  
- Dentro de `/deploy` execute o Docker Compose com

```bash
docker compose up -d
```

Acesse o web GUI a partir da porta mapeada no host em `http://localhost:8888/`.


## Colaboradores

<div align="center">
    <table style="width: 100%; border-collapse: collapse; text-align: center;">
    <tr>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/74667067?v=4" alt="jvitor-alol" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/jvitor-alol" target="_blank"><p>jvitor-alol</p></a>
        </td>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/85653011?v=4" alt="Lynn-Noob" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/Lynn-Noob" target="_blank"><p>Lynn-Noob</p></a>
        </td>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/95151247?v=4" alt="Guilherme-Soares05" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/Guilherme-Soares05" target="_blank"><p>Guilherme-Soares05</p></a>
        </td>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/94906196?v=4" alt="Rosicre" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/Rosicre" target="_blank"><p>Rosicre</p></a>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/142458518?v=4" alt="mirelaads" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/mirelaads" target="_blank"><p>mirelaads</p></a>
        </td>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/102329062?v=4" alt="medinaandre" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/medinaandre" target="_blank"><p>medinaandre</p></a>
        </td>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/86894587?v=4" alt="dkexs" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/dkexs" target="_blank"><p>dkexs</p></a>
        </td>
        <td style="padding: 20px; border: 1px solid #ddd; vertical-align: middle;">
            <img src="https://avatars.githubusercontent.com/u/60987344?v=4" alt="PedroBrito22" style="display: block; margin: 0 auto; width: 100px; height: 100px;">
            <a href="https://github.com/PedroBrito22" target="_blank"><p>PedroBrito22</p></a>
        </td>
    </tr>
  </table>
</div>

