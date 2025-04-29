from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Products_Eletronics
from ecommerce.auth.config.config import app_logger
import uuid
import json

from sqlalchemy.future import select


class ServicesEletronics:

    @staticmethod
    async def createEletronicProductService(product, db):

        product_id = str(uuid.uuid4())

        db_product = Products_Eletronics(id=product_id, **product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        app_logger.info(msg=f"Produto com  id: {product_id} cadastrado.")

        return db_product
    

    @staticmethod
    async def getEletronicProductInIntervalService(skip, limit, db):
        product_search = select(Products_Eletronics).offset(skip).limit(limit)  # Usando o modelo SQLAlchemy
        
        # Executa a consulta de forma assíncrona
        result = await db.execute(product_search)

        # Obtém os resultados da consulta
        products = result.scalars().all()

        if products:
            app_logger.info(msg="Produtos eletronicos listados!")
            products_listados = [Products_Eletronics.from_orm(product) for product in products]
            return products_listados
        
        if not products:
            app_logger.info(msg="Nenhum produto eletronico inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto eletronico inserido!")
        

    @staticmethod
    async def getEletronicProductWithParamsService(
        db, category, name, stars, color,
        details, size,min_price, max_price,
        skip, limit
    ):
        query = select(Products_Eletronics)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Products_Eletronics.name.ilike(f"%{name}%"))

        if category: # Usando LIKE para categorya
            query = query.filter(Products_Eletronics.category.ilike(f"%{category}%"))

        if stars:# Usando LIKE para start
            query = query.filter(Products_Eletronics.stars >= stars)
        
        if color:# Usando LIKE para cor
            query = query.filter(Products_Eletronics.color.ilike(f"%{color}%"))

        if details:# Usando LIKE para detalhes
            query = query.filter(Products_Eletronics.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Products_Eletronics.size.ilike(f"%{size}%"))


        if min_price is not None:
            query = query.filter(Products_Eletronics.price >= min_price)

        if max_price is not None:
            query = query.filter(Products_Eletronics.price <= max_price)

        
        product = await db.execute(query.offset(skip).limit(limit))  # Usando o modelo SQLAlchemy

        # Obtemos os produtos da consulta
        products = product.scalars().all()

        if products:
            app_logger.info(msg="Produtos de moda sendo listados!")
            products_listed = [Products_Eletronics.from_orm(product) for product in products]
            return products_listed

        app_logger.info(msg="Nenhum produto de eletronicos encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de eletronicos encontrado!")
    

    @staticmethod
    async def getEletronicProductByIdService(product_id, db):
        # primeiro procura no redis
        product_data = redis_client.get(f"produto_eletronicos:{product_id}")

        # retorna do redis se tiver no redis
        if product_data:
            app_logger.info(msg="Produto retornado do Redis!")
            return json.loads(product_data)
        
        # senao, procura no db e retorna
        product = select(Products_Eletronics).filter(Products_Eletronics.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product)
        product = result.scalars().first()

        # no db, procura se existir, e transforma para ser armazenado no redis
        if product:
            app_logger.info(msg="Produto encontrado no Banco de dados!")
            product_listed = Products_Eletronics.from_orm(product)

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
                "category": "Eletronicos"
            }
            app_logger.info(msg="Produto inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_eletronicos:{product.id}", 54000, json.dumps(product_data))
            app_logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product_listed


        if product is None:
            app_logger.info(msg="Produto eletronico nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto eletronico nao encontrado!")
        

    @staticmethod
    async def deleteEletronicProductByIdService(product_id, db):
        product_delete = select(Products_Eletronics).filter(Products_Eletronics.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product = result.scalars().first()

        if product:
            app_logger.info(msg="Produto eletronico deletado")
            await db.delete(product)
            await db.commit()
            #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
            # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto eletronico nao encontrado!")
        

    @staticmethod
    async def updateEletronicProductByIdService(product_id, db, product_data):
        product_update = select(Products_Eletronics).filter(Products_Eletronics.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            app_logger.info(msg="Produto eletronico encontrado!")
            for key, value in product_data.dict().items():
                setattr(product, key, value)
            app_logger.info(msg="Produto eletronico atualizado")

            db.commit()
            db.refresh(product)
            return product
        
        if product is None:
            app_logger.info(msg="Produto eletronico nao encontrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto eletronico nao encontrado!")

        # Corrige o valor da categoria se necessário
        #product.category = "Eletronicos"  # Defina o valor da categoria como "Eletronicos"

