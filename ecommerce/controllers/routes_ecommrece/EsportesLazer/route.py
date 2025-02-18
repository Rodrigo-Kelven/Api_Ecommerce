from ecommerce.schemas.ecommerce.schemas import ProductEsporteLazer, EspecificacoesEsporteLazer, ProductBase
from fastapi import APIRouter, status, HTTPException, Body, Depends, Query
from ecommerce.models.ecommerce.models import Product_Esporte_Lazer
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json
import uuid


route_esporte_lazer = APIRouter()


@route_esporte_lazer.post(
    path="/category/esporte-lazer/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
async def create_product(
    product: ProductEsporteLazer = Body(embed=True),
    db: Session = Depends(get_db)
):
    product_id = str(uuid.uuid4())

    db_product = Product_Esporte_Lazer(id=product_id, **product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product



@route_esporte_lazer.get(
    path="/category/esporte-lazer/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesEsporteLazer],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products"
)
async def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    products = db.query(Product_Esporte_Lazer).offset(skip).limit(limit).all()
    
    if products:
        products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
        logger.info(msg="Produtos sendo listado!")
        return products_listed

    if not products:
        logger.info(msg="Nenhum  produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")


# rota de filtragem de buscas 
@route_esporte_lazer.get(
    path="/category/esporte-lazer/search-filters/",
    response_model=list[EspecificacoesEsporteLazer],
    status_code=status.HTTP_200_OK,
    description="List all products",
    name="Route list products"
)
def read_products(
    category: str = Query(None, description="Filtrar por categoria"),
    min_price: float = Query(None, description="Filtrar por preço mínimo"),
    max_price: float = Query(None, description="Filtrar por preço máximo"),
    name: str = Query(None, description="Filtrar por nome"),
    stars: int = Query(None, description="Filtrar por quantidade de estrelas"),
    color: str = Query(None, description="Filtrar pela cor"),
    size: float = Query(None, description="Filtrar pelo tamanho"),
    details: str = Query(None, description="Filtrar por detalhes"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Product_Esporte_Lazer)

    # Aplicar filtros se fornecidos
    # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
    if name:
        query = query.filter(Product_Esporte_Lazer.name.ilike(f"%{name}%"))

    if category: 
        query = query.filter(Product_Esporte_Lazer.category.ilike(f"%{category}%"))  # Usando LIKE

    if stars:
        query = query.filter(Product_Esporte_Lazer.stars >= stars)
    
    if color:
        query = query.filter(Product_Esporte_Lazer.color.ilike(f"%{color}%"))  # Usando LIKE para cor

    if details:
        query = query.filter(Product_Esporte_Lazer.details.ilike(f"%{details}%"))

    if size:
        query = query.filter(Product_Esporte_Lazer.size.ilike(f"%{size}%"))  # Usando LIKE para tamanho


    if min_price is not None:
        query = query.filter(Product_Esporte_Lazer.price >= min_price)

    if max_price is not None:
        query = query.filter(Product_Esporte_Lazer.price <= max_price)

    
    products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

    if products:
        logger.info(msg="Produtos de moda sendo listados!")
        products_listed = [Product_Esporte_Lazer.from_orm(product) for product in products]
        return products_listed

    logger.info(msg="Nenhum produto de moda encontrado!")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de moda encontrado!")



@route_esporte_lazer.get(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route get product for ID",
    name="Route GET product for ID"
)
async def searchProduct_id(
    product_id: str,
    db: Session = Depends(get_db)
):
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



@route_esporte_lazer.delete(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Esporte_Lazer).filter(Product_Esporte_Lazer.id == product_id).first()
    
    if product_delete:
        db.delete(product_delete)
        db.commit()


    if product_delete is None:
        logger.info(msg="Produto nao encontado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")




@route_esporte_lazer.put(
    path="/category/esporte-lazer/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesEsporteLazer,
    response_description="Informations Products",
    description="Route put product for ID",
    name="Route PUT product for ID"
)
async def update_products(
    product_id: str,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_db),
):
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
    
