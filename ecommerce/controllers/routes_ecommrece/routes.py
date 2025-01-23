# controllers/routes_ecommrece/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ecommerce.models import Product  # Importando o modelo SQLAlchemy
from schemas.ecommerce.schemas import ProductCreate  # Importando o schema Pydantic para validação
from databases.ecommerce_config.database import SessionLocal  # Importando a sessão do banco de dados


route_ecom = APIRouter()


# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um produto
@route_ecom.post("/products/", response_model=ProductCreate)  # Usando o schema para resposta
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())  # Usando o modelo SQLAlchemy
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Rota para listar produtos
@route_ecom.get("/products/", response_model=list[ProductCreate])  # Usando o schema para resposta
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy
    return products

# Rota para consultar um produto específico
@route_ecom.get("/products/{product_id}", response_model=ProductCreate)  # Usando o schema para resposta
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()  # Usando o modelo SQLAlchemy
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
