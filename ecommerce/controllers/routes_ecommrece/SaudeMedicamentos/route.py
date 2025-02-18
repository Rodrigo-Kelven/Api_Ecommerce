from ecommerce.schemas.ecommerce.schemas import EspecificacoesSaudeMedicamentos, ProductSaudeMedicamentos, ProductBase
from fastapi import APIRouter, status, Depends, HTTPException, Body
from models.ecommerce.models import Product_Saude_Medicamentos
from databases.ecommerce_config.database import get_db, redis_client
from ecommerce.config.config import logger
from sqlalchemy.orm import Session
import json

route_saude_medicamentos = APIRouter()


# Rota POST
@route_saude_medicamentos.post(
    path="/category/saude-medicamentos/product",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesSaudeMedicamentos,
    response_description="Informations product",
    description="Route create product",
    name="Route Create product"
)
async def create_product(
    product: ProductSaudeMedicamentos,
    db: Session = Depends(get_db)
):
    db_product = Product_Saude_Medicamentos(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Rota GET
@route_saude_medicamentos.get(
    path="/category/saude-medicamentos/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesSaudeMedicamentos],
    response_description="Informations products",
    description="Route list products",
    name="Route list products category automotivo"
)
async def get_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    db_product = db.query(Product_Saude_Medicamentos).offset(skip).limit(limit).all()

    if db_product:
        logger.info(msg="Produtos sendo listados")
        products_listed = Product_Saude_Medicamentos.from_orm(db_product)
        return products_listed
    
    if not db_product:
        logger.info("Nenhum produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")
    

# Rota GET with ID
@route_saude_medicamentos.get(
    path="/category/saude-medicamentos/product/{product_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesSaudeMedicamentos,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def get_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_data = redis_client.get(f"produto: {product_id}")

    if product_data:
        logger.info(msg="Produto retornado do Redis")
        return json.loads(product_data)
    
    db_product = db.query(Product_Saude_Medicamentos).filter(Product_Saude_Medicamentos.id == product_id).first()
    
    if db_product:
        logger.info(msg="Produto encontrado")
        product = Product_Saude_Medicamentos.from_orm(db_product)

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
            "category": 'Brinquedos_Jogos'
        }
        redis_client.set(f"produto: {db_product.id}", json.dumps(product_data))
        logger.info(msg="Produto armazenado no Redis")

        return product

    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


# Rota DELETE with ID
@route_saude_medicamentos.delete(
    path="/category/saude-medicamentos/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def delete_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):

    product_delete = db.query(Product_Saude_Medicamentos).filter(Product_Saude_Medicamentos.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    print("Produto deletado!!")
    return f"Product with {product_id} removed succesfull"


# Rota PUT
@route_saude_medicamentos.put(
    path="/category/saude-medicamentos/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesSaudeMedicamentos,
    description="Route PUT product",
    name="Route PUT product"
)
async def update_product(
    product_id: int,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
    product = db.query(Product_Saude_Medicamentos).filter(Product_Saude_Medicamentos.id == product_id).first()
    # Verifica se o produto existe
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Atualiza os campos do produto com os dados recebidos
    for key, value in product_data.dict().items():
        setattr(product, key, value)

    # Corrige o valor da categoria se necessário
    #product.category = "Saude_Medicamentos"  

    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(product)
    return product