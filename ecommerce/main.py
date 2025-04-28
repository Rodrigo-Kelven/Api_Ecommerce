from fastapi import FastAPI
from ecommerce.auth.config.config_db import Base_auth, engine_auth
from ecommerce.config.config import *
from ecommerce.databases.ecommerce_config.database import engine_ecommerce_products, Base
from ecommerce.controllers.all_routes.routes import routes
from ecommerce.auth.config.config import db_logger, config_CORS


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
db_logger.info("Tabelas sendo criadas,")
Base.metadata.create_all(bind=engine_ecommerce_products)
db_logger.info("Tabelas criadas.")

config_CORS(app)

@app.on_event("startup")
async def startup_event():
    try:
        # Criação das tabelas no banco de dados de usuários
        async with engine_auth.begin() as conn:
            await conn.run_sync(Base_auth.metadata.create_all)
            db_logger.info("Tabela UserDB criada com sucesso.")

    except Exception as e:
        db_logger.error(f"Erro ao criar tabelas: {str(e)}.")


@app.on_event("shutdown")
async def shutdown_event():
    await engine_auth.dispose()
    db_logger.info("Conexões com os bancos de dados encerradas.")