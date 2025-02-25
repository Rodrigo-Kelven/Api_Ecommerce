from fastapi import FastAPI
from ecommerce.databases.ecommerce_config.database import Base
from ecommerce.config.config import *
from ecommerce.databases.ecommerce_config.database import engine_ecommerce_products, engine_ecommerce_users
from ecommerce.controllers.all_routes.routes import routes

# Configure o logging para depuração
logging.basicConfig(level=logging.DEBUG)

# Verifique se as tabelas estão sendo criadas
logging.debug("Criando as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine_ecommerce_users)
Base.metadata.create_all(bind=engine_ecommerce_products)
logging.debug("Tabelas criadas com sucesso.")


app = FastAPI()
routes(app) # funcao que chama todas as rotas existentes

# Adiciona o middleware ao FastAPI, verifica requests e responses
app.add_middleware(LogRequestMiddleware)

# funcao para configuracao do middleware
app.middleware("http")(rate_limit_middleware)