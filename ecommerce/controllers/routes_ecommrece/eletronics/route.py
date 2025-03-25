from ecommerce.schemas.ecommerce.schemas import ProductEletronicos, EspecificacoesEletronicos, ProductBase 
from fastapi import APIRouter, Depends,  status, Body, Query
from ecommerce.databases.ecommerce_config.database import  get_db
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_eletronics import ServicesEletronics


route_eletronicos = APIRouter()


@route_eletronicos.post(
        path="/category/eletronic/", 
        status_code=status.HTTP_201_CREATED,
        response_model=EspecificacoesEletronicos,
        response_description="Informations of product",
        description="Create product",
        name="Route create product"
    )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def create_product(
    product: ProductEletronicos = Body(embed=True),
    db: Session = Depends(get_db)
): # db esta sendo tipado como uma Sessao, que tem uma dependencia em fazer um get, no DB
    # servico para criar produtos eletronicos
    return await ServicesEletronics.create_product(product,db)



@route_eletronicos.get(
        path="/category/eletronic/", 
        response_model=list[EspecificacoesEletronicos],
        status_code=status.HTTP_200_OK,
        description="List all producst",
        name="Route list products"
        )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def read_products(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return await ServicesEletronics.get_all_products(skip, limit, db)

# rota de filtragem de buscas 
@route_eletronicos.get(
    path="/category/eletronic/search-filters/",
    response_model=list[EspecificacoesEletronicos],
    status_code=status.HTTP_200_OK,
    description="List serach products",
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
    return await ServicesEletronics.get_product_params(
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
async def read_product_id(
    product_id: str,
    db: Session = Depends(get_db
)):

    return await ServicesEletronics.get_product_id(product_id, db)


@route_eletronicos.delete(
    path="/category/eletronic/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
    )
async def delete_product_id(
    product_id: str, 
    db: Session = Depends(get_db)
):
    return await ServicesEletronics.delete_product(product_id, db)



@route_eletronicos.put(
    path="/category/eletronic/{product_id}",
    response_model=EspecificacoesEletronicos,
    status_code=status.HTTP_200_OK,
    description="Update product for ID",
    name="Route update product with ID"
)
async def update_product(
    product_id: str,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True)
):

    return await ServicesEletronics.update_product(product_id, db, product_data)
