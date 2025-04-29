from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Product_Automotivo
from ecommerce.auth.config.config import app_logger
import uuid
import json

from sqlalchemy.future import select


class Services_Automotivo:

    @staticmethod
    async def createAutomotiveProductService(product, db):
        # gera uuid 
        product_id = str(uuid.uuid4())
        # coloca o uuid como id em formato str
        db_product = Product_Automotivo(id=product_id, **product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        app_logger.info(msg=f"Produto automotivo com  id: {product_id} cadastrado.")

        return db_product
    
    @staticmethod
    async def getAutomotiveProductsInIntervalService(skip, limit, db):
        product_search = select(Product_Automotivo).offset(skip).limit(limit)

        # Executa a consulta de forma assíncrona
        result = await db.execute(product_search)

        # Obtém os resultados da consulta
        products = result.scalars().all()

        if products:
            app_logger.info(msg="Produtos automotivos listados!")
            # Convert db_product (list of Product_Automotivo) to a list of Product_Automotivo
            products = [Product_Automotivo.from_orm(product) for product in products]
            return products
        
        if not products:
            app_logger.info(msg="Nenhum produto automotivo inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def getAutomotiveProductWithParamsService(
        name, category, stars, color, details,
        size, min_price, max_price, skip, limit, db
    ):
        query = select(Product_Automotivo)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Product_Automotivo.name.ilike(f"%{name}%"))

        if category: # Usando LIKE para categoria
            query = query.filter(Product_Automotivo.category.ilike(f"%{category}%"))

        if stars:# Usando LIKE para stard
            query = query.filter(Product_Automotivo.stars >= stars)
        
        if color:# Usando LIKE para cor
            query = query.filter(Product_Automotivo.color.ilike(f"%{color}%"))

        if details:# Usando LIKE para detalhes
            query = query.filter(Product_Automotivo.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Product_Automotivo.size.ilike(f"%{size}%"))


        if min_price is not None:
            query = query.filter(Product_Automotivo.price >= min_price)

        if max_price is not None:
            query = query.filter(Product_Automotivo.price <= max_price)

        
        product = await db.execute(query.offset(skip).limit(limit))  # Usando o modelo SQLAlchemy

        # Obtemos os produtos da consulta
        products = product.scalars().all()

        if products:
            app_logger.info(msg="Produtos de automotivo sendo listados!")
            products_listed = [Product_Automotivo.from_orm(product) for product in products]
            return products_listed

        app_logger.info(msg="Nenhum produto automotivo encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto automotivo encontrado!")
    

    @staticmethod
    async def getAutomotiveProductByIdService(product_id, db):
        # primeiro procura no redis
        product_data = redis_client.get(f"produto_automotivo:{product_id}")

        # retorna do redis se tiver no redis
        if product_data:
            app_logger.info(msg=f"Produto de id: {product_id} retornado do Redis!")
            return json.loads(product_data)
        
        # senao, procura no db e retorna
        product = select(Product_Automotivo).filter(Product_Automotivo.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product)
        product = result.scalars().first()

        # no db, procura se existir, e transforma para ser armazenado no redis
        if product:
            app_logger.info(msg=f"Produto de id: {product_id} encontrado no Banco de dados")
            product_listed = Product_Automotivo.from_orm(product)

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
            app_logger.info(msg=f"Produto de id: {product_id} inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_automotivo:{product.id}", 54000, json.dumps(product_data))
            app_logger.info(msg=f"Produto de id: {product_id} armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product_listed


        if product is None:
            app_logger.info(msg="Produto automotivo nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto automotivo nao encontrado!")
        

    @staticmethod
    async def deleteAutomotiveProductByIdService(product_id, db):
        product_delete = select(Product_Automotivo).filter(Product_Automotivo.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product = result.scalars().first()

        if product:
            await db.delete(product)
            app_logger.info(msg=f"Produto de id: {product_id} automotivo deletado!")
            await db.commit()

        if product is None:
            app_logger.info(msg=f"Produto de id: {product_id} nao encontado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        
    

    @staticmethod
    async def updateAutomotiveProductByIdService(product_id, db, product_data):
        product_update = select(Product_Automotivo).filter(Product_Automotivo.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Salva as alterações no banco de dados
            await db.commit()
            await db.refresh(product)
            app_logger.info(msg=f"Produto de id: {product_id} atualizado!")
            return product

        # Verifica se o produto existe
        if product is None:
            app_logger.info(msg=f"Produto de id: {product_id} nao encontrado!")
            raise HTTPException(status_code=404, detail="Produto nao encontado!")

        