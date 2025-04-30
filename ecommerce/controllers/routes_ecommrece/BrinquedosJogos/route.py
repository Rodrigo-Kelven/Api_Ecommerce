from ecommerce.schemas.ecommerce.schemas import ProductBrinquedosJogos, EspecificacoesBrinquedosJogos, ProductBase
from ecommerce.databases.ecommerce_config.database import get_Session
from fastapi import APIRouter, status, Body, Depends, Query, Request
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_brinquedos import Servico_Brinquedos_Jogos
from ecommerce.config.config import limiter
from ecommerce.auth.auth import get_current_user

route_brinquedos_jogos = APIRouter()


@route_brinquedos_jogos.post(
    path="/category/brinquedos-jogos/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
@limiter.limit("5/minute") # O ideal é 5
async def createToyProduct(
    request, Request,
    product: ProductBrinquedosJogos = Body(embed=True),
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para criar produto Brinquedo e Jogos
    return await Servico_Brinquedos_Jogos.createToyProductService(product, db)



@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesBrinquedosJogos],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products"
)
@limiter.limit("40/minute")
async def getToyProductInInterval(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_Session)
):
    # servico para pegar todos os produtos de Brinquedos e Jogos
    return await Servico_Brinquedos_Jogos.getToyProductInIntervalService(skip, limit, db)


# rota de filtragem de buscas 
@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/search-filters/",
    response_model=list[EspecificacoesBrinquedosJogos],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
)
@limiter.limit("40/minute")
async def getToyProductWithParams(
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
    # servico para buscar produtos por parametros
    return await Servico_Brinquedos_Jogos.getToyProductWithParamsService(
        db, name, category, stars, color, details,
        size, min_price, max_price, skip, limit
    )

@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations Products",
    description="Route get product for ID",
    name="Route GET product for ID"
)
@limiter.limit("40/minute")
async def getToyProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session)
):
    # servico para buscar produto por ID
    return await Servico_Brinquedos_Jogos.getToyProductByIdService(product_id, db)

@route_brinquedos_jogos.delete(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
@limiter.limit("5/minute")
async def deleteToyProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para deletar produto por ID
    return await Servico_Brinquedos_Jogos.deleteToyProductByIdService(product_id, db)

@route_brinquedos_jogos.put(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations Products",
    description="Route update products",
    name="Route PUT product for ID"
)
@limiter.limit("5/minute")
async def updateToyProductById(
    request: Request,
    product_id: str,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servco para fazer update in produto Brinquedos e Jogos
    return await Servico_Brinquedos_Jogos.updateToyProductByIdService(product_id, product_data, db)