from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.models.ecommerce.models import Product_Casa_Decoracao
from ecommerce.config.config import logger
import uuid
import json



class ServicesCasaDecoracao:

    @staticmethod
    async def create_product(product, db):
        product_id = str(uuid.uuid4())

        db_product = Product_Casa_Decoracao(id=product_id, **product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product
    
    @staticmethod
    async def get_products(skip, limit, db):
        products = db.query(Product_Casa_Decoracao).offset(skip).limit(limit).all()
    
        if products:
            logger.info(msg="Produtos sendo listados")
            products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
            return products_listed

        if not products:
            logger.info(msg="Nenhum produto inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def get_product_params(
        db, name, category, stars, color, details,
        size, min_price, max_price, skip, limit
    ):
        query = db.query(Product_Casa_Decoracao)

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

        
        products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

        if products:
            logger.info(msg="Produtos de moda sendo listados!")
            products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
            return products_listed

        logger.info(msg="Nenhum produto de casa e decoracao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de casa e decoracao encontrado!")
    

    @staticmethod
    async def get_product_id(product_id, db):
        product_data = redis_client.get(f"produto_casa_decoracao:{product_id}")

        if product_data:
            logger.info(msg="Produto retornado do Redis!")
            return json.loads(product_data)


        products = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()  # Usando o modelo de SQLAlchemy
        
        
        if products:
            logger.info(msg="Produto encontrado no Banco de dados")
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
            logger.info(msg="Produto inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_casa_decoracao:{products.id}", 54000, json.dumps(product_data))
            logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product
        

        if products is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def delete_product_id(product_id, db):
        product_delete = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()
        
        if product_delete:
            db.delete(product_delete)
            db.commit()
            logger.info(msg="Produto deletado!")
            #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
            # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500

        if product_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def update_product_id(product_id, db, product_data):
    
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
        