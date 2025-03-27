from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.models.ecommerce.models import Product_Esporte_Lazer
from ecommerce.config.config import logger
import uuid
import json



class ServicesEsportLazer:


    @staticmethod
    async def create_product(product, db):
        product_id = str(uuid.uuid4())

        db_product = Product_Esporte_Lazer(id=product_id, **product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product
    
    @staticmethod
    async def get_all_products(skip, limit, db):
        products = db.query(Product_Esporte_Lazer).offset(skip).limit(limit).all()
        
        if products:
            products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
            logger.info(msg="Produtos sendo listado!")
            return products_listed

        if not products:
            logger.info(msg="Nenhum  produto inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def get_product(
        db, name, category, stars, color,
        details, size, min_price, max_price, skip, limit
    ):
        query = db.query(Product_Esporte_Lazer)

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

        
        products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

        if products:
            logger.info(msg="Produtos de esporte e lazer sendo listados!")
            products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
            return products_listed

        logger.info(msg="Nenhum produto de moda encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de esporte e lazer encontrado!")
    
    @staticmethod
    async def get_product_id(db, product_id):
        product_data = redis_client.get(f"produto_esporte_lazer:{product_id}")

        if product_data:
            logger.info(msg="Produto retornado do Redis!")
            return json.loads(product_data)
        

        products = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()
        

        if products:
            logger.info(msg="Produto encontrado no Banco de dados!")
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
            logger.info(msg="Produto inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_esporte_lazer:{products.id}", 54000, json.dumps(product_data))
            logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return products_listed
        
        if not products:
            logger.info("Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        
    @staticmethod
    async def delete_product(product_id, db):
        product_delete = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()
        
        if product_delete:
            db.delete(product_delete)
            db.commit()


        if product_delete is None:
            logger.info(msg="Produto nao encontado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        
    @staticmethod
    async def update_product(product_id, product_data, db):
        product = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()

        if product:
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Corrige o valor da categoria se necessário
            #product.category = "Esporte_Lazer"  

            # Salva as alterações no banco de dados
            db.commit()
            db.refresh(product)
            return product

        
        if product is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        