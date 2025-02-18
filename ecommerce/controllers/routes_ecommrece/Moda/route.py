from ecommerce.schemas.ecommerce.schemas import ProductModaFeminina, EspecificacoesModaFeminina, ProductBase
from ecommerce.models.ecommerce.models import Products_Moda_Feminina
from fastapi import APIRouter, Depends, HTTPException, status, Body
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json


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
    
    if products:
        logger.info(msg="Produtos de moda sendo listado!")
        products_listed = [Products_Moda_Feminina.from_orm(product) for product in products]
        return products_listed

    if not products:
        logger.info(msg="Nenhum produto de moda nao encontardo!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de moda encontrado!")



@route_moda.get(
    path="/category/moda-feminina/{product_id}",
    response_model=EspecificacoesModaFeminina,
    status_code=status.HTTP_200_OK,
    description="Get product by ID",
    name="Route get product by ID"
)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    
    # Tenta pegar produto pelo redis
    product_data = redis_client.get(f"produto_moda: {product_id}")

    if product_data:
        # Se encontrar no redis retorna
        logger.info(msg="Produto retornado do Redis")
        return json.loads(product_data)

    # senao encontrar, retorna do db
    product = db.query(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id).first()
    logger.info(msg="Produto encontrado no banco de dados!")

    if product:
        # converte de modelo SqlAlchemy para um dicionario
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "tax": product.tax,
            "stars": product.stars,
            "color": product.color,
            "size": product.size,
            "details": product.details,
            "category": product.category
        }

        # guarda no redis para melhorar performance d buscas
        redis_client.set(f"produto_moda: {product.id}", json.dumps(product_data))
        logger.info(msg="Produto armazenado no Redis")

        return product_data

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


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
    
    if product_delete:
        logger.info(msg="Produto deletado!")
        db.delete(product_delete)
        db.commit()
        #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
        # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500


    if product_delete is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")



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

    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        # Salva as alterações no banco de dados
        logger.info(msg="Produto atualizado")
        db.commit()
        db.refresh(product)
        return product


    if product is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    

