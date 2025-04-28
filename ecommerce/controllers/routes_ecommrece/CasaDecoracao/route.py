from ecommerce.schemas.ecommerce.schemas import EspecificacoesCasaeDecoracao, ProductCasaeDecoracao, ProductBase
from ecommerce.databases.ecommerce_config.database import get_Session
from fastapi import APIRouter, status, Body, Depends, Query
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_casadecoracao import ServicesCasaDecoracao


route_casa_decoracao = APIRouter()


@route_casa_decoracao.post(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Create product home and decorations",
    name="Route create product",
    )
async def createDecorationProduct(
    product: ProductCasaeDecoracao = Body(embed=True), 
    db: Session = Depends(get_Session)
):
    # servico para criar produto
    return await ServicesCasaDecoracao.createDecorationProductService(product, db)



@route_casa_decoracao.get(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesCasaeDecoracao],
    description="List all products",
    name="Route list products"
)
async def getDecorationProductInInterval(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_Session)
):
    # servico para retornar todos os produtos de casa e decoracao
    return await ServicesCasaDecoracao.getDecorationProductInIntervalService(skip, limit, db)

# rota de filtragem de buscas 
@route_casa_decoracao.get(
    path="/category/casa-e-decoracao/search-filters/",
    response_model=list[EspecificacoesCasaeDecoracao],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
)
async def getDecorationProductWithParams(
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
    # servico para retornar produtos passando parametros
    return await ServicesCasaDecoracao.getDecorationProductWithParamsService(
        db, name, category, stars, color, details,
        size, min_price, max_price, skip, limit
    )

@route_casa_decoracao.get(
    path="/category/casa-e-decoracao/{product_id}",
    response_model=EspecificacoesCasaeDecoracao,
    status_code=status.HTTP_200_OK,
    description="Search product with ID",
    name="Route search product with ID"
)
async def getDecorationProductById(
    product_id: str,
    db: Session = Depends(get_Session)
):
    # servico para retornar produto passando id
    return await ServicesCasaDecoracao.getDecorationProductByIdService(product_id, db)



@route_casa_decoracao.delete(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
)
async def deleteDecorationProductById(
    product_id: str,
    db: Session = Depends(get_Session)
):
    # servico para deletar produto passando id
    return await ServicesCasaDecoracao.deleteDecorationProductByIdService(product_id, db)



@route_casa_decoracao.put(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Route for update products",
    name="Route create product"
)
async def updateDecorationProductById(
    product_id: str,
    db: Session = Depends(get_Session),
    product_data: ProductBase = Body(embed=True)
    ):
    # servico para realizar update em produto passando id
    return await ServicesCasaDecoracao.updateDecorationProductByIdService(product_id, db, product_data)