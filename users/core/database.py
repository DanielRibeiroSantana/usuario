"""Configuração de conexão com banco de dados.

Este módulo define:
- Engine do SQLAlchemy (conexão com banco)
- SessionLocal (gerenciador de sessões)
- Base (classe base para modelos ORM)
- get_db (dependency injection para FastAPI)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

# Cria a engine do SQLAlchemy para conectar ao banco de dados
# echo=True exibe todas as queries SQL (remover em produção)
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal é a factory para criar novas sessões de banco de dados
# autocommit=False: transações precisam ser commitadas explicitamente
# autoflush=False: objetos não são salvos automaticamente
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe base para todos os modelos ORM
# Todos os modelos herdam dessa classe
Base = declarative_base()


def get_db():
    """Dependency injection para obter sessão de banco de dados.
    
    FastAPI usa essa função para injetar uma sessão de banco
    em cada requisição. A sessão é fechada automaticamente
    após a requisição ser processada.
    
    Yields:
        SessionLocal: Sessão ativa do banco de dados
    """
    db = SessionLocal()

    try:
        # Fornece a sessão para o endpoint
        yield db
    finally:
        # Garante que a sessão é fechada mesmo em caso de erro
        db.close()
