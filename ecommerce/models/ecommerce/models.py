from sqlalchemy import Column, Integer, String, Float
from databases.ecommerce_config.database import Base

# modelo do que vai para o DB
# modelo para produtos eletronicos
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer)
    taxa = Column(Float, nullable=True)
    stars = Column(Float, nullable=True)
    color = Column(String)

# criar os modelos das outras categorias