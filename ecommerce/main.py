from fastapi import FastAPI
from ecommerce.databases.ecommerce_config.database import Base
from ecommerce.config.config import *
from ecommerce.databases.ecommerce_config.database import engine_ecommerce_products, engine_ecommerce_users
from ecommerce.controllers.all_routes.routes import routes


app = FastAPI(
    debug=True,
    title="API Ecommerce with FastAPI",
    version="0.2.0",
    summary="Este projeto é uma API RESTful para um sistema de e-commerce."
    "Um simples projeto baseado num ecommerce construido em FastAPI."
    "A ideia e criar um pequeno Ecommerce e usa-lo como base em outros projetos."
    "Ele permite que os usuários realizem operações como criar, ler, atualizar e excluir produtos, além de gerenciar pedidos e usuários."
)

routes(app) # funcao que chama todas as rotas existentes

# Adiciona o middleware ao FastAPI, verifica requests e responses
app.add_middleware(LogRequestMiddleware)

# funcao para configuracao do middleware
app.middleware("http")(rate_limit_middleware)

# Configure o logging para depuração
logging.basicConfig(level=logging.DEBUG)

# Verifique se as tabelas estão sendo criadas
logging.debug("Criando as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine_ecommerce_users)
Base.metadata.create_all(bind=engine_ecommerce_products)
logging.debug("Tabelas criadas com sucesso.")