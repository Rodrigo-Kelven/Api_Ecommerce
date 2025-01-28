from fastapi import FastAPI
from models.ecommerce.models import Base
from databases.ecommerce_config.database import engine_ecommerce_products, engine_ecommerce_users
from controllers.all_routes.routes import routes

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine_ecommerce_users)
Base.metadata.create_all(bind=engine_ecommerce_products)


app = FastAPI()
routes(app) # funcao que chama todas as rotas existentes
