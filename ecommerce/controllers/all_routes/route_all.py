from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ecommerce.models import Product_Casa_Decoracao, Products_Eletronics, Products_Moda_Feminina
from databases.ecommerce_config.database import get_db

route_all = APIRouter()

@route_all.get(
    path="/all-products/",
    status_code=status.HTTP_200_OK,
    #response_model=list[ProductBase], Criar um model ou deixar assim mesmo, se desconmentar nao funciona porque esta retornando uma lista com todos os produtos por categorias
    response_description="Informations products",
    description="Route return all products",
    name="Route all products"
    )
async def all_products(
    db: Session = Depends(get_db)
):
    products_eletronics = db.query(Products_Eletronics).all()
    products_casa_decoracao = db.query(Product_Casa_Decoracao).all()
    products_moda_feminina = db.query(Products_Moda_Feminina).all()
    
    # Combine todos os produtos em uma única lista
    # usando assim, sera retornado somnete uma lista com os produtos e suas indormacoes
    all_products = (
        products_eletronics +
        products_casa_decoracao +
        products_moda_feminina
    )
    # usando assim, os dados dos produtos sao retornados como um dicionario, que suas suas categorias
    all = {
        "Produtos eletronicos":products_eletronics,
        "Produtos Casa e decoracao":products_casa_decoracao,
        "Produtos Moda Feminina":products_moda_feminina
    }
    return all  # Retorna uma lista de produtos