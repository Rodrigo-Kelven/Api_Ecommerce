from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Products_Moda_Feminina
from ecommerce.config.config import logger
import uuid
import json

from sqlalchemy.future import select


class ServiceModa:


    @staticmethod
    async def createFashionProductService(product, db):
        # Gera um UUID para o novo produto
        product_id = str(uuid.uuid4())

        # Cria uma instância do modelo com o UUID
        db_product = Products_Moda_Feminina(id=product_id, **product.dict())  # Adiciona o UUID ao modelo
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)

        return db_product
    

    @staticmethod
    async def getFashionProductInIntervalService(skip, limit, db):
        product_search = select(Products_Moda_Feminina).offset(skip).limit(limit)  # Usando o modelo SQLAlchemy

        # Executa a consulta de forma assíncrona
        result = await db.execute(product_search)

        # Obtém os resultados da consulta
        products = result.scalars().all()

        if products:
            logger.info(msg="Produtos de moda sendo listado!")
            products_listed = [Products_Moda_Feminina.from_orm(product) for product in products]
            return products_listed

        if not products:
            logger.info(msg="Nenhum produto de moda nao encontardo!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de moda encontrado!")
        

    @staticmethod
    async def getFashionProductWithParamsService(
        db, name, category, stars, color, 
        details, size, min_price, max_price,
        skip, limit
    ):
        query = select(Products_Moda_Feminina)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Products_Moda_Feminina.name.ilike(f"%{name}%"))

        if category:# Usando LIKE para categoria
            query = query.filter(Products_Moda_Feminina.category.ilike(f"%{category}%"))

        if stars:# Usando LIKE para stars
            query = query.filter(Products_Moda_Feminina.stars >= stars)
        
        if color:# Usando LIKE para cor
            query = query.filter(Products_Moda_Feminina.color.ilike(f"%{color}%"))

        if details:# Usando LIKE para detalhes
            query = query.filter(Products_Moda_Feminina.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Products_Moda_Feminina.size.ilike(f"%{size}%"))


        if min_price is not None:
            query = query.filter(Products_Moda_Feminina.price >= min_price)

        if max_price is not None:
            query = query.filter(Products_Moda_Feminina.price <= max_price)

        
        # Executa a consulta com paginação
        result = await db.execute(query.offset(skip).limit(limit))

        # Obtemos os produtos da consulta
        products = result.scalars().all()
        
        if products:
            logger.info(msg="Produtos de moda sendo listados!")
            products_listed = [Products_Moda_Feminina.from_orm(product) for product in products]
            return products_listed

        logger.info(msg="Nenhum produto de moda encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de moda encontrado!")
    

    @staticmethod
    async def getFashionProductByIdService(product_id, db):
        # Tenta pegar produto pelo redis
        product_data = redis_client.get(f"produto_moda:{product_id}")

        if product_data:
            # Se encontrar no redis retorna
            logger.info(msg="Produto retornado do Redis")
            return json.loads(product_data)

        # senao encontrar, retorna do db
        product = select(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product)
        product = result.scalars().first()


        if product:
            logger.info(msg="Produto encontrado no banco de dados!")
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

            # guarda no redis para melhorar performance das buscas
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_moda:{product.id}", 54000, json.dumps(product_data))
            logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")

            
            
            return product_data

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    

    @staticmethod
    async def deleteFashionProductByIdService(product_id, db):
        product_delete = select(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product = result.scalars().first()

        if product:
            logger.info(msg="Produto deletado!")
            await db.delete(product)
            await db.commit()
            #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
            # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500


        if product is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        
        
    @staticmethod
    async def updateFashionProductByIdService(product_id, db, product_data):
        product_update = select(Products_Moda_Feminina).filter(Products_Moda_Feminina.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Salva as alterações no banco de dados
            logger.info(msg="Produto atualizado")
            await db.commit()
            await db.refresh(product)
            return product


        if product is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
