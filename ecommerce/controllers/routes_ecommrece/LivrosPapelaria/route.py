from ecommerce.schemas.ecommerce.schemas import EspecificacoesLivrosPapelaria, ProductLivrosPapelaria, ProductBase
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from ecommerce.models.ecommerce.models import Product_Livros_Papelaria
from fastapi import APIRouter, status, Depends, HTTPException, Body, Query
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json
import uuid


route_livros_papelaria = APIRouter()


@route_livros_papelaria.post(
    path="/category/livros-papelaria/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesLivrosPapelaria,
    response_description="Informations product",
    description="Route create product",
    name="Route Create product"
)
async def create_product(
    product: ProductLivrosPapelaria,
    db: Session = Depends(get_db)
):
    product_id = str(uuid.uuid4())

    db_product = Product_Livros_Papelaria(id=product_id, **product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



@route_livros_papelaria.get(
    path="/category/livros-papelaria/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesLivrosPapelaria],
    response_description="Informations products",
    description="Route list products",
    name="Route list products category automotivo"
)
async def get_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    db_product = db.query(Product_Livros_Papelaria).offset(skip).limit(limit).all()
    
    if db_product:
        logger.info(msg="Produtos sendo listado!")
        products_listed = [Product_Livros_Papelaria.from_orm(product) for product in db_product]
        return products_listed
    
    if not db_product:
        logger.info(msg="Nenhum produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")


# rota de filtragem de buscas 
@route_livros_papelaria.get(
    path="/category/livros-papelaria/search-filters/",
    response_model=list[EspecificacoesLivrosPapelaria],
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
    query = db.query(Product_Livros_Papelaria)

    # Aplicar filtros se fornecidos
    # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
    if name:
        query = query.filter(Product_Livros_Papelaria.name.ilike(f"%{name}%"))

    if category: 
        query = query.filter(Product_Livros_Papelaria.category.ilike(f"%{category}%"))  # Usando LIKE

    if stars:
        query = query.filter(Product_Livros_Papelaria.stars >= stars)
    
    if color:
        query = query.filter(Product_Livros_Papelaria.color.ilike(f"%{color}%"))  # Usando LIKE para cor

    if details:
        query = query.filter(Product_Livros_Papelaria.details.ilike(f"%{details}%"))

    if size:
        query = query.filter(Product_Livros_Papelaria.size.ilike(f"%{size}%"))  # Usando LIKE para tamanho


    if min_price is not None:
        query = query.filter(Product_Livros_Papelaria.price >= min_price)

    if max_price is not None:
        query = query.filter(Product_Livros_Papelaria.price <= max_price)

    
    products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

    if products:
        logger.info(msg="Produtos de moda sendo listados!")
        products_listed = [Product_Livros_Papelaria.from_orm(product) for product in products]
        return products_listed

    logger.info(msg="Nenhum produto encontrado!")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto encontrado!")



@route_livros_papelaria.get(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesLivrosPapelaria,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def get_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    
    product_data = redis_client.get(f"produto_livraria:{product_id}")

    if product_data:
        logger.info(msg="Produto retornado do Redis!")
        return json.loads(product_data)
    
    db_product = db.query(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id).first()
    
    if db_product:
        logger.info(msg="Produto encontrado no banco de dados!")
        product = Product_Livros_Papelaria.from_orm(db_product)

        product_data = {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "quantity": db_product.quantity,
            "tax": db_product.tax,
            "stars": db_product.stars,
            "color": db_product.color,
            "size": db_product.size,
            "details": db_product.details,
            "category": "Livros_Papelaria"
        }
        logger.info(msg="Produto inserido no redis!")
        # Armazena no Redis com um tempo de expiração de 15 horas (54000 segundos)
        redis_client.setex(f"produto_livraria:{db_product.id}", 54000, json.dumps(product_data))
        logger.info(msg="Produto armazenado no Redis com expiração de 15 horas.")
        # retorna do db
        return product

    if db_product is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")



@route_livros_papelaria.delete(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def delete_product_id(
    product_id: str,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id).first()
    
    if product_delete:
        logger.info(msg="Produto encontrado!")
        db.delete(product_delete)
        db.commit()
        print("Produto deletado!!")
        return f"Product with {product_id} removed succesfull"

    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")



@route_livros_papelaria.put(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesLivrosPapelaria,
    description="Route PUT product",
    name="Route PUT product"
)
async def update_product(
    product_id: str,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
    product = db.query(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id).first()

    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        # Corrige o valor da categoria se necessário
        #product.category = "Livros_Papelaria"  

        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(product)
        return product


    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    