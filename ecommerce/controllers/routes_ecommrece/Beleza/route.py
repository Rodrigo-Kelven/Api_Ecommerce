from ecommerce.schemas.ecommerce.schemas import ProductBelezaeCuidados, EspecificacoesBelezaCuidados, ProductBase
from ecommerce.models.ecommerce.models import Product_Beleza_e_cuidados
from fastapi import APIRouter, status, HTTPException, Body, Depends
from ecommerce.databases.ecommerce_config.database import get_db
from ecommerce.config.config import logger
from sqlalchemy.orm import Session

route_Beleza = APIRouter()



@route_Beleza.post(
    path="/category/beleza-e-cuidados/product",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=EspecificacoesBelezaCuidados,
    response_description="Informations product",
    description="Route create product",
    name="Route create product"
)
async def create_product(
    product: ProductBelezaeCuidados = Body(embed=True),
    db: Session = Depends(get_db)
):
    product = Product_Beleza_e_cuidados(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



@route_Beleza.get(
    path="/category/beleza-e-cuidados/products",
    status_code=status.HTTP_200_OK,
    response_model=list[EspecificacoesBelezaCuidados],
    response_description="Informations Products",
    description="Route list products",
    name="Route list products category"
)
async def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    products = db.query(Product_Beleza_e_cuidados).offset(skip).limit(limit).all()
    
    if products:
        logger.info(msg="Produto sendo listado!")
        products_listed = [Product_Beleza_e_cuidados.from_orm(product) for product in products]
        return products_listed

    if not products:
        logger.info(msg="Nenhum produto inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto inserido!")



@route_Beleza.get(
    path="/category/beleza-e-cuidados/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBelezaCuidados,
    response_description="Informations Products",
    description="Route list products",
    name="Route list products category"
)
async def searchProduct_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    products = db.query(Product_Beleza_e_cuidados).filter(Product_Beleza_e_cuidados.id == product_id).first()

    if products:
        logger.info(msg="Produto encontrado")
        products_listed = Product_Beleza_e_cuidados.from_orm(products)
        return products_listed
    
    if not products:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")



@route_Beleza.delete(
    path="/category/beleza-e-cuidados/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations Products",
    description="Route delete product for ID",
    name="Route DELETE products for ID"
)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_delete = db.query(Product_Beleza_e_cuidados).filter(Product_Beleza_e_cuidados.id == product_id).first()
    
    if product_delete:
        db.delete(product_delete)
        db.commit()
        logger.info(msg="Produto deletado!")


    if product_delete is None:
        logger.info(msg="Produto nao encontado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encnotrado!")
    



@route_Beleza.put(
    path="/category/beleza-e-cuidados/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=EspecificacoesBelezaCuidados,
    response_description="Informations Products",
    description="Route update product for ID",
    name="Route PUT products for ID"
)
async def update_products(
    product_id: int,
    product_data: ProductBase = Body(embed=True),
    db: Session = Depends(get_db),
):
    product = db.query(Product_Beleza_e_cuidados).filter(Product_Beleza_e_cuidados.id == product_id).first()
    
    if product:
        # Atualiza os campos do produto com os dados recebidos
        for key, value in product_data.dict().items():
            setattr(product, key, value)

        # Corrige o valor da categoria se necessário
        #product.category = "Beleza_e_cuidados"  

        # Salva as alterações no banco de dados
        db.commit()
        db.refresh(product)
        logger.info(msg="Produto atualziado")
        return product


    # Verifica se o produto existe
    if product is None:
        logger.info(msg="Produto nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado!")
    