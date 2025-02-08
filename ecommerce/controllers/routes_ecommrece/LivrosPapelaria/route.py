from fastapi import APIRouter, status, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ecommerce.schemas.ecommerce.schemas import EspecificacoesLivrosPapelaria, ProductLivrosPapelaria, ProductBase
from ecommerce.models.ecommerce.models import Product_Livros_Papelaria
from ecommerce.databases.ecommerce_config.database import get_db


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
    db_product = Product_Livros_Papelaria(**product.dict())
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
    return db_product



@route_livros_papelaria.get(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesLivrosPapelaria,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def get_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    db_product = db.query(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product



@route_livros_papelaria.delete(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Information products",
    description="Route get product for id",
    name="Route GET products ID"
)
async def delete_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    print("Produto deletado!!")
    return f"Product with {product_id} removed succesfull"



@route_livros_papelaria.put(
    path="/category/livros-papelaria/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesLivrosPapelaria,
    description="Route PUT product",
    name="Route PUT product"
)
async def update_product(
    product_id: int,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True),
):
    product = db.query(Product_Livros_Papelaria).filter(Product_Livros_Papelaria.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    

    for key, value in product_data.dict().items():
        setattr(product, key, value)

    # Corrige o valor da categoria se necessário
    #product.category = "Livros_Papelaria"  

    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(product)
    return product