from ecommerce.auth.schemas.schemas import Token, User, UserResponse, UserResponseUpdate
from ecommerce.databases.ecommerce_config.database import SessionLocal_users, get_db_users
from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks, Body
from ecommerce.auth.models.models import UserDB, Role
from typing import List, Annotated
from ecommerce.auth.auth import *

from fastapi.security import OAuth2PasswordRequestForm

from ecommerce.auth.auth import check_permissions


class ServicesAuth:


    @staticmethod
    async def loginTokenService(
        form_data:OAuth2PasswordRequestForm = Depends(), 
        db: Session = Depends(get_db_users)
        ) -> Token:

        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
        )
        # response
        return Token(access_token=access_token, token_type="bearer")
    

    @staticmethod
    async def getInfoMeService(current_user):
        # Verifique as permissões antes de retornar as informações do usuário
        check_permissions(current_user, Role.user)  # Aqui verificamos se o usuário tem o papel de 'user'

        # Se a permissão foi verificada com sucesso, retornamos os dados do usuário
        return current_user
    

    @staticmethod
    async def creteUserService(username, email, full_name, password, db):

        # Verifica se o username já está registrado
        if get_user(db, username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username ja registrado!")
        
        # Verifica se o email já está registrado
        if db.query(UserDB).filter(UserDB.email == email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ja registrado!")

        # Hash da senha
        hashed_password = get_password_hash(password)
        
        # Criação do usuário
        db_user = UserDB(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            #role=role  # Define o papel do usuário, seja 'user', 'admin', ou 'moderator'
        )
        
        # Adiciona e comita o novo usuário no banco de dados
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    
    @staticmethod
    async def getUserListService(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
        # Verifique as permissões antes de retornar as informações do usuário
        check_permissions(current_user, Role.admin)  # Aqui verificamos se o usuário tem o papel de 'user'

        db = SessionLocal_users()
        users = db.query(UserDB).all()
        db.close()
        return [UserResponse (**user.__dict__) for user in users]
    

    @staticmethod
    async def updateUserService(username, user, current_user):
        db = SessionLocal_users()
        db_user = get_user(db, username)
        if not db_user:
            db.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado!")
        
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        db.close()
        return db_user
    

    @staticmethod
    async def deleteUserService(current_user):
        db = SessionLocal_users()
        db_user = get_user(db, current_user.username)  # Obtém o usuário autenticado

        if not db_user:
            db.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado!")
        
        db.delete(db_user)
        db.commit()
        db.close()
        return {"detail": f"User {current_user.username} deleted successfully."}
