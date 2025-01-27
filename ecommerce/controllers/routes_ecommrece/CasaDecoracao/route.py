from fastapi import APIRouter, status, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ecommerce.models import Product_Casa_Decoracao
from schemas.ecommerce.schemas import EspecificacoesCasaeDecoracao, ProductCasaeDecoracao, ProductBase
from databases.ecommerce_config.database import get_db



route_cada_decoracao = APIRouter()


# Rota para criar um produto
@route_cada_decoracao.post(
    path="/category/casa-e-decoracao/",
    status_code=status.HTTP_201_CREATED,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Create product home and decorations",
    name="Route create product",
    )
async def create_product(product: ProductCasaeDecoracao = Body(embed=True), db: Session = Depends(get_db)):
    db_product = Product_Casa_Decoracao(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Rota para listar todos os produtos
@route_cada_decoracao.get(
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
    product = db.query(Product_Casa_Decoracao).offset(skip).limit(limit).all()
    return product


# Rota para consultar um produto pelo ID
@route_cada_decoracao.get(
    path="/category/casa-e-decoracao/{product_id}",
    response_model=EspecificacoesCasaeDecoracao,
    status_code=status.HTTP_200_OK,
    description="Search product with ID",
    name="Route search product with ID"
)
async def search_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()  # Usando o modelo de SQLAlchemy
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Rota para deletar produto pelo ID
@route_cada_decoracao.delete(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
)
async def delete_product_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
    # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500
    print("Produto deletado!!")
    return f"Product with {product_id} removed succesfull"


# Rota para atualizar os produtos pelo ID
@route_cada_decoracao.put(
    path="/category/casa-e-decoracao/{product_id}/",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesCasaeDecoracao,
    response_description="Informations product",
    description="Route for update products",
    name="Route create product"
)
async def update_product(
    product_id: int,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True)
    ):
    product = db.query(Product_Casa_Decoracao).filter(Product_Casa_Decoracao.id == product_id).first()

    # Verifica se o produto existe
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Atualiza os campos do produto com os dados recebidos
    for key, value in product_data.dict().items():
        setattr(product, key, value)

    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(product)
    return product