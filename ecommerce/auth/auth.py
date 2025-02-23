from ecommerce.auth.models.models import UserDB, Role
from ecommerce.databases.ecommerce_config.database import SessionLocal_users
from ecommerce.auth.config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context, oauth2_scheme
from ecommerce.auth.schemas.schemas import TokenData, User
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
import jwt.exceptions # Corrigido para capturar exceções genéricas do JWT
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from starlette.requests import Request
from starlette.responses import JSONResponse


# Funções utilitárias
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Pegar o password transformado em hash
def get_password_hash(password):
    return pwd_context.hash(password)


# Pegar a sessão do primeiro usuário encontrado
def get_user(db: Session, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()


# Verifica se o usuário está autenticado
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Criar token de acesso
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Garantir que o 'role' seja serializável (se for Enum)
    if isinstance(to_encode.get("role"), Role):
        to_encode["role"] = to_encode["role"].value  # Pega o valor da Enum

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Pegar a sessão atual
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:  # Captura exceções genéricas de JWT
        raise credentials_exception

    db = SessionLocal_users()
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Verificar se a sessão está ativa
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Função que verifica permissões de acesso
def check_permissions(user: UserDB, required_role: Role):
    if user.role != required_role and user.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissões Insuficiêntes!")


# Configurar o log
logging.basicConfig(level=logging.INFO)


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Loga os detalhes da requisição
        logging.info(f"Requisição recebida: {request.method} {request.url}")

        # Chama o próximo middleware ou rota
        response = await call_next(request)

        # Loga os detalhes da resposta
        logging.info(f"Resposta enviada com status {response.status_code}")

        return response


# Middleware que verifica um token de autenticação antes de permitir o acesso a uma rota
class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")

        if token != "Bearer secret-token":
            raise HTTPException(status_code=401, detail="Unauthorized")

        response = await call_next(request)
        return response


# Middleware que trata exceções de forma centralizada
class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Em caso de erro, retorna uma resposta com código 500
            return JSONResponse(
                status_code=500,
                content={"message": "An unexpected error occurred", "error": str(e)},
            )
