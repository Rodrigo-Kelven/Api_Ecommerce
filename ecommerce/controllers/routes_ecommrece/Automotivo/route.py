from ecommerce.schemas.ecommerce.schemas import EspecificacoesAutomotivo, ProductAutomotivo, ProductBase
from fastapi import APIRouter, status, Depends, HTTPException, Body, Query
from ecommerce.models.ecommerce.models import Product_Automotivo
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json
import uuid


route_automotivo = APIRouter()


@route_automotivo.post(
    path="/category/automotivo",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesAutomotivo,
    response_description="Informations product",
    description="Route create product",
    name="Route Create product category"
)
async def create_product(
    product: ProductAutomotivo = Body(embed=True),
    db: Session = Depends(get_db)
):
    # gera uuid 
    product_id = str(uuid.uuid4())
    # coloca o uuid como id em formato str
    db_product = Product_Automotivo(id=product_id, **product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product



@route_automotivo.get(
    path="/category/automotivo",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesAutomotivo],
    response_description="Informations products",
    description="Route list products",
    name="Route list products category automotivo"
)
async def get_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    
    db_product = db.query(Product_Automotivo).offset(skip).limit(limit).all()

    if db_product:
        logger.info(msg="Produtos automotivos listados!")
        # Convert db_product (list of Product_Automotivo) to a list of Product_Automotivo
        products = [Product_Automotivo.from_orm(product) for product in db_product]
        return products
    
    if not db_product:
        logger.info(msg="Nenhum produto automotivo inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")


# rota de filtragem de buscas 
@route_automotivo.get(
    path="/category/automotivo/search-filters/",
    response_model=list[EspecificacoesAutomotivo],
    status_code=status.HTTP_200_OK,
    description="List search products",
    name="Route search products"
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



@route_automotivo.get(
    path="/category/automotivo/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesAutomotivo,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products for ID"
)
async def get_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
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




@route_automotivo.delete(
    path="/category/automotivo/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Information products",
    description="Route get product for id",
    name="Route DELETE products for ID"
)
async def delete_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Automotivo).filter(Product_Automotivo.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=404, detail="Produto nao encontrado!")
    db.delete(product_delete)
    db.commit()
    print("Produto deletado!!")
    return 



@route_automotivo.put(
    path="/category/automotivo/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesAutomotivo,
    description="Route PUT product",
    name="Route PUT product for ID"
)
async def update_product(
    product_id: str,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
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
