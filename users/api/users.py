from ..core.database import get_db
from ..schemas.user import UserCreate, UserUpdate
from ..services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/')
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create(db, user)


@router.get('/')
def list_users(db: Session = Depends(get_db)):
    return UserService.get_all(db)


@router.get('/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = UserService.get_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return user


@router.put('/{user_id}')
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):

    updated_user = UserService.update(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return updated_user


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):

    deleted_user = UserService.delete(db, user_id)

    if not deleted_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return {'message': 'Usuário removido com sucesso'}
