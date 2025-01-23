from sqlalchemy import Column, Integer, String, Float
from databases.ecommerce_config.database import Base

# modelo do que vai para o DB
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)