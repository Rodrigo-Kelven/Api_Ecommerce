from ecommerce.schemas.ecommerce.schemas import EspecificacoesLivrosPapelaria, ProductLivrosPapelaria, ProductBase
from ecommerce.databases.ecommerce_config.database import get_db
from fastapi import APIRouter, status, Depends, Body, Query
from sqlalchemy.orm import Session
from ecommerce.controllers.services.services_livraria import ServicesLivraria


route_livros_papelaria = APIRouter()


@route_livros_papelaria.post(
    path="/category/livros-papelaria/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesLivrosPapelaria,
    response_description="Informations product",
    description="Route create product",
    name="Route Create product"
)
async def createLibraryProduct(
    product: ProductLivrosPapelaria,
    db: Session = Depends(get_db)
):
    # servico para criar produto
    return await ServicesLivraria.createLibraryProductService(product, db)



@route_livros_papelaria.get(
    path="/category/livros-papelaria/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesLivrosPapelaria],
    response_description="Informations products",
    description="Route list products",
    name="Route list products category papelaria"
)
async def getLibraryProductInInterval(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    # servico para pegar produtos com parametros
    return await ServicesLivraria.getLibraryProductInIntervalService(skip, limit, db)


# rota de filtragem de buscas 
@route_livros_papelaria.get(
    path="/category/livros-papelaria/search-filters/",
    response_model=list[EspecificacoesLivrosPapelaria],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
)
async def getLibraryProductWithParams(
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
    # servico para pegar produtos com parametros especificos
    return await ServicesLivraria.getLibraryProductWithParamsService(
        db, name, category, stars, color,
        details, size, min_price, max_price, skip, limit
    )


@route_livros_papelaria.get(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesLivrosPapelaria,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def getLibraryProductById(
    product_id: str,
    db: Session = Depends(get_db)
):
    # servico para pegar produto por ID  
    return await ServicesLivraria.getLibraryProductByIdService(product_id, db)


@route_livros_papelaria.delete(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def deleteLibraryProductById(
    product_id: str,
    db: Session = Depends(get_db)
):
    # servico para deletar produto por ID
    return await ServicesLivraria.deleteLibraryProductByIdService(product_id, db)


@route_livros_papelaria.put(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesLivrosPapelaria,
    description="Route PUT product",
    name="Route PUT product"
)
async def updateLibraryProductById(
    product_id: str,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
    # servico para atualizar produto por ID
    return await ServicesLivraria.updateLibraryProductByIdService(product_id, db, product_data)