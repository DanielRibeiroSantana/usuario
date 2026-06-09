# Guia de Arquitetura - User Management API

## 🏗️ Padrão de Arquitetura: Layered Architecture (Camadas)

Este projeto segue o padrão de **Arquitetura em Camadas**, que separa responsabilidades em diferentes níveis:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│              (FastAPI Routers - api/users.py)              │
│  Responsável por: Requisições HTTP, Respostas, Validação  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVICE LAYER                             │
│          (Business Logic - services/user_service.py)        │
│  Responsável por: CRUD, Lógica de Negócio, Regras         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                        │
│    (ORM Models - models/user.py, Database - core/)         │
│  Responsável por: Banco de Dados, Queries, Transações      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Fluxo de uma Requisição

```
1. Cliente (Postman/Browser)
   │
   ├─► POST /users/ { name, email, password }
   │
   └──────► FastAPI Router (api/users.py)
            │
            ├─► Validação com Pydantic (schemas/user.py)
            │   → EmailStr valida o email automaticamente
            │   → Strings validadas (não vazias)
            │
            └──────► UserService.create() (services/user_service.py)
                     │
                     ├─► Cria instância User (models/user.py)
                     │   → Prepara dados para banco
                     │
                     └──────► SQLAlchemy ORM
                              │
                              ├─► db.add(user)      # Prepara
                              ├─► db.commit()       # Salva no BD
                              ├─► db.refresh(user)  # Recarrega
                              │
                              └──────► PostgreSQL
                                       │
                                       └─► INSERT INTO users VALUES (...)
                                           └─► RETORNA ID GERADO
                     │
                     ├─► Retorna objeto User com ID
                     │
                     └──────► Router converte para JSON
                              │
                              └──────► Resposta 200 OK + JSON
```

## 🔄 Padrão Dependency Injection

FastAPI usa **Dependency Injection** para gerenciar a sessão do banco:

```python
# Em api/users.py
@router.get('/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    #                                          ↑↑↑
    #  O FastAPI automaticamente chama get_db()
    #  e injeta a sessão nesta função
    return UserService.get_by_id(db, user_id)
```

**Benefícios:**
- ✅ Gerenciamento automático de sessões
- ✅ Conexão fechada após a requisição
- ✅ Sem vazamento de recursos
- ✅ Fácil de testar (pode mockar)

## 🗂️ Responsabilidade de Cada Camada

### 1️⃣ **Presentation Layer** (api/users.py)
```python
# Responsabilidades:
✓ Definir endpoints HTTP
✓ Validar entrada com Depends(get_db)
✓ Tratar erros HTTP (404, 500, etc)
✓ Retornar respostas JSON

# Não faz:
✗ Lógica complexa de negócio
✗ Queries diretas ao banco
✗ Manipulação de banco
```

### 2️⃣ **Service Layer** (services/user_service.py)
```python
# Responsabilidades:
✓ Implementar CRUD
✓ Validar regras de negócio
✓ Orquestrar operações
✓ Usar models e schemas

# Não faz:
✗ Retornar respostas HTTP
✗ Acessar http direto
✗ Lógica específica de rotas
```

### 3️⃣ **Data Access Layer** (models/user.py, core/database.py)
```python
# Responsabilidades:
✓ Definir modelo ORM
✓ Gerenciar conexão com BD
✓ Transações (commit/rollback)
✓ Queries genéricas

# Não faz:
✗ Regras de negócio
✗ Validação de dados
✗ Formatação de respostas
```

## 💾 Fluxo de Dados (CRUD)

### CREATE (POST /users/)
```
UserCreate Schema
    ↓ (validado)
UserService.create()
    ↓
models.User (instância)
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL INSERT
    ↓
User com ID gerado
```

### READ (GET /users/{id})
```
URL Parameter: user_id
    ↓
UserService.get_by_id()
    ↓
SQLAlchemy Query
    ↓
PostgreSQL SELECT
    ↓
models.User (recuperado)
    ↓
UserResponse Schema (convertido)
```

