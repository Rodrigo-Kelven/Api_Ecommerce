from ecommerce.auth.schemas.schemas import Token, User, UserResponse, UserResponseUpdate
from ecommerce.databases.ecommerce_config.database import SessionLocal_users, get_db_users
from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks, Body
from ecommerce.auth.models.models import UserDB, Role
from typing import List, Annotated
from ecommerce.auth.auth import *

from fastapi.security import OAuth2PasswordRequestForm

from ecommerce.auth.auth import check_permissions

# caso queira entender como funciona, recomendo desenhar o fluxo
routes_auth_auten = APIRouter()



# rota login, esta rota recebe os dados do front para a validacao
@routes_auth_auten.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_users)) -> Token:

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
    return Token(access_token=access_token, token_type="bearer")




# rota para ter suas informacoes
@routes_auth_auten.get(
        path="/users/me/",
        response_model=UserResponse,
        response_description="Informations user",
        description="Route get informations user",
        name="Route get informations user"
)
async def read_users_me(current_user: Annotated[User , Depends(get_current_user)]):
    # Verifique as permissões antes de retornar as informações do usuário
    check_permissions(current_user, Role.user)  # Aqui verificamos se o usuário tem o papel de 'user'

    # Se a permissão foi verificada com sucesso, retornamos os dados do usuário
    return current_user



# rota para ter as informacoes sobre seus items, lembre da alura, aqui seria onde guarda os "certificados"
@routes_auth_auten.get(
        path="/users/me/items/",
        response_description="Informations items user",
        description="Route get items user",
        name="Route get items user"
)
async def read_own_items(current_user: Annotated[User , Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]



# Rota para criar um novo usuário -> qualquer usuario pode criar 
# Rota para criar um novo usuário
@routes_auth_auten.post("/users/")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    #role: str = Role.user,  # Permite definir o papel do usuário, default é 'user'
    db: Session = Depends(get_db_users),
):
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


# Listar todos os usuários -> somente user admin 
@routes_auth_auten.get(
        path="/users/",
        response_model=List[UserResponse],
        response_description="Users",
        description="Route list users",
        name="Route list users"
)
async def get_users(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
    # Verifique as permissões antes de retornar as informações do usuário
    check_permissions(current_user, Role.admin)  # Aqui verificamos se o usuário tem o papel de 'user'

    db = SessionLocal_users()
    users = db.query(UserDB).all()
    db.close()
    return [UserResponse (**user.__dict__) for user in users]


# Atualizar informações do usuário
@routes_auth_auten.put(
        path="/users/{username}",
        response_model=UserResponse,
        response_description="Update informations user",
        description="Route update informations user",
        name="Route informations user"
)
async def update_user(
    username: str, user: UserResponseUpdate, current_user: Annotated[User , Depends(get_current_active_user)]
    ):

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


# Deletar a conta do usuário somente autenticado
@routes_auth_auten.delete(
        path="/users/delete-account-me/",
        response_description="Informations delete account",
        name="Route delete user"
)
async def delete_user(
    current_user: Annotated[User , Depends(get_current_active_user)],
    ):
    db = SessionLocal_users()
    db_user = get_user(db, current_user.username)  # Obtém o usuário autenticado

    if not db_user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado!")
    
    db.delete(db_user)
    db.commit()
    db.close()
    return {"detail": f"User  {current_user.username} deleted successfully"}


# exemplo simples sistena de envio de mensagem por email
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@routes_auth_auten.post(
        "/send-notification/{email}",
        response_description="Send mesage email",
        description="Route send mesage email",
        name="Route send mesage email"
)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}