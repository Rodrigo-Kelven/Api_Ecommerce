from ecommerce.schemas.ecommerce.schemas import ProductEletronicos, EspecificacoesEletronicos, ProductBase 
from fastapi import APIRouter, Depends,  status, Body, Query, Request
from ecommerce.databases.ecommerce_config.database import  get_Session
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_eletronics import ServicesEletronics
from ecommerce.auth.auth import get_current_user
from ecommerce.config.config import limiter


route_eletronicos = APIRouter()


@route_eletronicos.post(
        path="/category/eletronic/", 
        status_code=status.HTTP_201_CREATED,
        response_model=EspecificacoesEletronicos,
        response_description="Informations of product",
        description="Create product",
        name="Route create product"
)  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
@limiter.limit("5/minute")
async def createEletronicProduct(
    request: Request,
    product: ProductEletronicos = Body(embed=True),
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
): # db esta sendo tipado como uma Sessao, que tem uma dependencia em fazer um get, no DB
    # servico para criar produtos eletronicos
    return await ServicesEletronics.createEletronicProductService(product,db)



@route_eletronicos.get(
        path="/category/eletronic/", 
        response_model=list[EspecificacoesEletronicos],
        status_code=status.HTTP_200_OK,
        description="List all producst",
        name="Route list products"
)  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
@limiter.limit("40/minute")
async def getEletronicProductInInterval(
    request: Request,
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_Session)
):
    # servico para pegar todos os produtos de eletornicos
    return await ServicesEletronics.getEletronicProductInIntervalService(skip, limit, db)



# rota de filtragem de buscas 
@route_eletronicos.get(
    path="/category/eletronic/search-filters/",
    response_model=list[EspecificacoesEletronicos],
    status_code=status.HTTP_200_OK,
    description="List serach products",
    name="Route search products"
)
@limiter.limit("40/minute")
async def getEletronicProductWithParams(
    request: Request,
    category: str = Query(None, description="Filtrar por categoria"),
    min_price: float = Query(None, description="Filtrar por preço mínimo"),
    max_price: float = Query(None, description="Filtrar por preço máximo"),
    name: str = Query(None, description="Filtrar por nome"),
    stars: int = Query(None, description="Filtrar por quantidade de estrelas"),
    color: str = Query(None, description="Filtrar pela cor"),
    size: float = Query(None, description="Filtrar pelo tamanho"),
    details: str = Query(None, description="Filtrar por detalhes"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_Session)
):
    # servico para retornar produtos de eletronicos baseados nos parametros
    return await ServicesEletronics.getEletronicProductWithParamsService(
        db, category, name, stars, color,
        details, size,min_price, max_price,
        skip, limit
    )



@route_eletronicos.get(
        path="/category/eletronic/{product_id}",
        response_model=EspecificacoesEletronicos,
        status_code=status.HTTP_200_OK,
        description="Search product with ID",
        name="Route search product with ID"
)  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
@limiter.limit("40/minute")
async def getEletronicProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session)
):
    # servico para retornar produto com parametro ID passado
    return await ServicesEletronics.getEletronicProductByIdService(product_id, db)


@route_eletronicos.delete(
    path="/category/eletronic/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
)
@limiter.limit("5/minute")
async def deleteEletronicProductById(
    request: Request,
    product_id: str, 
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para deletar produto com parametro ID passado
    return await ServicesEletronics.deleteEletronicProductByIdService(product_id, db)



@route_eletronicos.put(
    path="/category/eletronic/{product_id}",
    response_model=EspecificacoesEletronicos,
    status_code=status.HTTP_200_OK,
    description="Update product for ID",
    name="Route update product with ID"
)
@limiter.limit("5/minute")
async def updateEletronicProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session),
    product_data: ProductBase = Body(embed=True),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para realizar update em produto com parametro ID passado
    return await ServicesEletronics.updateEletronicProductByIdService(product_id, db, product_data)
