from fastapi import APIRouter, status, Body
from schemas.ecommerce.schemas import *

route_moda = APIRouter()

@route_moda.post(
    path="/category/moda-feminina/",
    status_code=status.HTTP_201_CREATED,
    description="Create product mode female",
    name="Route create product",
    response_model=EspecificacoesModaFeminina,
    response_description="Informations of product"
)
async def create_product(product: ProductModaFeminina = Body(embed=True)):
    print(product)
    return product