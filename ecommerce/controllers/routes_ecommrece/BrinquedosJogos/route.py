from ecommerce.schemas.ecommerce.schemas import ProductBrinquedosJogos, EspecificacoesBrinquedosJogos, ProductBase
from ecommerce.databases.ecommerce_config.database import get_db, redis_client
from fastapi import APIRouter, status, HTTPException, Body, Depends, Query
from ecommerce.models.ecommerce.models import Product_Brinquedos_Jogos
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json

route_brinquedos_jogos = APIRouter()



@route_brinquedos_jogos.post(
    path="/category/brinquedos-jogos/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
async def create_product(
    product: ProductBrinquedosJogos = Body(embed=True),
    db: Session = Depends(get_db)
):
    product = Product_Brinquedos_Jogos(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)

    return product



@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesBrinquedosJogos],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products"
)
async def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    products = db.query(Product_Brinquedos_Jogos).offset(skip).limit(limit).all()

    if products:
        logger.info(msg="Produtos sendo listados!")
        products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
        return products_listed
    
    if not products:
        logger.info(msg="Nenhum produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")


# rota de filtragem de buscas 
@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/search-filters/",
    response_model=list[EspecificacoesBrinquedosJogos],
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
    query = db.query(Product_Brinquedos_Jogos)

    # Aplicar filtros se fornecidos
    # explicacao: ecommerce/databases/ecommerce_config/database.py -> linha 80
    if name:
        query = query.filter(Product_Brinquedos_Jogos.name.ilike(f"%{name}%"))

    if category: 
        query = query.filter(Product_Brinquedos_Jogos.category.ilike(f"%{category}%"))  # Usando LIKE

    if stars:
        query = query.filter(Product_Brinquedos_Jogos.stars >= stars)
    
    if color:
        query = query.filter(Product_Brinquedos_Jogos.color.ilike(f"%{color}%"))  # Usando LIKE para cor

    if details:
        query = query.filter(Product_Brinquedos_Jogos.details.ilike(f"%{details}%"))

    if size:
        query = query.filter(Product_Brinquedos_Jogos.size.ilike(f"%{size}%"))  # Usando LIKE para tamanho


    if min_price is not None:
        query = query.filter(Product_Brinquedos_Jogos.price >= min_price)

    if max_price is not None:
        query = query.filter(Product_Brinquedos_Jogos.price <= max_price)

    
    products = query.offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy

    if products:
        logger.info(msg="Produtos de moda sendo listados!")
        products_listed = [Product_Brinquedos_Jogos.from_orm(product) for product in products]
        return products_listed

    logger.info(msg="Nenhum produto de moda encontrado!")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto de moda encontrado!")



@route_brinquedos_jogos.get(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations Products",
    description="Route get product for ID",
    name="Route GET product for ID"
)
async def searchProduct_id(
    product_id: int,
    db: Session = Depends(get_db)
):
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

@route_brinquedos_jogos.delete(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE product for ID"
)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
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



@route_brinquedos_jogos.put(
    path="/category/brinquedos-jogos/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBrinquedosJogos,
    response_description="Informations Products",
    description="Route update products",
    name="Route PUT product for ID"
)
async def update_products(
    product_id: int,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_db),
):
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
    