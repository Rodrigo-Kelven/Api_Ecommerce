from sqlalchemy import Column, Integer, String, Float
from databases.ecommerce_config.database import Base

# criar os modelos das outras categorias

# modelo do que vai para o DB, nao esquecer de passar todos os dados de forma correta!

# modelo para produtos eletronicos
class Products_Eletronics(Base):
    __tablename__ = "products_eletronics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)  # Nome do produto é obrigatório
    description = Column(String, nullable=True)  # Descrição opcional
    price = Column(Float, nullable=False)  # Preço é obrigatório
    quantity = Column(Integer, nullable=False)  # Quantidade é obrigatória
    tax = Column(Float, nullable=True)  # Taxa opcional
    stars = Column(Float, nullable=True)  # Avaliação opcional
    color = Column(String, nullable=False)  # Cor é obrigatória
    size = Column(Integer, nullable=False)  # Tamanho é obrigatório
    details = Column(String, nullable=True)  # Detalhes opcionais
    category = Column(String, nullable=False, default='Eletronicos')

# modelo para Moda Feminina
class Products_Moda_Feminina(Base):
    __tablename__ = "products_moda_feminina"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Moda-Feminina')


class Product_Casa_Decoracao(Base):
    __tablename__ = "products_casa_decoracao"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Casa-e-decoracao')


class Product_Automotivo(Base):
    __tablename__ = "products_automotivo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Automotivo')


class Product_Beleza_e_cuidados(Base):
    __tablename__ = "products_beleza_e_cuidados"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Beleza_e_cuidados')


class Product_Esporte_Lazer(Base):
    __tablename__ = "products_esporte_lazer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Esporte_Lazer')


class Product_Brinquedos_Jogos(Base):
    __tablename__ = "products_brinquedos_jogos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Brinquedos_Jogos')

class Product_Saude_Medicamentos(Base):
    __tablename__ = "products_saude_medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Saude_Medicamentos')


class Product_Livros_Papelaria(Base):
    __tablename__ = "products_livros_papelaria"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    description = Column(String, nullable=True)  
    price = Column(Float, nullable=False)  
    quantity = Column(Integer, nullable=False)  
    tax = Column(Float, nullable=True)  
    stars = Column(Float, nullable=True)  
    color = Column(String, nullable=False)  
    size = Column(Integer, nullable=False)  
    details = Column(String, nullable=True)
    category = Column(String, nullable=False, default='Livros_Papelaria')