from fastapi import HTTPException, status
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.models.ecommerce.models import Product_Automotivo
from ecommerce.config.config import logger
import uuid
import json



class Services_Automotivo:

    @staticmethod
    async def createAutomotiveProduct(product, db):
        # gera uuid 
        product_id = str(uuid.uuid4())
        # coloca o uuid como id em formato str
        db_product = Product_Automotivo(id=product_id, **product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product
    
    @staticmethod
    async def getAutomotiveProductsInInterval(skip, limit, db):
        db_product = db.query(Product_Automotivo).offset(skip).limit(limit).all()

        if db_product:
            logger.info(msg="Produtos automotivos listados!")
            # Convert db_product (list of Product_Automotivo) to a list of Product_Automotivo
            products = [Product_Automotivo.from_orm(product) for product in db_product]
            return products
        
        if not db_product:
            logger.info(msg="Nenhum produto automotivo inserido!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
        

    @staticmethod
    async def getAutomotiveProductWithParams(
        name, category, stars, color, details,
        size, min_price, max_price, skip, limit, db
    ):
        query = db.query(Product_Automotivo)

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

        
        products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

        if products:
            logger.info(msg="Produtos de moda sendo listados!")
            products_listed = [Product_Automotivo.from_orm(product) for product in products]
            return products_listed

        logger.info(msg="Nenhum produto automotivo encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto automotivo encontrado!")
    

    @staticmethod
    async def getAutomotiveProductById(product_id, db):
        # primeiro procura no redis
        product_data = redis_client.get(f"produto_automotivo:{product_id}")

        # retorna do redis se tiver no redis
        if product_data:
            logger.info(msg="Produto retornado do Redis!")
            return json.loads(product_data)
        
        # senao, procura no db e retorna
        product = db.query(Product_Automotivo).filter(Product_Automotivo.id == product_id).first()
        

        # no db, procura se existir, e transforma para ser armazenado no redis
        if product:
            logger.info(msg="Produto encontrado no Banco de dados")
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
            logger.info(msg="Produto inserido no redis!")
            # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
            redis_client.setex(f"produto_automotivo:{product.id}", 54000, json.dumps(product_data))
            logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
            # retorna do db
            return product_listed


        if product is None:
            logger.info(msg="Produto automotivo nao encontrado!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto automotivo nao encontrado!")
        

    @staticmethod
    async def deleteAutomotiveProductById(product_id, db):
        product_delete = db.query(Product_Automotivo).filter(Product_Automotivo.id == product_id).first()
        if product_delete is None:
            raise HTTPException(status_code=404, detail="Produto nao encontrado!")
        db.delete(product_delete)
        db.commit()
        print("Produto deletado!!")
        return 
    

    @staticmethod
    async def updateAutomotiveProductById(product_id, db, product_data):
        product = db.query(Product_Automotivo).filter(Product_Automotivo.id == product_id).first()
        # Verifica se o produto existe
        if product is None:
            raise HTTPException(status_code=404, detail="Produto nao encontado!")
        
        # Atualiza os campos do produto com os dados recebidos
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        # Corrige o valor da categoria se necessário
        #product.category = "Automotivo"  

        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(product)
        return product