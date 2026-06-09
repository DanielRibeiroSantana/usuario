"""Serviço de lógica de negócio para usuários.

Este módulo implementa as operações CRUD (Create, Read, Update, Delete)
para a entidade User. As funções aqui separão a lógica de negócio
das rotas HTTP.
"""
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class UserService:
    """Serviço para gerenciar operações de usuários.
    
    Todos os métodos são estáticos pois não mantêm estado.
    Recebem a sessão do banco como parâmetro (dependency injection).
    """

    @staticmethod
    def create(db: Session, user_data: UserCreate):
        """Cria um novo usuário no banco de dados.
        
        Args:
            db: Sessão do banco de dados
            user_data: Dados validados do novo usuário (UserCreate)
        
        Returns:
            User: Objeto usuário criado com ID gerado
        """
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
        """Obtém todos os usuários do banco de dados.
        
        Args:
            db: Sessão do banco de dados
        
        Returns:
            list[User]: Lista de todos os usuários
        """
        # Query simples: select * from users
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        """Obtém um usuário específico pelo ID.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário a buscar
        
        Returns:
            User | None: Usuário encontrado ou None se não existe
        """
        # Query com filtro: select * from users where id = user_id
        # first() retorna o primeiro resultado ou None
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate):
        """Atualiza um usuário existente.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário a atualizar
            user_data: Dados validados para atualização (UserUpdate)
        
        Returns:
            User | None: Usuário atualizado ou None se não existe
        """
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
        """Deleta um usuário do banco de dados.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário a deletar
        
        Returns:
            User | None: Usuário deletado ou None se não existe
        """
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
