from fastapi import APIRouter, status, Depends, Body, Query
from ecommerce.schemas.ecommerce.schemas import EspecificacoesAutomotivo, ProductAutomotivo, ProductBase
from ecommerce.controllers.services.services_automotivo import Services_Automotivo
from ecommerce.databases.ecommerce_config.database import get_db
from sqlalchemy.orm import Session


route_automotivo = APIRouter()


@route_automotivo.post(
    path="/category/automotivo",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesAutomotivo,
    response_description="Informations product",
    description="Route create product",
    name="Route Create product category"
)
async def create_product(
    product: ProductAutomotivo = Body(embed=True),
    db: Session = Depends(get_db)
):
    # servico para registro de produto automotivo
    return await Services_Automotivo.create_product_automotivo(product, db)



@route_automotivo.get(
    path="/category/automotivo",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesAutomotivo],
    response_description="Informations products",
    description="Route list products",
    name="Route list products category automotivo"
)
async def get_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    # servico para pegar todos os produtos de automotivo
    return await Services_Automotivo.get_products_in_interval(skip, limit, db)

# rota de filtragem de buscas 
@route_automotivo.get(
    path="/category/automotivo/search-filters/",
    response_model=list[EspecificacoesAutomotivo],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
)
async def read_products(
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
    db: Session = Depends(get_db)
):
    # servico para pegar todos os produtos com base nos parametros
    return await Services_Automotivo.get_prodcut_with_params(
        name, category, stars, color, details,
        size, min_price, max_price, skip, limit, db
    )


@route_automotivo.get(
    path="/category/automotivo/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesAutomotivo,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products for ID"
)
async def get_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    # servico para pegar produto automotivo por ID
    return await Services_Automotivo.get_product_with_ID(product_id, db)


@route_automotivo.delete(
    path="/category/automotivo/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Information products",
    description="Route get product for id",
    name="Route DELETE products for ID"
)
async def delete_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    # servico para deletar produto automotivo por ID
    return await Services_Automotivo.delete_product_automotivo_ID(product_id, db)


@route_automotivo.put(
    path="/category/automotivo/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesAutomotivo,
    description="Route PUT product",
    name="Route PUT product for ID"
)
async def update_product(
    product_id: str,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
    # servico para atualizar produto por ID
    return await Services_Automotivo.update_product_id(product_id, db, product_data)