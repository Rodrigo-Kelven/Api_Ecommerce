import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definindo o caminho do banco de dados SQLite
db_ecommerce_path = "./ecommerce/databases/DB_ecommerce/ecommerce.db" # -> banco de dados dos produtos
# db_path = "./ecommerce/databases/DB_users/users_ecommerce.db" -> banco de dados de usuarios 

# Verificar se a pasta existe, caso contrário, criar
db_directory = os.path.dirname(db_ecommerce_path)  # Pega a pasta do caminho do DB
if not os.path.exists(db_directory):
    os.makedirs(db_directory)  # Cria o diretório se não existir

# URL do banco de dados SQLite dentro da pasta 'databases'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_ecommerce_path}"

# Criando o engine para conectar ao banco de dados, aqui esta criando uma ponte para ai sim conectar a aplicacao ao DB e executar as operacoes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Testando a conexão
try:
    with engine.connect():
        print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro de conexão: {e}")

# Sessão para interagir com o banco de dados, essa sesao é muito importante, ela é responsavel por 'manter uma sessao'
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir os modelos
Base = declarative_base()
