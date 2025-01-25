# controllers/routes_ecommrece/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from typing import Union
from sqlalchemy.orm import Session
from models.ecommerce.models import Product  # Importando o modelo SQLAlchemy
from schemas.ecommerce.schemas import * # Importando o schema Pydantic para validação
from databases.ecommerce_config.database import SessionLocal  # Importando a sessão do banco de dados


route_ecom = APIRouter()

# criar mais endpoint para as categorias
# documentar cada endpoint e o que cada coisa faz

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um produto
@route_ecom.post(
        path="/products/", 
        response_model=ProductCreate,
        status_code=status.HTTP_201_CREATED,
        description="Create product",
        name="Route create product"
        )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
def create_product(product: ProductCreate, db: Session = Depends(get_db)): # db esta sendo tipado como uma Sessao, que tem uma dependencia em fazer um get, no DB
    db_product = Product(**product.dict())  # Usando o modelo SQLAlchemy
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Rota para listar todos os produtos
@route_ecom.get(path="/products/", 
                response_model=list[ProductCreate],
                status_code=status.HTTP_200_OK,
                description="List all producst",
                name="Route list products"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy
    return products

# Rota para consultar um produto pelo ID
@route_ecom.get(path="/products/{product_id}",
                response_model=ProductCreate,
                status_code=status.HTTP_200_OK,
                description="Search product with ID",
                name="Route search product with ID"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()  # Usando o modelo de SQLAlchemy
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Rota para deletar produto pelo ID
@route_ecom.delete(
    path="/product-delete/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
    )
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_delete = db.query(Product).filter(Product.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    db.refresh(product_delete)
    return f"Product with {product_id} removed succesfull"



