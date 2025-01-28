import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definindo o caminho do banco de dados SQLite
db_ecommerce_path = "./databases/DB_ecommerce/db_products/ecommerce.db" # -> banco de dados dos produtos
db_users_path = "./databases/DB_ecommerce/db_users/users_ecommerce.db" # -> banco de dados de usuarios

# Verificar se a pasta existe, caso contrário, criar
db_directory_users = os.path.dirname(db_users_path)
db_directory_products = os.path.dirname(db_ecommerce_path)

if not os.path.exists(db_directory_users):
    os.makedirs(db_directory_users)  # Cria o diretório se não existir

if not os.path.exists(db_directory_products):
    os.makedirs(db_directory_products)  # Cria o diretório se não existir

# URL do banco de dados SQLite dentro da pasta 'databases'
SQLALCHEMY_DATABASE_ecommerce_products_URL = f"sqlite:///{db_ecommerce_path}"
SQLALCHEMY_DATABASE_ecommerce_users_URL = f"sqlite:///{db_users_path}"

# Criando o engine para conectar ao banco de dados, aqui esta criando uma ponte para ai sim conectar a aplicacao ao DB e executar as operacoes
engine_ecommerce_products = create_engine(SQLALCHEMY_DATABASE_ecommerce_products_URL, connect_args={"check_same_thread": False})
engine_ecommerce_users = create_engine(SQLALCHEMY_DATABASE_ecommerce_users_URL, connect_args={"check_same_thread": False})

# Testando a conexão
try:
    with engine_ecommerce_products.connect():
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro de conexão: {e}")

# Sessão para interagir com o banco de dados, essa sesao é muito importante, ela é responsavel por 'manter uma sessao'
SessionLocal_products = sessionmaker(autocommit=False, autoflush=False, bind=engine_ecommerce_products)
SessionLocal_users = sessionmaker(autocommit=False, autoflush=False, bind=engine_ecommerce_users)

# Base para definir os modelos
Base = declarative_base()


# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal_products()
    db_users = SessionLocal_users()
    try:
        yield db
    finally:
        db.close()