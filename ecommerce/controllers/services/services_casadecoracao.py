from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Product_Casa_Decoracao
from ecommerce.auth.config.config import app_logger
import uuid
import json
from sqlalchemy.future import select


class ServicesCasaDecoracao:

    @staticmethod
    async def createDecorationProductService(product, db):
        product_id = str(uuid.uuid4())

        db_product = Product_Casa_Decoracao(id=product_id, **product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} cadastrado.")

        return db_product
    
    @staticmethod
    async def getDecorationProductInIntervalService(skip, limit, db):
        product_search = select(Product_Casa_Decoracao).offset(skip).limit(limit)

        # Executa a consulta de forma assíncrona
        result = await db.execute(product_search)

        # Obtém os resultados da consulta
        products = result.scalars().all()

        if products:
            app_logger.info(msg="Produtos Casa e Decoracao sendo listados")
            products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
            return products_listed

        if not products:
            app_logger.info(msg="Nenhum produto Casa e Decoracao inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def getDecorationProductWithParamsService(
        db, name, category, stars, color, details,
        size, min_price, max_price, skip, limit
    ):
        query = select(Product_Casa_Decoracao)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Product_Casa_Decoracao.name.ilike(f"%{name}%"))

        if category:# Usando LIKE para categoria
            query = query.filter(Product_Casa_Decoracao.category.ilike(f"%{category}%"))

        if stars:# Usando LIKE para stars
            query = query.filter(Product_Casa_Decoracao.stars >= stars)
        
        if color:# Usando LIKE para cor
            query = query.filter(Product_Casa_Decoracao.color.ilike(f"%{color}%"))

        if details:# Usando LIKE para detalhes
            query = query.filter(Product_Casa_Decoracao.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Product_Casa_Decoracao.size.ilike(f"%{size}%"))


        if min_price is not None:
            query = query.filter(Product_Casa_Decoracao.price >= min_price)

        if max_price is not None:
            query = query.filter(Product_Casa_Decoracao.price <= max_price)

        
        product = await db.execute(query.offset(skip).limit(limit))  # Usando o modelo SQLAlchemy

        # Obtemos os produtos da consulta
        products = product.scalars().all()

        if products:
            app_logger.info(msg="Produtos Casa e Decoracao sendo listados!")
            products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
            return products_listed

        app_logger.info(msg="Nenhum produto de casa e decoracao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de casa e decoracao encontrado!")
    

    @staticmethod
    async def getDecorationProductByIdService(product_id, db):
        product_data = redis_client.get(f"produto_casa_decoracao:{product_id}")

        if product_data:
            app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} retornado do Redis!")
            return json.loads(product_data)


        product = select(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id)  # Usando o modelo de SQLAlchemy
        
        # Executa a consulta assíncrona
        result = await db.execute(product)
        products = result.scalars().first()
        
        if products:
            app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} encontrado no Banco de dados")
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
            app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_casa_decoracao:{products.id}", 54000, json.dumps(product_data))
            app_logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product
        

        if products is None:
            app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def deleteDecorationProductByIdService(product_id, db):
        product_delete = select(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product = result.scalars().first()

        if product:
            await db.delete(product)
            await db.commit()
            app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} deletado!")
            #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
            # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def updateDecorationProductByIdService(product_id, db, product_data):
    
        product_update = select(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            # Atualiza os campos do produto com os dados recebidos
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Salva as alterações no banco de dados
            db.commit()
            db.refresh(product)
            app_logger.info(msg=f"Produto Casa e Decoracao de id: {product_id} atualizado")
            return product


        # Verifica se o produto existe
        if product is None:
            app_logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        