"""Schemas Pydantic para validação de dados.

Estes schemas definem a estrutura de dados esperada
para requisições e respostas da API.
Pydantic automaticamente valida e serializa os dados.
"""
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema para criação de um novo usuário.
    
    Atributos:
        name: Nome do usuário (string)
        email: Email válido do usuário (validado pelo Pydantic)
        password: Senha do usuário (string)
    """
    name: str
    email: EmailStr  # EmailStr valida automaticamente o formato do email
    password: str


class UserUpdate(BaseModel):
    """Schema para atualizar um usuário existente.
    
    Atributos:
        name: Novo nome do usuário
        email: Novo email do usuário
    
    Nota: Password não é atualizado por esta rota
    """
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    """Schema para resposta de um usuário (leitura).
    
    Atributos:
        id: Identificador único do usuário
        name: Nome do usuário
        email: Email do usuário
    
    Config:
        from_attributes: Permite converter objetos ORM para dict
    """
    id: int
    name: str
    email: EmailStr

    class Config:
        # from_attributes=True permite que Pydantic leia
        # atributos de objetos ORM (models.User)
        from_attributes = True
