from fastapi import FastAPI
from models.ecommerce.models import Base
from databases.ecommerce_config.database import engine
from controllers.all_routes.routes import routes

# Criação das tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()
routes(app) # funcao que chama todas as rotas existentes
