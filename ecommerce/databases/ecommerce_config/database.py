from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
import logging
import redis



# URL do banco de dados PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/fastapi_db"

# Redis em container
# o tempo de expiracao do dados esta em cada endpoins, a medida que os dados nao requesitados, o tempo se expiracao aumenta
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Criação do engine assíncrono
engine_ecommerce = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=20,  # Tamanho do pool de conexões
    max_overflow=0,  # Conexões adicionais permitidas
    pool_pre_ping=True, # Verifica se a conexão está ativa antes de se conectar
)



# Criação do gerenciador de sessões assíncronas
AsyncSessionLocal = sessionmaker(bind=engine_ecommerce, class_=AsyncSession, expire_on_commit=False)

# Criação da base para os modelos
Base = declarative_base()


# Função para obter a sessão de banco de dados
async def get_Session():
    async with AsyncSessionLocal() as session:
        yield session


# sessao de anotacoes
"""
Uso de ilike: O método ilike é usado para realizar uma busca insensível a maiúsculas e minúsculas.
O padrão f"%{category}%" permite que a pesquisa encontre qualquer categoria que contenha a string fornecida.
Por exemplo, se o usuário buscar "verão", ele encontrará categorias como "Moda de Verão", "Roupas de Verão", etc.

Flexibilidade: Isso torna a pesquisa mais flexível,
permitindo que os usuários encontrem produtos que correspondam a partes de strings em vez de uma correspondência exata.

"""