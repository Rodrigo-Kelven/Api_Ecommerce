from fastapi import APIRouter, status, Body
from schemas.ecommerce.schemas import *



route_cada_decoracao = APIRouter()


@route_cada_decoracao.post(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_201_CREATED,
    description="Create product home and decorations",
    name="route create product",
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product"
)
async def create_product(product: ProductCasaeDecoracao = Body(embed=True)):
    return product