from fastapi import APIRouter, status, Depends
from ecommerce.databases.ecommerce_config.database import get_db
from ecommerce.models.ecommerce.models import (
    Products_Eletronics,
    Product_Casa_Decoracao,
    Products_Moda_Feminina,
    Product_Automotivo,
    Product_Esporte_Lazer,
    Product_Brinquedos_Jogos,
    Product_Saude_Medicamentos,
    Product_Livros_Papelaria
)
from sqlalchemy.orm import Session


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
    # PRESTE ATENÇÃO PARA NAO ESQUECER O () DE  .ALL()
    products_eletronics = db.query(Products_Eletronics).all()
    products_casa_decoracao = db.query(Product_Casa_Decoracao).all()
    products_moda_feminina = db.query(Products_Moda_Feminina).all()
    products_automotivo = db.query(Product_Automotivo).all()
    products_esporte_lazer = db.query(Product_Esporte_Lazer).all()
    products_brinquedos_e_jogos = db.query(Product_Brinquedos_Jogos).all()
    products_saude_e_medicamentos = db.query(Product_Saude_Medicamentos).all()
    products_livros_papelaria = db.query(Product_Livros_Papelaria).all()
    
    # Combine todos os produtos em uma única lista
    # usando assim, sera retornado somnete uma lista com os produtos e suas indormacoes
    all_products = (
        products_eletronics +
        products_casa_decoracao +
        products_moda_feminina
    )
    # usando assim, os dados dos produtos sao retornados como um dicionario, que suas suas categorias
    all = {
        "Produtos Eletronicos": products_eletronics,
        "Produtos Casa e Decoracao": products_casa_decoracao,
        "Produtos Moda Feminina": products_moda_feminina,
        "Produtos Automotivos":  products_automotivo,
        "Produtos de Esporte e Lazer": products_esporte_lazer,
        "Produtos Brinquedos e Jogos": products_brinquedos_e_jogos,
        "Produtos Saude e Mediacmentos": products_saude_e_medicamentos,
        "Produtos Livros e Papelaria": products_livros_papelaria
    }
    return all  # Retorna uma lista de produtos