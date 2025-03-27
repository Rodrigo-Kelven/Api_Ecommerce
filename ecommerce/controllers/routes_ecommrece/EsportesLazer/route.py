from ecommerce.schemas.ecommerce.schemas import ProductEsporteLazer, EspecificacoesEsporteLazer, ProductBase
from fastapi import APIRouter, status, HTTPException, Body, Depends, Query
from ecommerce.models.ecommerce.models import Product_Esporte_Lazer
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json
import uuid

from ecommerce.controllers.services.services_esport import ServicesEsportLazer

route_esporte_lazer = APIRouter()


@route_esporte_lazer.post(
    path="/category/esporte-lazer/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
async def create_product(
    product: ProductEsporteLazer = Body(embed=True),
    db: Session = Depends(get_db)
):
    return await ServicesEsportLazer.create_product(product, db)



@route_esporte_lazer.get(
    path="/category/esporte-lazer/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesEsporteLazer],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products"
)
async def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return await ServicesEsportLazer.get_all_products(skip, limit, db)

# rota de filtragem de buscas 
@route_esporte_lazer.get(
    path="/category/esporte-lazer/search-filters/",
    response_model=list[EspecificacoesEsporteLazer],
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
    return await ServicesEsportLazer.get_product(
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
async def searchProduct_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    return await ServicesEsportLazer.get_product_id(db, product_id)


@route_esporte_lazer.delete(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    return await ServicesEsportLazer.delete_product(product_id, db)



@route_esporte_lazer.put(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route put product for ID",
    name="Route PUT product for ID"
)
async def update_products(
    product_id: str,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_db),
):
    return await ServicesEsportLazer.update_product(product_id, product_data, db)

