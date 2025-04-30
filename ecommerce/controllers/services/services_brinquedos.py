from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import redis_client
from ecommerce.models.ecommerce.models import Product_Brinquedos_Jogos
from ecommerce.config.config import app_logger
import uuid
import json
from sqlalchemy.future import select


class Servico_Brinquedos_Jogos:


    @staticmethod
    async def createToyProductService(product, db):
        product_id = str(uuid.uuid4())

        product = Product_Brinquedos_Jogos(id=product_id, **product.dict())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        app_logger.info(msg=f"Produto brinquedo com  id: {product_id} cadastrado.")

        return product
    

    @staticmethod
    async def getToyProductInIntervalService(skip, limit, db):
        product_search = select(Product_Brinquedos_Jogos).offset(skip).limit(limit)

        # Executa a consulta de forma assíncrona
        result = await db.execute(product_search)

        # Obtém os resultados da consulta
        products = result.scalars().all()

        if products:
            app_logger.info(msg="Produtos brinquedos sendo listados!")
            products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
            return products_listed
        
        if not products:
            app_logger.info(msg="Nenhum produto brinquedo inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def getToyProductWithParamsService(
        db, name, category, stars, color, details,
        size, min_price, max_price, skip, limit
    ):
        # sessao de anotacoes
        """
        Uso de ilike: O método ilike é usado para realizar uma busca insensível a maiúsculas e minúsculas.
        O padrão f"%{category}%" permite que a pesquisa encontre qualquer categoria que contenha a string fornecida.
        Por exemplo, se o usuário buscar "verão", ele encontrará categorias como "Moda de Verão", "Roupas de Verão", etc.

        Flexibilidade: Isso torna a pesquisa mais flexível,
        permitindo que os usuários encontrem produtos que correspondam a partes de strings em vez de uma correspondência exata.

        """
        query = select(Product_Brinquedos_Jogos)

        # Aplicar filtros se fornecidos
        # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
        if name:
            query = query.filter(Product_Brinquedos_Jogos.name.ilike(f"%{name}%"))

        if category:# Usando LIKE para categoria
            query = query.filter(Product_Brinquedos_Jogos.category.ilike(f"%{category}%"))

        if stars:# Usando LIKE para stars
            query = query.filter(Product_Brinquedos_Jogos.stars >= stars)
        
        if color:# Usando LIKE para cor
            query = query.filter(Product_Brinquedos_Jogos.color.ilike(f"%{color}%"))

        if details:# Usando LIKE para detalhes
            query = query.filter(Product_Brinquedos_Jogos.details.ilike(f"%{details}%"))

        if size:# Usando LIKE para tamanho
            query = query.filter(Product_Brinquedos_Jogos.size.ilike(f"%{size}%"))


        if min_price is not None:
            query = query.filter(Product_Brinquedos_Jogos.price >= min_price)

        if max_price is not None:
            query = query.filter(Product_Brinquedos_Jogos.price <= max_price)

        
        product = await db.execute(query.offset(skip).limit(limit))  # Usando o modelo SQLAlchemy

        # Obtemos os produtos da consulta
        products = product.scalars().all()
        
        if products:
            app_logger.info(msg="Produtos de brinquedo listados!")
            products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
            return products_listed

        app_logger.info(msg="Nenhum produto de brinquedo encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de brinquedo e jogos encontrado!")
    

    @staticmethod
    async def getToyProductByIdService(product_id, db):
        product_data = redis_client.get(f"produto_brinquedos_jogos:{product_id}")

        if product_data:
            app_logger.info(msg="Produto brinquedos retornado do Redis!")
            return json.loads(product_data)


        product = select(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product)
        products = result.scalars().first()

        if products:
            app_logger.info(msg="Produto brinquedo encontrado no banco de dados!")
            product = Product_Brinquedos_Jogos.from_orm(products)

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
                "category": 'Brinquedos_Jogos'
            }
            app_logger.info(msg="Produto brinquedos inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_brinquedos_jogos:{products.id}", 54000, json.dumps(product_data))
            app_logger.info(msg="Produto brinquedos armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product
        
        if not products:
            app_logger.info(msg="Produto brinquedos nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def deleteToyProductByIdService(product_id, db):
        product_delete = select(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id)
        
        # Executa a consulta assíncrona
        result = await db.execute(product_delete)
        product = result.scalars().first()

        if product:
            app_logger.info(msg="Produto brinquedo encontrado!")
            await db.delete(product)
            await db.commit()
            app_logger.info(msg=f"Produto brinquedo de id: {product_id} deletado!!")
            return f"Product with {product_id} removed succesfull"
        
        if product is None:
            app_logger.info(msg="Produto brinquedo nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    

    @staticmethod
    async def updateToyProductByIdService(product_id, product_data ,db):
        product_update = select(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id)

        # Executa a consulta assíncrona
        result = await db.execute(product_update)
        product = result.scalars().first()

        if product:
            # Atualiza os campos do produto com os dados recebidos
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Corrige o valor da categoria se necessário
            #product.category = "Beleza_e_cuidados"  

            # Salva as alterações no banco de dados
            db.commit()
            db.refresh(product)
            app_logger.info(msg=f"Produto brinquedo de id: {product_id} atualizado.")
            return product

        
        # Verifica se o produto existe
        if product is None:
            app_logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        