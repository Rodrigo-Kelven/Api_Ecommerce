from fastapi import FastAPI
from ecommerce.auth.config.config import config_CORS, LogRequestMiddleware
from ecommerce.databases.ecommerce_config.database import Base, engine_ecommerce
from ecommerce.auth.config.config_db import Base_auth, engine_auth
from ecommerce.controllers.all_routes.routes import routes
from ecommerce.config.config import cors,db_logger


app = FastAPI(
    debug=True,
    title="API Ecommerce with FastAPI",
    version="1.2.2",
    summary="Este projeto é uma API RESTful para um sistema de e-commerce."
    "Um simples projeto baseado num ecommerce construido em FastAPI."
    "A ideia e criar um pequeno Ecommerce e usa-lo como base em outros projetos."
    "Ele permite que os usuários realizem operações como criar, ler, atualizar e excluir produtos, além de gerenciar pedidos e usuários.",
)

routes(app) # funcao que chama todas as rotas existentes

# Adiciona o middleware ao FastAPI, verifica requests e responses
app.add_middleware(LogRequestMiddleware)

# funcao para configuracao do middleware
#app.middleware("http")(rate_limit_middleware) # refatorar depois

# CORS de autenticacao
config_CORS(app)

# CORS do ecommerce
cors(app)

@app.on_event("startup")
async def startup_event():
    try:
        # Criação das tabelas no banco de dados de usuários
        async with engine_auth.begin() as conn:
            await conn.run_sync(Base_auth.metadata.create_all)
            db_logger.info("Tabela UserDB criada com sucesso.")
            
        # Criação das tabelas no banco de dados de produtos
        async with engine_ecommerce.begin() as conn_ecom:
            await conn_ecom.run_sync(Base.metadata.create_all)
            db_logger.info("Tabelas criada com sucesso.")

    except Exception as e:
        db_logger.error(f"Erro ao criar tabelas: {str(e)}.")


@app.on_event("shutdown")
async def shutdown_event():
    await engine_auth.dispose()
    await engine_ecommerce.dispose()
    db_logger.info("Conexões com os bancos de dados encerradas.")