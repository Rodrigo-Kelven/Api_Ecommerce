from pydantic import BaseModel, Field
from typing_extensions import Literal 

# melhorar "detalhar" e revisar todos os schema para garantir maior precisao e documentacao sobre os produtos
# criar as subcategorias das categorias

# eschemas de cada categoria de produtos
# o schema serve basicamente como um intermediario entre voce e o modelo que ira para o DB

# nao esquecer de adicionar outros campos nesta class e caso seja adicionado em alguma outra categoria
class ProductBase(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product")
    description: str = Field(None, title="Description product", description="Description of products")
    price: float = Field(..., title="Price Product", description="Price of product")
    quantity: int = Field(..., title="Amount of product", description="Amount of product")
    tax: float = Field(None, title="Tax Product", description="Tax of product")
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product")
    color: str = Field(..., title="color product", description="Color of product")
    size: int = Field(..., title="size product", description="size product in CM")
    details: str = Field(None, title="details products", description="details of products")
    

class ProductBase_2(ProductBase):
    category: str


class ProductEletronicos(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Notbook asus"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[250.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Full Led"])

class ProductModaFeminina(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Calça cintura alta"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[250.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Jeans"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["rasgado leve"])

    
class ProductCasaeDecoracao(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Vaso para decoração"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[250.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Brilhante"])


class ProductAutomotivo(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Cera para painel"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[20.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Cera"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["15"])
    details: str = Field(None, title="details products", description="details of products", examples=["Brilhante"])


class ProductBelezaeCuidados(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Blush"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[50.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Base"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["10"])
    details: str = Field(None, title="details products", description="details of products", examples=["Base"])


class ProductEsporteLazer(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Saco de Pancada"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[60.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Preto"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["170"])
    details: str = Field(None, title="details products", description="details of products", examples=["Vazio"])


class ProductBrinquedosJogos(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Velocipe"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[50.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco e Azul"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Policia"])


class ProductLivrosPapelaria(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Livro algoritimos"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[25.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco e Preto"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Novo"])





# retornar com ID em todos
class ProductEletronicosID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Notbook"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[2500.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Black"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Full Led"])


class ProductModaFemininaID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Calça cintura alta"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[250.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Jeans"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["rasgado leve"])


class ProductCasaeDecoracaoID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Vaso para decoração"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[250.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Brilhante"])


class ProductAutomotivoID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Cera para painel"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[20.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Cera"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["15"])
    details: str = Field(None, title="details products", description="details of products", examples=["Brilhante"])


class ProductBelezaeCuidadosID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Blush"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[50.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Base"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["10"])
    details: str = Field(None, title="details products", description="details of products", examples=["Base"])


class ProductEsporteLazerID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Saco de Pancada"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[60.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Preto"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["170"])
    details: str = Field(None, title="details products", description="details of products", examples=["Vazio"])


class ProductBrinquedosJogosID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Velocipe"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[50.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco e Azul"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Policia"])


class ProductLivrosPapelariaID(BaseModel):
    id: str
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Livro algoritimos"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[25.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco e Preto"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Novo"])


# Especificacoes dos produtos
# o nome que estiver aqui em category, seve estar em category em models tambem
class EspecificacoesEletronicos(ProductEletronicosID):
    category: Literal["Eletronicos"] = "Eletronicos"
    
class EspecificacoesModaFeminina(ProductModaFemininaID):
    category: Literal["Moda-Feminina"] = "Moda-Feminina" 
    
class EspecificacoesCasaeDecoracao(ProductCasaeDecoracaoID):
    category: Literal["Casa-e-decoracao"] = "Casa-e-decoracao" # somente passando a Litral é suficiente para setar o valor desejado

class EspecificacoesEsporteLazer(ProductEsporteLazerID):
    category: Literal["Esporte_Lazer"] = "Esporte_Lazer" 

class EspecificacoesBrinquedosJogos(ProductBrinquedosJogosID):
    category: Literal["Brinquedos_Jogos"] = "Brinquedos_Jogos" 

class EspecificacoesLivrosPapelaria(ProductLivrosPapelariaID):
    category: Literal["Livros_Papelaria"] = "Livros_Papelaria" 

class EspecificacoesAutomotivo(ProductAutomotivoID):
    category: Literal["Automotivo"] = "Automotivo" # somente passando a Litral é suficiente para setar o valor desejado
