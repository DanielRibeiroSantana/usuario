"""Modelo ORM para a tabela de usuários.

Este módulo define a classe User que representa
a tabela 'users' no banco de dados PostgreSQL.
"""
from ..core.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func


class User(Base):
    """Modelo ORM para usuários.
    
    Atributos:
        id: Identificador único (chave primária)
        name: Nome completo do usuário (até 100 caracteres)
        email: Email único do usuário (até 255 caracteres)
        password: Senha criptografada do usuário
        created_at: Data e hora de criação (preenchida automaticamente)
    """
    # Nome da tabela no banco de dados
    __tablename__ = 'users'
    
    # Define o schema PostgreSQL (namespace) para a tabela
    __table_args__ = {'schema': 'users'}

    # Coluna ID: chave primária com índice automático
    id = Column(Integer, primary_key=True, index=True)
    
    # Coluna NAME: string até 100 caracteres, obrigatória
    name = Column(String(100), nullable=False)
    
    # Coluna EMAIL: string até 255 caracteres, única (sem duplicatas), obrigatória
    email = Column(String(255), unique=True, nullable=False)
    
    # Coluna PASSWORD: string até 255 caracteres, obrigatória
    password = Column(String(255), nullable=False)
    
    # Coluna CREATED_AT: data/hora com valor padrão (agora)
    # server_default=func.now() define a data no banco de dados
    created_at = Column(DateTime, server_default=func.now())
