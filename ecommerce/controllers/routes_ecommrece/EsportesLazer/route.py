from ecommerce.schemas.ecommerce.schemas import ProductEsporteLazer, EspecificacoesEsporteLazer, ProductBase
from fastapi import APIRouter, status, Body, Depends, Query, Request
from ecommerce.databases.ecommerce_config.database import get_Session
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_esport import ServicesEsportLazer
from ecommerce.auth.auth import get_current_user
from ecommerce.config.config import limiter


route_esporte_lazer = APIRouter()


@route_esporte_lazer.post(
    path="/category/esporte-lazer/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
@limiter.limit("5/minute")
async def createSportProduct(
    request: Request,
    product: ProductEsporteLazer = Body(embed=True),
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # service para criar produto
    return await ServicesEsportLazer.createSportProductService(product, db)



@route_esporte_lazer.get(
    path="/category/esporte-lazer/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesEsporteLazer],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products"
)
@limiter.limit("40/minute")
async def getSportProductInInterval(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_Session)
):
    # servico para listar produto com parametros 
    return await ServicesEsportLazer.getSportProductInIntervalService(skip, limit, db)



# rota de filtragem de buscas 
@route_esporte_lazer.get(
    path="/category/esporte-lazer/search-filters/",
    response_model=list[EspecificacoesEsporteLazer],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
)
@limiter.limit("40/minute")
async def getSportProductWithParams(
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
    # servico para listar produtos com parametros especificos
    return await ServicesEsportLazer.getSportProductWithParamsService(
        db, name, category, stars, color,
        details, size, min_price, max_price, skip, limit
    )



@route_esporte_lazer.get(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route get product for ID",
    name="Route GET product for ID"
)
@limiter.limit("40/minute")
async def getSportProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session)
):
    # servico para pegar produto por ID
    return await ServicesEsportLazer.getSportProductByIdService(db, product_id)



@route_esporte_lazer.delete(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
@limiter.limit("5/minute")
async def deleteSportProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para deletar produto pelo ID
    return await ServicesEsportLazer.deleteSportProductByIdService(product_id, db)



@route_esporte_lazer.put(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route put product for ID",
    name="Route PUT product for ID"
)
@limiter.limit("5/minute")
async def updateSportProductById(
    request: Request,
    product_id: str,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para atualizar informacoes do produto
    return await ServicesEsportLazer.updateSportProductByIdService(product_id, product_data, db)

