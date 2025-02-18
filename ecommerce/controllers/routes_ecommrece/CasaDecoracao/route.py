from ecommerce.schemas.ecommerce.schemas import EspecificacoesCasaeDecoracao, ProductCasaeDecoracao, ProductBase
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from fastapi import APIRouter, status, Body, Depends, HTTPException, Query
from ecommerce.models.ecommerce.models import Product_Casa_Decoracao
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json
import uuid


route_casa_decoracao = APIRouter()


@route_casa_decoracao.post(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Create product home and decorations",
    name="Route create product",
    )
async def create_product(
    product: ProductCasaeDecoracao = Body(embed=True), 
    db: Session = Depends(get_db)
):
    product_id = str(uuid.uuid4())

    db_product = Product_Casa_Decoracao(id=product_id, **product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product



@route_casa_decoracao.get(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesCasaeDecoracao],
    description="List all products",
    name="Route list products"
)
async def list_products(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    products = db.query(Product_Casa_Decoracao).offset(skip).limit(limit).all()
    
    if products:
        logger.info(msg="Produtos sendo listados")
        products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
        return products_listed

    if not products:
        logger.info(msg="Nenhum produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")


# rota de filtragem de buscas 
@route_casa_decoracao.get(
    path="/category/casa-e-decoracao/search-filters/",
    response_model=list[EspecificacoesCasaeDecoracao],
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
    query = db.query(Product_Casa_Decoracao)

    # Aplicar filtros se fornecidos
    # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
    if name:
        query = query.filter(Product_Casa_Decoracao.name.ilike(f"%{name}%"))

    if category: 
        query = query.filter(Product_Casa_Decoracao.category.ilike(f"%{category}%"))  # Usando LIKE

    if stars:
        query = query.filter(Product_Casa_Decoracao.stars >= stars)
    
    if color:
        query = query.filter(Product_Casa_Decoracao.color.ilike(f"%{color}%"))  # Usando LIKE para cor

    if details:
        query = query.filter(Product_Casa_Decoracao.details.ilike(f"%{details}%"))

    if size:
        query = query.filter(Product_Casa_Decoracao.size.ilike(f"%{size}%"))  # Usando LIKE para tamanho


    if min_price is not None:
        query = query.filter(Product_Casa_Decoracao.price >= min_price)

    if max_price is not None:
        query = query.filter(Product_Casa_Decoracao.price <= max_price)

    
    products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

    if products:
        logger.info(msg="Produtos de moda sendo listados!")
        products_listed = [Product_Casa_Decoracao.from_orm(product) for product in products]
        return products_listed

    logger.info(msg="Nenhum produto de moda encontrado!")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de moda encontrado!")


@route_casa_decoracao.get(
    path="/category/casa-e-decoracao/{product_id}",
    response_model=EspecificacoesCasaeDecoracao,
    status_code=status.HTTP_200_OK,
    description="Search product with ID",
    name="Route search product with ID"
)
async def search_product(
    product_id: str,
    db: Session = Depends(get_db)
):
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




@route_casa_decoracao.delete(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
)
async def delete_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()
    
    if product_delete:
        db.delete(product_delete)
        db.commit()
        logger.info(msg="Produto deletado!")
        #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
        # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500

    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")




@route_casa_decoracao.put(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Route for update products",
    name="Route create product"
)
async def update_product(
    product_id: str,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True)
    ):
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
    