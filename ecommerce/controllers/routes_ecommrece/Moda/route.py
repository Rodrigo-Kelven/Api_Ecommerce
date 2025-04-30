from ecommerce.schemas.ecommerce.schemas import ProductModaFeminina, EspecificacoesModaFeminina, ProductBase
from fastapi import APIRouter, Depends, status, Body, Query, Request
from ecommerce.databases.ecommerce_config.database import get_Session
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_moda import ServiceModa
from ecommerce.auth.auth import get_current_user
from ecommerce.config.config import limiter


route_moda = APIRouter()


@route_moda.post(
    path="/category/moda-feminina/",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesModaFeminina,
    response_description="Informations of product",
    description="Create product",
    name="Route create product"
)
@limiter.limit("5/minute")
async def createFashionProduct(
    request: Request,
    product: ProductModaFeminina = Body(embed=True),
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # service para criar produto
    return await ServiceModa.createFashionProductService(product, db)



@route_moda.get(
        path="/category/moda-feminina/", 
        response_model=list[EspecificacoesModaFeminina],
        status_code=status.HTTP_200_OK,
        description="List all producst",
        name="Route list products"
)  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
@limiter.limit("40/minute")
async def getFashionProductInInterval(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_Session)
):
    # servico para listar produtos com parametros
    return await ServiceModa.getFashionProductInIntervalService(skip, limit, db)



# rota de filtragem de buscas 
@route_moda.get(
    path="/category/moda-feminina/search-filters/",
    response_model=list[EspecificacoesModaFeminina],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
)
@limiter.limit("40/minute")
async def getFashionProductWithParams(
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
    # servico para procurar produtos com parametros
    return await ServiceModa.getFashionProductWithParamsService(
        db, name, category, stars, color, 
        details, size, min_price, max_price,
        skip, limit
    )



@route_moda.get(
    path="/category/moda-feminina/{product_id}",
    response_model=EspecificacoesModaFeminina,
    status_code=status.HTTP_200_OK,
    description="Get product by ID",
    name="Route get product by ID"
)
@limiter.limit("40/minute")
async def getFashionProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session)
):
    # servico para procurar produto por ID
    return await ServiceModa.getFashionProductByIdService(product_id, db)



@route_moda.delete(
    path="/category/moda-feminina/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
)
@limiter.limit("5/minute")
async def deleteFashionProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para deletar produto por ID
    return await ServiceModa.deleteFashionProductByIdService(product_id, db)



@route_moda.put(
    path="/category/moda-feminina/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesModaFeminina,
    response_description="Informations of product",
    description="Update product for ID",
    name="Route update product for ID"
)
@limiter.limit("5/minute")
async def updateFashionProductById(
    request: Request,
    product_id: str,
    db: Session = Depends(get_Session),
    product_data: ProductBase = Body(embed=True),
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
):
    # servico para atualizar produto por ID
    return await ServiceModa.updateFashionProductByIdService(product_id, db, product_data)
