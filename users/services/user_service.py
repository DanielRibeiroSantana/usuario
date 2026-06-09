from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class UserService:
    @staticmethod
    def create(db: Session, user_data: UserCreate):

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        user.name = user_data.name
        user.email = user_data.email

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete(db: Session, user_id: int):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        db.delete(user)
        db.commit()

        return user
