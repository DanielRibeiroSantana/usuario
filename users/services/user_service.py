"""Serviço de lógica de negócio para usuários.

Este módulo implementa as operações CRUD (Create, Read, Update, Delete)
para a entidade User. As funções aqui separão a lógica de negócio
das rotas HTTP.
"""
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class UserService:

    @staticmethod
    def create(db: Session, user_data: UserCreate):

        # Cria uma nova instância do modelo User com os dados recebidos
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
        )

        # Adiciona o novo usuário à sessão (ainda não foi salvo no BD)
        db.add(user)
        
        # Confirma a transação e salva o usuário no banco
        db.commit()
        
        # Recarrega o objeto para obter o ID gerado pelo banco
        db.refresh(user)

        return user

    @staticmethod
    def get_all(db: Session):

        # Query simples: select * from users
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):

        # Query com filtro: select * from users where id = user_id
        # first() retorna o primeiro resultado ou None
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate):

        # Busca o usuário pelo ID
        user = db.query(User).filter(User.id == user_id).first()

        # Se não encontrar, retorna None
        if not user:
            return None

        # Atualiza os atributos do usuário com os novos dados
        user.name = user_data.name
        user.email = user_data.email

        # Salva as alterações no banco
        db.commit()
        
        # Recarrega o objeto para garantir dados atualizados
        db.refresh(user)

        return user

    @staticmethod
    def delete(db: Session, user_id: int):

        # Busca o usuário pelo ID
        user = db.query(User).filter(User.id == user_id).first()

        # Se não encontrar, retorna None
        if not user:
            return None

        # Remove o usuário da sessão
        db.delete(user)
        
        # Confirma a exclusão no banco
        db.commit()

        return user
