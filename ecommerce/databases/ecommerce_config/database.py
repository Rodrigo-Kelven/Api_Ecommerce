from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite dentro da pasta 'databases'
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce/databases/DB/ecommerce.db"

# Criando o engine para conectar ao banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Testando a conexão
try:
    with engine.connect():
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro de conexão: {e}")

# Sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir os modelos
Base = declarative_base()
