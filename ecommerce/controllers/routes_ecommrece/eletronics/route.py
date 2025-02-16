from ecommerce.schemas.ecommerce.schemas import ProductEletronicos, EspecificacoesEletronicos, ProductBase 
from fastapi import APIRouter, Depends, HTTPException, status, Body
from ecommerce.models.ecommerce.models import Products_Eletronics  
from ecommerce.databases.ecommerce_config.database import  get_db
from ecommerce.config.config import logger
from sqlalchemy.orm import Session


route_eletronicos = APIRouter()




@route_eletronicos.post(
        path="/category/eletronic/", 
        status_code=status.HTTP_201_CREATED,
        response_model=EspecificacoesEletronicos,
        response_description="Informations of product",
        description="Create product",
        name="Route create product"
    )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def create_product(
    product: ProductEletronicos = Body(embed=True),
    db: Session = Depends(get_db)
    ): # db esta sendo tipado como uma Sessao, que tem uma dependencia em fazer um get, no DB
    
    db_product = Products_Eletronics(**product.dict()) 
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



@route_eletronicos.get(
        path="/category/eletronic/", 
        response_model=list[EspecificacoesEletronicos],
        status_code=status.HTTP_200_OK,
        description="List all producst",
        name="Route list products"
        )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def read_products(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    products = db.query(Products_Eletronics).offset(skip).limit(limit).all()  # Usando o modelo SQLAlchemy
    
    if products:
        logger.info(msg="Produtos eletronicos listados")
        products_listados = [Products_Eletronics.from_orm(product) for product in products]
        return products_listados
    
    if not products:
        logger.info(msg="Nenhum produto eletronico inserido!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto eletronico inserido!")


@route_eletronicos.get(path="/category/eletronic/{product_id}",
                response_model=EspecificacoesEletronicos,
                status_code=status.HTTP_200_OK,
                description="Search product with ID",
                name="Route search product with ID"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def read_product_id(
    product_id: int,
    db: Session = Depends(get_db
)):
    product = db.query(Products_Eletronics).filter(Products_Eletronics.id == product_id).first()

    if product:
        logger.info(msg="Produto eletronico sendo listado")
        product_listed = Products_Eletronics.from_orm(product)
        return product_listed


    if product is None:
        logger.info(msg="Produto eletronico nao encontrado!")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto eletronico nao encontrado!")



@route_eletronicos.delete(
    path="/category/eletronic/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
    )
async def delete_product_id(
    product_id: int, 
    db: Session = Depends(get_db)
):
    product_delete = db.query(Products_Eletronics).filter(Products_Eletronics.id == product_id).first()
    
    if product_delete:
        logger.info(msg="Produto eletronico deletado")
        db.delete(product_delete)
        db.commit()
        #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
        # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500

    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto eletronico nao encontrado!")
    




@route_eletronicos.put(
    path="/category/eletronic/{product_id}",
    response_model=EspecificacoesEletronicos,
    status_code=status.HTTP_200_OK,
    description="Update product for ID",
    name="Route update product with ID"
)
async def update_product(
    product_id: int,
    db: Session = Depends(get_db),
    product_data: ProductBase = Body(embed=True)
):

    product = db.query(Products_Eletronics).filter(Products_Eletronics.id == product_id).first()

    if product:
        logger.info(msg="Produto eletronico encontrado!")
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        logger.info(msg="Produto eletronico atualizado")

        db.commit()
        db.refresh(product)
        return product
    
    if product is None:
        logger.info(msg="Produto eletronico nao encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto eletronico nao encontrado!")
    


    # Corrige o valor da categoria se necessário
    #product.category = "Eletronicos"  # Defina o valor da categoria como "Eletronicos"