### UPDATE (PUT /users/{id})
```
UserUpdate Schema + URL ID
    ↓ (validado)
UserService.update()
    ↓
Busca User existente
    ↓
Modifica atributos
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL UPDATE
    ↓
User atualizado (refresh)
```

### DELETE (DELETE /users/{id})
```
URL Parameter: user_id
    ↓
UserService.delete()
    ↓
Busca User
    ↓
SQLAlchemy Delete
    ↓
PostgreSQL DELETE
    ↓
User deletado (retorna para confirmação)
```

## 🔐 Segurança por Camada

```
┌─────────────────────────────────────────┐
│ Presentation                            │
│ ✓ Validação de entrada (Pydantic)      │
│ ✓ Tratamento de exceções               │
│ ✓ Status codes HTTP corretos           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Service                                 │
│ ✓ Validação de regras de negócio       │
│ ✓ Verificação de existência (404)       │
│ ✓ Transações atômicas                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Data Access                             │
│ ✓ ORM protege contra SQL Injection      │
│ ✓ Prepared Statements automáticas       │
│ ✓ Constraint do BD (unique email)       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Configuration                           │
│ ✓ Credenciais em .env (não em código)   │
│ ✓ .gitignore protege .env               │
│ ✓ .env.example como template            │
└─────────────────────────────────────────┘
```

## 📊 Exemplo Completo: Criar Usuário

### 1. Request
```http
POST http://127.0.0.1:8000/users/
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

### 2. FastAPI Valida (Pydantic)
```python
# schemas/user.py - UserCreate
class UserCreate(BaseModel):
    name: str  # ✓ String não vazia
    email: EmailStr  # ✓ Formato válido de email
    password: str  # ✓ String não vazia
```

### 3. Service Layer
```python
# services/user_service.py
user = User(name='João Silva', email='joao@example.com', password='senha123')
db.add(user)
db.commit()
db.refresh(user)
# Agora user.id existe (gerado pelo BD)
```

### 4. SQLAlchemy ORM
```python
# Converte para SQL:
INSERT INTO users.users (name, email, password)
VALUES ('João Silva', 'joao@example.com', 'senha123')
RETURNING id;
```

### 5. PostgreSQL Executa
```sql
-- Verifica constraints:
-- - email UNIQUE (não pode repetir)
-- - name NOT NULL
-- - email NOT NULL

-- Se tudo ok, insere e retorna ID
-- Se erro, faz ROLLBACK automático
```

### 6. Response
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com"
}
```

## ✅ Vantagens dessa Arquitetura

| Vantagem | Benefício |
|----------|-----------|
| **Separação de Responsabilidades** | Código mais limpo e fácil de manter |
| **Testabilidade** | Fácil mockar dependências e testar cada camada |
| **Reutilização** | UserService pode ser usado em diferentes rotas |
| **Escalabilidade** | Fácil adicionar novas features sem quebrar existentes |
| **Segurança** | Validação em múltiplos níveis |
| **Performance** | ORM otimiza queries automáticas |

## 🧪 Como Testar Cada Camada

```python
# Teste de Schema (Pydantic)
from schemas.user import UserCreate

user = UserCreate(name='João', email='joao@test.com', password='123')
# ✓ Pasa
# ✗ Falha se email inválido

# Teste de Service
from services.user_service import UserService

user = UserService.create(db, user_data)
assert user.id is not None
# ✓ Verifica se ID foi gerado

# Teste de API
from fastapi.testclient import TestClient

response = client.post('/users/', json={...})
assert response.status_code == 200
# ✓ Testa endpoint completo
```

---

**Resumo:** Essa arquitetura em camadas permite que você explique cada responsabilidade claramente durante uma entrevista, mostrando compreensão de boas práticas de engenharia de software! 🚀
