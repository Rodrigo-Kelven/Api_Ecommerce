from ecommerce.schemas.ecommerce.schemas import EspecificacoesCasaeDecoracao, ProductCasaeDecoracao, ProductBase
from ecommerce.models.ecommerce.models import Product_Casa_Decoracao
from fastapi import APIRouter, status, Body, Depends, HTTPException
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json


route_cada_decoracao = APIRouter()



@route_cada_decoracao.post(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Create product home and decorations",
    name="Route create product",
    )
async def create_product(product: ProductCasaeDecoracao = Body(embed=True), db: Session = Depends(get_db)):
    db_product = Product_Casa_Decoracao(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product



@route_cada_decoracao.get(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesCasaeDecoracao],
    description="List all products",
    name="Route list products"
)
async def list_products(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    products = db.query(Product_Casa_Decoracao).offset(skip).limit(limit).all()
    
    if products:
        logger.info(msg="Produtos sendo listados")
        products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
        return products_listed

    if not products:
        logger.info(msg="Nenhum produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
    


@route_cada_decoracao.get(
    path="/category/casa-e-decoracao/{product_id}",
    response_model=EspecificacoesCasaeDecoracao,
    status_code=status.HTTP_200_OK,
    description="Search product with ID",
    name="Route search product with ID"
)
async def search_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_data = redis_client.get(f"produto_casa_decoracao: {product_id}")

    if product_data:
        logger.info(msg="Produto retornado do Redis!")
        return json.loads(product_data)


    products = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()  # Usando o modelo de SQLAlchemy
    logger.info(msg="Produto encontrado no Banco de dados")
    
    if products:
        logger.info(msg="Produto encontrado!")
        product = Product_Casa_Decoracao.from_orm(products)

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
            "category": 'Casa-e-decoracao'
        }
        redis_client.set(f"produto_casa_decoracao: {products.id}", json.dumps(product_data))
        logger.info(msg="Produto armazenado no Redis")
        
        return product
    

    if products is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")




@route_cada_decoracao.delete(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
)
async def delete_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()
    
    if product_delete:
        db.delete(product_delete)
        db.commit()
        logger.info(msg="Produto deletado!")
        #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
        # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500

    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")




@route_cada_decoracao.put(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Route for update products",
    name="Route create product"
)
async def update_product(
    product_id: int,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True)
    ):
    product = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()

    if product:
        # Atualiza os campos do produto com os dados recebidos
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(product)
        logger.info(msg="Produto atualizado")
        return product


    # Verifica se o produto existe
    if product is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    