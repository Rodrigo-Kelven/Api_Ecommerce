from ecommerce.schemas.ecommerce.schemas import ProductBrinquedosJogos, EspecificacoesBrinquedosJogos, ProductBase
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from fastapi import APIRouter, status, HTTPException, Body, Depends, Query
from ecommerce.models.ecommerce.models import Product_Brinquedos_Jogos
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json
import uuid

from ecommerce.controllers.services.services_brinquedos import Servico_Brinquedos_Jogos


route_brinquedos_jogos = APIRouter()


@route_brinquedos_jogos.post(
    path="/category/brinquedos-jogos/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
async def create_product(
    product: ProductBrinquedosJogos = Body(embed=True),
    db: Session = Depends(get_db)
):
    return await Servico_Brinquedos_Jogos.create_produtc_brinq_jogos(product, db)



@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesBrinquedosJogos],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products"
)
async def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return await Servico_Brinquedos_Jogos.get_products_brinq_jogos(skip, limit, db)


# rota de filtragem de buscas 
@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/search-filters/",
    response_model=list[EspecificacoesBrinquedosJogos],
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
    return await Servico_Brinquedos_Jogos.get_products_with_params(
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
async def searchProduct_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    return await Servico_Brinquedos_Jogos.get_product_ID(product_id, db)

@route_brinquedos_jogos.delete(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    return await Servico_Brinquedos_Jogos.delete_product_ID(product_id, db)

@route_brinquedos_jogos.put(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations Products",
    description="Route update products",
    name="Route PUT product for ID"
)
async def update_products(
    product_id: str,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_db),
):
    return await Servico_Brinquedos_Jogos.update_product_ID(product_id, product_data, db)