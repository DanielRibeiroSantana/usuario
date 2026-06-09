# User Management API

Uma API REST para gerenciamento de usuários construída com **FastAPI** e **SQLAlchemy**, seguindo as melhores práticas de segurança e estrutura de código profissional.

## 🚀 Características

- ✅ **FastAPI** - Framework web moderno e de alto desempenho
- ✅ **SQLAlchemy ORM** - Mapeamento objeto-relacional para banco de dados
- ✅ **PostgreSQL** - Banco de dados robusto
- ✅ **Variáveis de Ambiente** - Gerenciamento seguro de credenciais
- ✅ **Validação de Dados** - Com Pydantic
- ✅ **Documentação Automática** - Swagger/OpenAPI
- ✅ **Estrutura Modular** - Código organizado e escalável

## 📁 Estrutura do Projeto

```
users/
├── main.py                 # Aplicação principal do FastAPI
├── pyproject.toml         # Configuração de dependências (Poetry)
├── .env                   # Variáveis de ambiente (não commitado)
├── .env.example          # Template de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── api/
│   ├── __init__.py
│   └── users.py          # Rotas da API REST
├── core/
│   ├── __init__.py
│   ├── config.py         # Configurações (variáveis de ambiente)
│   └── database.py       # Conexão com banco de dados
├── models/
│   ├── __init__.py
│   └── user.py           # Modelo ORM do usuário
├── schemas/
│   ├── __init__.py
│   └── user.py           # Schemas Pydantic para validação
├── services/
│   ├── __init__.py
│   └── user_service.py   # Lógica de negócio para usuários
└── tests/
    └── __init__.py
```

## 🔧 Instalação

### Pré-requisitos

- Python 3.13+
- Poetry
- PostgreSQL

### Passos

1. **Clone o repositório:**

```bash
git clone https://github.com/DanielRibeiroSantana/usuario.git
cd usuario/users
```

2. **Instale as dependências:**

```bash
poetry install
```

3. **Configure as variáveis de ambiente:**

```bash
cp .env.example .env
# Edite .env com suas credenciais PostgreSQL
```

4. **Execute o servidor:**

```bash
poetry run task run
```

O servidor estará disponível em: `http://127.0.0.1:8000`

## 📚 Endpoints da API

### Criar Usuário

```http
POST /users/
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

### Listar Todos os Usuários

```http
GET /users/
```

### Obter Usuário por ID

```http
GET /users/{user_id}
```

### Atualizar Usuário

```http
PUT /users/{user_id}
Content-Type: application/json

{
  "name": "João Silva Atualizado",
  "email": "joao_novo@example.com"
}
```

### Deletar Usuário

```http
DELETE /users/{user_id}
```

## 📖 Documentação Interativa

Acesse a documentação do Swagger em:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## 🔐 Segurança

- ✅ **Credenciais em Variáveis de Ambiente** - Não há hardcoding de senhas
- ✅ **.gitignore** - Arquivos sensíveis (.env) não são commitados
- ✅ **.env.example** - Template para configuração segura
- ✅ **Validação de Email** - Com Pydantic EmailStr
- ✅ **ORM** - Proteção contra SQL Injection

## 🏗️ Arquitetura

A aplicação segue o padrão de camadas (Layered Architecture):

1. **API Layer** (`api/users.py`)

   - Define os endpoints REST
   - Recebe requisições HTTP e retorna respostas
2. **Service Layer** (`services/user_service.py`)

   - Implementa a lógica de negócio
   - Realiza operações CRUD
3. **Data Layer** (`models/user.py`, `core/database.py`)

   - Define o modelo ORM
   - Gerencia a conexão com banco de dados
4. **Schema Layer** (`schemas/user.py`)

   - Define estruturas de dados
   - Valida entrada e saída de dados

## 📋 Tecnologias Usadas

| Tecnologia    | Versão   | Propósito             |
| ------------- | --------- | ---------------------- |
| FastAPI       | >=0.136.3 | Framework web          |
| SQLAlchemy    | >=2.0.50  | ORM                    |
| PostgreSQL    | Latest    | Banco de dados         |
| Pydantic      | Builtin   | Validação de dados   |
| python-dotenv | >=1.2.2   | Variáveis de ambiente |

## 🧪 Testes

Para executar testes:

```bash
poetry run pytest
```

## 📝 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

**Daniel Ribeiro**

- Email: daniel.obpc@outlook.com
- GitHub: [@DanielRibeiroSantana](https://github.com/DanielRibeiroSantana)

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou crie um pull request.
