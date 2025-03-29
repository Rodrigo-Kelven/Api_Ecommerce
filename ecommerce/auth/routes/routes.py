from ecommerce.auth.schemas.schemas import Token, User, UserResponse, UserResponseUpdate
from ecommerce.databases.ecommerce_config.database import SessionLocal_users, get_db_users
from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks, Body
from ecommerce.auth.models.models import UserDB, Role
from typing import List, Annotated
from ecommerce.auth.auth import *

from fastapi.security import OAuth2PasswordRequestForm

from ecommerce.auth.auth import check_permissions

from ecommerce.auth.service.services_auth import ServicesAuth

# caso queira entender como funciona, recomendo desenhar o fluxo
routes_auth_auten = APIRouter()



# rota login, esta rota recebe os dados do front para a validacao
@routes_auth_auten.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    description="Route login",
    name="Route Login",
    response_description="Sucessfull Login."
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_users)
    ) -> Token:
    # servico para login do usuario
    return await ServicesAuth.loginTokenService(form_data, db)


# rota para ter suas informacoes
@routes_auth_auten.get(
        path="/users/me/",
        status_code=status.HTTP_200_OK,
        response_model=UserResponse,
        response_description="Informations user",
        description="Route get informations user",
        name="Route get informations user"
)
async def read_users_me(current_user: Annotated[User , Depends(get_current_user)]):
    # servico para obter informacoes pessoais
    return await ServicesAuth.getInfoMeService(current_user)


# sera removida
# rota para ter as informacoes sobre seus items, lembre da alura, aqui seria onde guarda os "certificados"
@routes_auth_auten.get(
        path="/users/me/items/",
        status_code=status.HTTP_200_OK,
        response_description="Informations items user",
        description="Route get items user",
        name="Route get items user"
)
async def read_own_items(current_user: Annotated[User , Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]



# Rota para criar um novo usuário -> qualquer usuario pode criar 
# Rota para criar um novo usuário
@routes_auth_auten.post(
    path="/users/",
    status_code=status.HTTP_201_CREATED,
    description="Route create user",
    name="Route create User"
)
async def createUser(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    #role: str = Role.user,  # Permite definir o papel do usuário, default é 'user'
    db: Session = Depends(get_db_users),
):
   # servico para criacao de usuarios
   return await ServicesAuth.creteUserService(username, email, full_name, password, db)


# sera removido
# Listar todos os usuários -> somente user admin 
@routes_auth_auten.get(
        path="/users/",
        response_model=List[UserResponse],
        response_description="Users",
        description="Route list users",
        name="Route list users"
)
async def getUsersList(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
    # servico para lsitar todos os usuarios
    return await ServicesAuth.getUserListService(current_user)


# Atualizar informações do usuário
@routes_auth_auten.put(
        path="/users/{username}",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=UserResponse,
        response_description="Update informations user.",
        description="Route update informations user",
        name="Route informations user"
)
async def updateUser(
    username: str,
    user: UserResponseUpdate,
    current_user: Annotated[User , Depends(get_current_active_user)]
    ):
    # servico para atualizar informacoes do usuario
    return await ServicesAuth.updateUserService(username, user, current_user)

# Deletar a conta do usuário somente autenticado
@routes_auth_auten.delete(
        path="/users/delete-account-me/",
        status_code=status.HTTP_204_NO_CONTENT,
        response_description="Informations delete account",
        name="Route delete user"
)
async def deleteUser(
    current_user: Annotated[User , Depends(get_current_active_user)]):
    # servico para deletar usuario
    return await ServicesAuth.deleteUserService(current_user)


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