"""Configurações da aplicação.

Este módulo carrega as variáveis de ambiente e define
configurações como a URL do banco de dados.

Variáveis de ambiente são carregadas do arquivo .env
"""
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

# URL de conexão com o banco PostgreSQL
# É carregada de uma variável de ambiente por segurança
# Caso não exista, usa um padrão local
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://localhost/user_api'
)
