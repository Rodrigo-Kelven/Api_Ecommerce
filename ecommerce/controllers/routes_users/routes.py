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
        path="/users/",
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
    path="/users/registred/",
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