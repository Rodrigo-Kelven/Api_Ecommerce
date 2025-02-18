# app/database/database.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import redis
import os



# Definindo o caminho do banco de dados SQLite
db_ecommerce_path = "./databases/DB_ecommerce/db_ecommerce/ecommerce.db" # -> banco de dados dos produtos
db_users_path = "./databases/DB_users/db_users/users_users.db" # -> banco de dados de usuarios


# Redis em container
# o tempo de expiracao do dados esta em cada endpoins, a medida que os dados nao requesitados, o tempo se expiracao aumenta
redis_client = redis.Redis(host='localhost', port=6379, db=0)


# Verificar se a pasta existe, caso contrário, criar
db_directory_users = os.path.dirname(db_users_path)
db_directory_products = os.path.dirname(db_ecommerce_path)

if not os.path.exists(db_directory_users):
    os.makedirs(db_directory_users)  # Cria o diretório se não existir

if not os.path.exists(db_directory_products):
    os.makedirs(db_directory_products)  # Cria o diretório se não existir

# URL do banco de dados SQLite dentro da pasta 'databases'
SQLALCHEMY_DATABASE_api_automotors_veiculos_URL = f"sqlite:///{db_ecommerce_path}"
SQLALCHEMY_DATABASE_api_automotors_users_URL = f"sqlite:///{db_users_path}"

# Criando o engine para conectar ao banco de dados, aqui esta criando uma ponte para ai sim conectar a aplicacao ao DB e executar as operacoes
engine_ecommerce_products = create_engine(SQLALCHEMY_DATABASE_api_automotors_veiculos_URL, connect_args={"check_same_thread": False})
engine_ecommerce_users = create_engine(SQLALCHEMY_DATABASE_api_automotors_users_URL, connect_args={"check_same_thread": False})

# Testando a conexão, db veiculos
try:
    with engine_ecommerce_products.connect():
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro de conexão: {e}")

# Testando a conexão, db users
try:
    with engine_ecommerce_users.connect():
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro de conexão: {e}")

# Sessão para interagir com o banco de dados, essa sesao é muito importante, ela é responsavel por 'manter uma sessao'
SessionLocal_veiculos = sessionmaker(autocommit=False, autoflush=False, bind=engine_ecommerce_products)
SessionLocal_users = sessionmaker(autocommit=False, autoflush=False, bind=engine_ecommerce_users)

# Base para definir os modelos
Base = declarative_base()


# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal_veiculos()
    try:
        yield db
    finally:
        db.close()


# Dependência para obter a sessão do banco de dados de usuários
def get_db_users():
    db_users = SessionLocal_users()
    try:
        yield db_users
    finally:
        db_users.close()

