from ecommerce.schemas.ecommerce.schemas import ProductBrinquedosJogos, EspecificacoesBrinquedosJogos, ProductBase
from ecommerce.databases.ecommerce_config.database import get_Session
from fastapi import APIRouter, status, Body, Depends, Query
from sqlalchemy.orm import Session
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
async def createToyProduct(
    product: ProductBrinquedosJogos = Body(embed=True),
    db: Session = Depends(get_Session)
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
async def getToyProductInInterval(
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
async def getToyProductWithParams(
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
async def getToyProductById(
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
async def deleteToyProductById(
    product_id: str,
    db: Session = Depends(get_Session)
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
async def updateToyProductById(
    product_id: str,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_Session),
):
    # servco para fazer update in produto Brinquedos e Jogos
    return await Servico_Brinquedos_Jogos.updateToyProductByIdService(product_id, product_data, db)