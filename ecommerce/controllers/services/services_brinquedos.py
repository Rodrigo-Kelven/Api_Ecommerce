from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.models.ecommerce.models import Product_Brinquedos_Jogos
from ecommerce.config.config import logger
import uuid
import json


class Servico_Brinquedos_Jogos:


    @staticmethod
    async def create_produtc_brinq_jogos(product, db):
        product_id = str(uuid.uuid4())

        product = Product_Brinquedos_Jogos(id=product_id, **product.dict())
        db.add(product)
        db.commit()
        db.refresh(product)

        return product
    

    @staticmethod
    async def get_products_brinq_jogos(skip, limit, db):
        products = db.query(Product_Brinquedos_Jogos).offset(skip).limit(limit).all()

        if products:
            logger.info(msg="Produtos sendo listados!")
            products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
            return products_listed
        
        if not products:
            logger.info(msg="Nenhum produto inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
