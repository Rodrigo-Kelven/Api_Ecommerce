from fastapi import APIRouter, Form, Body, Query, status, Depends, HTTPException
from schemas.users.schemas import UserCreate, UserResponse
from models.users.models import User
from sqlalchemy.orm import Session
from databases.ecommerce_config.database import get_db

route_users = APIRouter() 

# adicionar mais validacoes
# adicionar protecao contra ataques de sqlinjection
# preparar o sistema de admin e usuarios

# Rota para criar usuarios
@route_users.post(
        path="/user-create/",
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse,
        response_model_exclude=["password"],
        description="Route create user",
        name="Route create user"
)

async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Verifica se o usuário já existe
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Cria um novo usuário
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  # Retorna o usuário criado


# Rota para listar todos os usuarios, "usar isso apenas como admin"
@route_users.get(
    path="/users/list/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
    description="Route list informations users",
    name="Route list informatinos users"
)
async def list_users(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Rota para consultar um usuario pelo ID
@route_users.get(path="/user-informations/{user_id}",
                response_model=UserResponse,
                status_code=status.HTTP_200_OK,
                description="Search user with ID",
                name="Route search user with ID"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def read_user_id(
    user_id: int,
    db: Session = Depends(get_db
)):
    user = db.query(User).filter(User.id == user_id).first()  # Usando o modelo de SQLAlchemy
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Rota para atualizar informacoes de um usuarios -> pensar em caso esqueca a senha, ataques de phishing
@route_users.put(
        path="/user-update-informations/{user_id}", 
        status_code=status.HTTP_200_OK,
        response_model=UserResponse,
        description="Route list informations users",
        name="Route list informatinos users"
)

def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
    ):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user



# Rota para deletar usuario pelo ID
@route_users.delete(
        path="/user-delete/{user_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        description="Delete users for ID",
        name="Route delete users for ID"
    )

def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    db.delete(db_user)
    db.commit()