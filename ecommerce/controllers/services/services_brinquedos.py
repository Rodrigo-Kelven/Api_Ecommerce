from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.models.ecommerce.models import Product_Brinquedos_Jogos
from ecommerce.config.config import logger
import uuid
import json


class Servico_Brinquedos_Jogos:


    @staticmethod
    async def createToyProduct(product, db):
        product_id = str(uuid.uuid4())

        product = Product_Brinquedos_Jogos(id=product_id, **product.dict())
        db.add(product)
        db.commit()
        db.refresh(product)

        return product
    

    @staticmethod
    async def getToyProductInInterval(skip, limit, db):
        products = db.query(Product_Brinquedos_Jogos).offset(skip).limit(limit).all()

        if products:
            logger.info(msg="Produtos sendo listados!")
            products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
            return products_listed
        
        if not products:
            logger.info(msg="Nenhum produto inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def getToyProductWithParams(
        db, name, category, stars, color, details,
        size, min_price, max_price, skip, limit
    ):
        query = db.query(Product_Brinquedos_Jogos)

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

        
        products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

        if products:
            logger.info(msg="Produtos de brinquedo e jogos listados!")
            products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
            return products_listed

        logger.info(msg="Nenhum produto de moda encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de brinquedo e jogos encontrado!")
    

    @staticmethod
    async def getToyProductById(product_id, db):
        product_data = redis_client.get(f"produto_brinquedos_jogos:{product_id}")

        if product_data:
            logger.info(msg="Produto retornado do Redis!")
            return json.loads(product_data)


        products = db.query(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id).first()
        

        if products:
            logger.info(msg="Produto encontrado no banco de dados!")
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
            logger.info(msg="Produto inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_brinquedos_jogos:{products.id}", 54000, json.dumps(product_data))
            logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product
        
        if not products:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        

    @staticmethod
    async def deleteToyProductById(product_id, db):
        product_delete = db.query(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id).first()
        
        if product_delete:
            logger.info(msg="Produto encontrado!")
            db.delete(product_delete)
            db.commit()
            print("Produto deletado!!")
            return f"Product with {product_id} removed succesfull"
        
        if product_delete is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    

    @staticmethod
    async def updateToyProductById(product_id, product_data ,db):
        product = db.query(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id).first()
    
        if product:
            # Atualiza os campos do produto com os dados recebidos
            for key, value in product_data.dict().items():
                setattr(product, key, value)

            # Corrige o valor da categoria se necessário
            #product.category = "Beleza_e_cuidados"  

            # Salva as alterações no banco de dados
            db.commit()
            db.refresh(product)
            return product

        
        # Verifica se o produto existe
        if product is None:
            logger.info(msg="Produto nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
        