"""Aplicação principal do FastAPI.

Este módulo inicializa a aplicação FastAPI e configura:
- Importação de rotas da API
- Criação de tabelas no banco de dados
- Metadados da aplicação
"""
from fastapi import FastAPI
from .api.users import router as users_router
from .core.database import Base, engine

# Cria todas as tabelas no banco de dados (se não existirem)
# Base contém todos os modelos ORM definidos
Base.metadata.create_all(bind=engine)

# Instancia a aplicação FastAPI com metadados
app = FastAPI(
    title='User Management API',
    description='API para gerenciamento de usuários',
    version='1.0.0',
)

# Inclui todas as rotas de usuários no app
# O prefixo '/users' é definido no router
app.include_router(users_router)


@app.get('/')
def health_check():

    return {'status': 'online'}
