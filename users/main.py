from fastapi import FastAPI
from .api.users import router as users_router
from .core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='User Management API',
    description='API para gerenciamento de usuários',
    version='1.0.0',
)

app.include_router(users_router)


@app.get('/')
def health_check():

    return {'status': 'online'}
