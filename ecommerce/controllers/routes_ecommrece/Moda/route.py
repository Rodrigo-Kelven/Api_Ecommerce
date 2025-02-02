from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from models.ecommerce.models import Products_Moda_Feminina
from schemas.ecommerce.schemas import ProductModaFeminina, EspecificacoesModaFeminina, ProductBase
from databases.ecommerce_config.database import get_db


route_moda = APIRouter()



@route_moda.post(
    path="/category/moda-feminina/",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesModaFeminina,
    response_description="Informations of product",
    description="Create product",
    name="Route create product"
)
async def create_product(
    product: ProductModaFeminina = Body(embed=True),
    db: Session = Depends(get_db)
):
    db_product = Products_Moda_Feminina(**product.dict())  # Usando o modelo SQLAlchemy
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



@route_moda.get(path="/category/moda-feminina/", 
                response_model=list[EspecificacoesModaFeminina],
                status_code=status.HTTP_200_OK,
                description="List all producst",
                name="Route list products"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
def read_products(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    products = db.query(Products_Moda_Feminina).offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy
    return products



@route_moda.get(path="/category/moda-feminina/{product_id}",
                response_model=EspecificacoesModaFeminina,
                status_code=status.HTTP_200_OK,
                description="Search product with ID",
                name="Route search product with ID"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
def read_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id).first()  # Usando o modelo de SQLAlchemy
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@route_moda.delete(
    path="/category/moda-feminina/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
    )
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
    # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500
    print("Produto deletado!!")
    return f"Product with {product_id} removed succesfull"



@route_moda.put(
    path="/category/moda-feminina/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesModaFeminina,
    response_description="Informations of product",
    description="Update product for ID",
    name="Route update product for ID"
    )
async def update_product(
    product_id: int,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
    product = db.query(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id).first()


    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    

    for key, value in product_data.dict().items():
        setattr(product, key, value)

    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(product)
    return product
