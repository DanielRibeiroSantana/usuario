"""Rotas da API REST para gerenciar usuários.

Este módulo define todos os endpoints HTTP para CRUD de usuários.
Cada função é decorada com @router.get(), @router.post(), etc.
para definir o método HTTP e o caminho.
"""
from ..core.database import get_db
from ..schemas.user import UserCreate, UserUpdate
from ..services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Cria um router com prefixo '/users' para todas as rotas
# tags=['Users'] agrupa as rotas na documentação Swagger
router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/')
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Depends(get_db) injeta uma sessão de banco que é fechada
    # automaticamente após a requisição
    return UserService.create(db, user)


@router.get('/')
def list_users(db: Session = Depends(get_db)):

    return UserService.get_all(db)


@router.get('/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):

    # Busca o usuário no banco
    user = UserService.get_by_id(db, user_id)

    # Se não encontrar, retorna erro 404
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return user


@router.put('/{user_id}')
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):

    # Atualiza o usuário no banco
    updated_user = UserService.update(db, user_id, user)

    # Se usuário não existe, retorna erro 404
    if not updated_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return updated_user


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):

    # Deleta o usuário do banco
    deleted_user = UserService.delete(db, user_id)

    # Se usuário não existe, retorna erro 404
    if not deleted_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return {'message': 'Usuário removido com sucesso'}
