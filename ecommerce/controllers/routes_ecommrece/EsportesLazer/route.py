from ecommerce.schemas.ecommerce.schemas import ProductEsporteLazer, EspecificacoesEsporteLazer, ProductBase
from fastapi import APIRouter, status, HTTPException, Body, Depends
from ecommerce.models.ecommerce.models import Product_Esporte_Lazer
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json

route_esporte_lazer = APIRouter()



@route_esporte_lazer.post(
    path="/category/esporte-lazer/product",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
async def create_product(
    product: ProductEsporteLazer = Body(embed=True),
    db: Session = Depends(get_db)
):
    db_product = Product_Esporte_Lazer(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product



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
    products = db.query(Product_Esporte_Lazer).offset(skip).limit(limit).all()
    
    if products:
        products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
        logger.info(msg="Produtos sendo listado!")
        return products_listed

    if not products:
        logger.info(msg="Nenhum  produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")


@route_esporte_lazer.get(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route get product for ID",
    name="Route GET product for ID"
)
async def searchProduct_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_data = redis_client.get(f"produuto: {product_id}")

    if product_data:
        logger.info(msg="Produto pego do Redis")
        return json.loads(product_data)
    

    products = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()

    if products:
        logger.info(msg="Produto encontado!")
        products_listed = Product_Esporte_Lazer.from_orm(products)

        product_data = {
            "id": products.id,
            "name": products.name,
            "description": products.description,
            "price": products.price,
            "quantity": products.quantity,
            "tax": products.tax,
            "stars": products.stars,
            "color": products.color,
            "size": products.size,
            "details": products.details,
            "category": products.category
        }
        redis_client.set(f"produuto: {products.id}", json.dumps(product_data))
        logger.info(msg="Produto armazenado no Redis")


        return products_listed
    
    if not products:
        logger.info("Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")



@route_esporte_lazer.delete(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()
    
    if product_delete:
        db.delete(product_delete)
        db.commit()


    if product_delete is None:
        logger.info(msg="Produto nao encontado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")




@route_esporte_lazer.put(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route put product for ID",
    name="Route PUT product for ID"
)
async def update_products(
    product_id: int,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_db),
):
    product = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()

    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        # Corrige o valor da categoria se necessário
        #product.category = "Esporte_Lazer"  

        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(product)
        return product

    
    if product is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    
