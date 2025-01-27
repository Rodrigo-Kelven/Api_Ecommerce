from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from models.ecommerce.models import Products_Eletronics  # Importando o modelo SQLAlchemy
from schemas.ecommerce.schemas import ProductEletronicos, EspecificacoesEletronicos, ProductBase # Importando o schema Pydantic para validação
from databases.ecommerce_config.database import  get_db  # Importando a sessão do banco de dados


route_eletronicos = APIRouter()


# Rota para criar um produto
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
    
    db_product = Products_Eletronics(**product.dict())  # Usando o modelo SQLAlchemy
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Rota para listar todos os produtos
@route_eletronicos.get(path="/category/eletronic/", 
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
    return products


# Rota para consultar um produto pelo ID
@route_eletronicos.get(path="/category/eletronic/{product_id}",
                response_model=EspecificacoesEletronicos,
                status_code=status.HTTP_200_OK,
                description="Search product with ID",
                name="Route search product with ID"
            )  # Usando o schema para transportar o Body para o Modelo que irá salvar os dados no Banco de dados
async def read_product(
    product_id: int,
    db: Session = Depends(get_db
)):
    product = db.query(Products_Eletronics).filter(Products_Eletronics.id == product_id).first()  # Usando o modelo de SQLAlchemy
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Rota para deletar produto pelo ID
@route_eletronicos.delete(
    path="/category/eletronic/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete product for ID",
    name="Route delete product for ID"
    )
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db)
):
    product_delete = db.query(Products_Eletronics).filter(Products_Eletronics.id == product_id).first()
    if product_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product_delete)
    db.commit()
    #db.refresh(product_delete) # se voce descomentar isso, sempre vai dar erro 500
    # porque ao dar refresh, entende-se que voce esta procurando o objeto excluido da sessao! por isso erro 500
    print("Produto deletado!!")
    return f"Product with {product_id} removed succesfull"


# Rota para atualizar os produtos
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
    # Busca o produto pelo ID
    product = db.query(Products_Eletronics).filter(Products_Eletronics.id == product_id).first()

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

