from pydantic import BaseModel, Field

# melhorar esse schema
# o schema serve basicamente como um intermediario entre voce e o modelo que ira para o DB
class ProductBase(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Notbook"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=["2500.00"])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=["1"])
    taxa: float = Field(None, title="Tax Product", description="Tax of product",examples=["0.1"])

# modelos/classes aninhadas -> Herdando outra class
class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
