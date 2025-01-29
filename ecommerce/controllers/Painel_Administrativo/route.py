from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.users.models import User
from databases.ecommerce_config.database import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../ecommerce/controllers/Painel_Administrativo/templates") # separar uma pasta somente para os paineis e templates ate criar o frontend

# adicionar validacoes de parametros nos forms, field
# deixar as operacoes mais rapidas
# dividir o painel entre usuarios e produtos
# adicionar ao painel as informacoes nescesarias: estoque, produtos, usuarios, estatistias e etc

# Rota GET (renderiza a pagina) -> lista os usuarios 
@router.get(
        path="/users/",
        status_code=status.HTTP_200_OK,
        description="Renderiza o Painel de Admin Users",
        name="Route Admin Users",
        response_class=HTMLResponse
)
def list_users(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

# Rota GET (renderiza a pagina) -> pag criar users
@router.get(
        path="/user/create",
        status_code=status.HTTP_200_OK,
        description="Renderiza o Painel de Admin Users",
        name="Route Admin Users",
        response_class=HTMLResponse
)
def create_user_form(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})


# Rota POST (envia os dados para o banco de dados) -> create users
@router.post(
        path="/user-create/",
        status_code=status.HTTP_201_CREATED,
        description="Renderiza o Painel de Admin Users",
        name="Route Admin Users",
)
async def create_user(

    name: str = Form(...),
    fullname: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = User(
        name=name,
        fullname=fullname,
        username=username,
        email=email,
        password=password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Redireciona para a página inicial após a criação do usuário
    return RedirectResponse(url="/ecommerce/admin/users/", status_code=303)

# Rota GET (renderiza a pagina)-> pag update informations users
@router.get(
        path="/user/update/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Renderiza o Painel de Admin Users",
        name="Route Admin Users",
        response_class=HTMLResponse
)
def update_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return templates.TemplateResponse("user_update.html", {"request": request, "user": user})


# Rota POST (envia os dados para o banco de dados)-> Update informations
@router.post("/user-update/{user_id}")

async def update_user(
    user_id: int,
    name: str = Form(...),
    fullname: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User  not found")

    db_user.name = name
    db_user.fullname = fullname
    db_user.username = username
    db_user.email = email
    db_user.password = password
    db.commit()
    db.refresh(db_user)

    # Redireciona para a lista de usuários após a atualização
    return RedirectResponse(url="/ecommerce/admin/users/", status_code=303)
    

# Rota GET -> pag delete user
@router.get(
        path="/user/delete/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Renderiza o Painel de Admin Users",
        name="Route Admin Users",
        response_class=HTMLResponse
)
def delete_user_form(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return templates.TemplateResponse("user_delete.html", {"request": request, "user": user})


# Rota POST -> delete user
@router.post(
    path="/user-delete/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Renderiza o Painel de Admin Users",
    name="Route Admin Users",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    db.delete(db_user)
    db.commit()

    return RedirectResponse(url="/ecommerce/admin/users", status_code=303)
