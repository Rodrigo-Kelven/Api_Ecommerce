from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Product_Esporte_Lazer
from ecommerce.config.config import app_logger
import uuid
import json

from sqlalchemy.future import select


class ServicesEsportLazer:


    @staticmethod
    async def createSportProductService(product, db):
        product_id = str(uuid.uuid4())

        db_product = Product_Esporte_Lazer(id=product_id, **product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        app_logger.info(msg=f"Produto Esporte de id: {product_id} cadastrado.")

        return db_product
    
    @staticmethod
    async def getSportProductInIntervalService(skip, limit, db):
        product_search = select(Product_Esporte_Lazer).offset(skip).limit(limit)
        
        # Executa a consulta de forma assíncrona
        result = await db.execute(product_search)

        # Obtém os resultados da consulta
        products = result.scalars().all()

        if products:
            products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
            app_logger.info(msg="Produto Esporte sendo listado!")
            return products_listed

        if not products:
            app_logger.info(msg="Nenhum Produto Esporte inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def getSportProductWithParamsService(
        db, name, category, stars, color,
        details, size, min_price, max_price, skip, limit
    ):
        # sessao de anotacoes
        """
        Uso de ilike: O método ilike é usado para realizar uma busca insensível a maiúsculas e minúsculas.
        O padrão f"%{category}%" permite que a pesquisa encontre qualquer categoria que contenha a string fornecida.
        Por exemplo, se o usuário buscar "verão", ele encontrará categorias como "Moda de Verão", "Roupas de Verão", etc.

        Flexibilidade: Isso torna a pesquisa mais flexível,
        permitindo que os usuários encontrem produtos que correspondam a partes de strings em vez de uma correspondência exata.

        """
        query = select(Product_Esporte_Lazer)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Product_Esporte_Lazer.name.ilike(f"%{name}%"))

        if category: # Usando LIKE para categoria
            query = query.filter(Product_Esporte_Lazer.category.ilike(f"%{category}%"))

        if stars:# Usando LIKE star
            query = query.filter(Product_Esporte_Lazer.stars >= stars)
        
        if color:# Usando LIKE para cor
            query = query.filter(Product_Esporte_Lazer.color.ilike(f"%{color}%"))

        if details:# Usando LIKE para detalhes
            query = query.filter(Product_Esporte_Lazer.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Product_Esporte_Lazer.size.ilike(f"%{size}%"))


        if min_price is not None:
            query = query.filter(Product_Esporte_Lazer.price >= min_price)

        if max_price is not None:
            query = query.filter(Product_Esporte_Lazer.price <= max_price)

        
        product = await db.execute(query.offset(skip).limit(limit))  # Usando o modelo SQLAlchemy

        # Obtemos os produtos da consulta
        products = product.scalars().all()

        if products:
            app_logger.info(msg="Produtos de esporte e lazer sendo listados!")
            products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
            return products_listed

        app_logger.info(msg="Nenhum produto de esporte encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de esporte e lazer encontrado!")
    

    @staticmethod
    async def getSportProductByIdService(db, product_id):
        product_data = redis_client.get(f"produto_esporte_lazer:{product_id}")

        if product_data:
            app_logger.info(msg=f"Produto Esporte de id: {product_id} retornado do Redis!")
            return json.loads(product_data)
        

        product = select(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product)
        products = result.scalars().first()

        if products:
            app_logger.info(msg=f"Produto Esporte de id: {product_id} encontrado no Banco de dados!")
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
            app_logger.info(msg=f"Produto Esporte de id: {product_id} inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_esporte_lazer:{products.id}", 54000, json.dumps(product_data))
            app_logger.info(msg=f"Produto Esporte de id: {product_id} armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return products_listed
        
        if not products:
            app_logger.info(msg=f"Produto Esporte de id: {product_id} nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def deleteSportProductByIdService(product_id, db):
        product_delete = select(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product = result.scalars().first()

        if product:
            await db.delete(product)
            await db.commit()
            app_logger.info(msg=f"Produto Esporte de id: {product_id} deletado.")


        if product is None:
            app_logger.info(msg=f"Produto Esporte de id: {product_id} nao encontado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def updateSportProductByIdService(product_id, product_data, db):
        product_update = select(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Corrige o valor da categoria se necessário
            #product.category = "Esporte_Lazer"  

            # Salva as alterações no banco de dados
            await db.commit()
            await db.refresh(product)
            app_logger.info(msg="fProduto Esporte de id: {product_id} atualizado")
            
            return product

        
        if product is None:
            app_logger.info(msg=f"Produto Esporte de id: {product_id} nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        