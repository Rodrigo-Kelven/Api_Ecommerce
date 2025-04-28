from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Product_Livros_Papelaria
from ecommerce.config.config import logger
import uuid
import json

from sqlalchemy.future import select

class ServicesLivraria:


    @staticmethod
    async def createLibraryProductService(product, db):
        product_id = str(uuid.uuid4())

        db_product = Product_Livros_Papelaria(id=product_id, **product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product
    

    @staticmethod
    async def getLibraryProductInIntervalService(skip, limit, db):
        db_product = select(Product_Livros_Papelaria).offset(skip).limit(limit)

        # Executa a consulta de forma assíncrona
        result = await db.execute(db_product)

        # Obtém os resultados da consulta
        products = result.scalars().all()
        
        if products:
            logger.info(msg="Produtos de papelaria sendo listado!")
            products_listed = [Product_Livros_Papelaria.from_orm(product) for product in products]
            return products_listed
        
        if not products:
            logger.info(msg="Nenhum produto de papelaria inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de papelaria inserido!")
        

    @staticmethod
    async def getLibraryProductWithParamsService(
        db, name, category, stars, color,
        details, size, min_price, max_price, skip, limit
    ):
        query = select(Product_Livros_Papelaria)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Product_Livros_Papelaria.name.ilike(f"%{name}%"))

        if category:# Usando LIKE para categoria
            query = query.filter(Product_Livros_Papelaria.category.ilike(f"%{category}%")) 

        if stars:# Usando LIKE para stars
            query = query.filter(Product_Livros_Papelaria.stars >= stars)
        
        if color: # Usando LIKE para cor
            query = query.filter(Product_Livros_Papelaria.color.ilike(f"%{color}%")) 

        if details: # Usando LIKE para detalhes
            query = query.filter(Product_Livros_Papelaria.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Product_Livros_Papelaria.size.ilike(f"%{size}%"))  


        if min_price is not None:
            query = query.filter(Product_Livros_Papelaria.price >= min_price)

        if max_price is not None:
            query = query.filter(Product_Livros_Papelaria.price <= max_price)

        
        result = await db.execute(query.offset(skip).limit(limit)) # Usando o modelo SQLAlchemy

        # Obtemos os produtos da consulta
        products = result.scalars().all()


        if products:
            logger.info(msg="Produtos de papelaria sendo listados!")
            products_listed = [Product_Livros_Papelaria.from_orm(product) for product in products]
            return products_listed

        logger.info(msg="Nenhum produto de papelaria encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto papelaria encontrado!")
    

    @staticmethod
    async def getLibraryProductByIdService(product_id, db):
        product_data = redis_client.get(f"produto_livraria:{product_id}")

        if product_data:
            logger.info(msg="Produto retornado do Redis!")
            return json.loads(product_data)
        
        db_product = select(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(db_product)
        db_product = result.scalars().first()

        if db_product:
            logger.info(msg="Produto encontrado no banco de dados!")
            product = Product_Livros_Papelaria.from_orm(db_product)

            product_data = {
                "id": db_product.id,
                "name": db_product.name,
                "description": db_product.description,
                "price": db_product.price,
                "quantity": db_product.quantity,
                "tax": db_product.tax,
                "stars": db_product.stars,
                "color": db_product.color,
                "size": db_product.size,
                "details": db_product.details,
                "category": "Livros_Papelaria"
            }
            logger.info(msg="Produto inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_livraria:{db_product.id}", 54000, json.dumps(product_data))
            logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product

        if db_product is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def deleteLibraryProductByIdService(product_id, db):
        product_delete = select(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product_delete = result.scalars().first()

        if product_delete:
            logger.info(msg="Produto encontrado!")
            await db.delete(product_delete)
            await db.commit()
            print("Produto deletado!!")
            return f"Product with {product_id} removed succesfull"

        if product_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")


    @staticmethod
    async def updateLibraryProductByIdService(product_id, db, product_data):
        product_update = select(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Corrige o valor da categoria se necessário
            #product.category = "Livros_Papelaria"  

            # Salva as alterações no banco de dados
            await db.commit()
            await db.refresh(product)
            return product


        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        