
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    name: str
    email: EmailStr  # EmailStr valida automaticamente o formato do email
    password: str


class UserUpdate(BaseModel):

    name: str
    email: EmailStr


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr

    class Config:
        # from_attributes=True permite que Pydantic leia
        # atributos de objetos ORM (models.User)
        from_attributes = True
