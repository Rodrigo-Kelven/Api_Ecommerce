from fastapi import APIRouter, status, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from ecommerce.models.ecommerce.models import Product_Brinquedos_Jogos
from ecommerce.schemas.ecommerce.schemas import ProductBrinquedosJogos, EspecificacoesBrinquedosJogos, ProductBase
from ecommerce.databases.ecommerce_config.database import get_db

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
    product = db.query(Product_Brinquedos_Jogos).offset(skip).limit(limit).all()
    return product



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
    product = db.query(Product_Brinquedos_Jogos).filter(Product_Brinquedos_Jogos.id == product_id).first()
    return product



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
    if product_delete is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    print("Produto deletado!!")
    return f"Product with {product_id} removed succesfull"



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
    # Verifica se o produto existe
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Atualiza os campos do produto com os dados recebidos
    for key, value in product_data.dict().items():
        setattr(product, key, value)

    # Corrige o valor da categoria se necessário
    #product.category = "Beleza_e_cuidados"  

    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(product)
    return product