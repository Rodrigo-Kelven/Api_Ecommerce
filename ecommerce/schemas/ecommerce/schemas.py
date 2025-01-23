from pydantic import BaseModel

# o schema serve basicamente como um intermediario entre voce e o modelo que ira para o DB
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

# modelos/classes aninhadas -> Herdando outra class
class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True