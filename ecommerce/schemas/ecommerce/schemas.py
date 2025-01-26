from pydantic import BaseModel, Field
from typing_extensions import Literal 

# melhorar "detalhar" e revisar todos os schema para garantir maior precisao e documentacao sobre os produtos
# criar as subcategorias das categorias

# eschemas de cada categoria de produtos
# o schema serve basicamente como um intermediario entre voce e o modelo que ira para o DB

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


class ProductBelezaeCuidados(BaseModel):
    pass

class ProductEsporteLazer(BaseModel):
    pass

class ProductBrinquedosJogos(BaseModel):
    pass

class ProductSaudeMedicamentos(BaseModel):
    pass

class ProductLivrosPapelaria(BaseModel):
    pass

class ProductAutomotivo(BaseModel):
    pass


# retornar com ID em todos
class ProductEletronicosID(BaseModel):
    id: int
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
    id: int
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
    id: int
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Vaso para decoração"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[250.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Brilhante"])



# Especificacoes dos produtos
class EspecificacoesEletronicos(ProductEletronicosID):
    categoty: Literal["Eletronicos"] = "Eletronicos"

class EspecificacoesModaFeminina(ProductModaFemininaID):
    category: Literal["Moda"] = "Moda" 
    
class EspecificacoesCasaeDecoracao(ProductCasaeDecoracaoID):
    category: Literal["Casa e decoracao"] = "Casa e decoracao" # somente passando a Litral é suficiente para setar o valor desejado

""" # Este método valida que o campo "category" não seja modificado
    def dict(self, *args, **kwargs):
        kwargs['exclude_unset'] = True
        original = super().dict(*args, **kwargs)
        if 'category' in original:
            original['category'] = self.category
        return original
 """   

class EspecificacoesBelezaCuidados(BaseModel):
    pass

class EspecificacoesEsporteLazer(BaseModel):
    pass

class EspecificacoesBrinquedosJogos(BaseModel):
    pass

class EspecificacoesSaudeMedicamentos(BaseModel):
    pass

class EspecificacoesLivrosPapelaria(BaseModel):
    pass

class EspecificacoesAutomotivo(BaseModel):
    pass


"""
class Product(ProductEletronicos):
    id: int

    class Config:
        orm_mode = True

"""

""" criar um schema especifico para cada produto
1. Eletrônicos

    Subcategorias:
        Smartphones e Acessórios
        Computadores e Laptops
        Televisores e Áudio
        Câmeras e Filmadoras
        Eletrodomésticos
        Gadgets e Wearables (smartwatches, fones de ouvido, etc.)

2. Moda

    Subcategorias:
        Roupas Femininas
        Roupas Masculinas
        Calçados
        Acessórios (bolsas, relógios, óculos, etc.)
        Moda Infantil
        Moda Plus Size

3. Casa e Decoração

    Subcategorias:
        Móveis (sofás, cadeiras, camas)
        Decoração (quadros, tapetes, almofadas)
        Utensílios Domésticos
        Iluminação
        Organizações (armários, prateleiras)

4. Beleza e Cuidados Pessoais

    Subcategorias:
        Cosméticos (maquiagem, cremes, perfumes)
        Cuidados com a pele
        Cuidados com o cabelo
        Saúde e Bem-estar
        Produtos naturais

5. Alimentos e Bebidas

    Subcategorias:
        Alimentos Perecíveis
        Alimentos Não Perecíveis
        Bebidas (alcoólicas e não alcoólicas)
        Produtos Gourmet
        Produtos Orgânicos e Naturais

6. Esportes e Lazer

    Subcategorias:
        Roupas e Calçados Esportivos
        Equipamentos de Ginástica
        Bicicletas e Acessórios
        Artigos de Camping e Aventura
        Materiais de Esportes (futebol, basquete, etc.)


8. Brinquedos e Jogos

    Subcategorias:
        Brinquedos para Bebês
        Brinquedos Educativos
        Jogos de Tabuleiro
        Jogos Eletrônicos e Video Games

9. Saúde e Medicamentos

    Subcategorias:
        Medicamentos
        Suplementos Alimentares
        Produtos de Primeiros Socorros
        Equipamentos Médicos

10. Livros e Papelaria

    Subcategorias:
        Livros (ficção, não-ficção, acadêmicos)
        Papelaria e Material Escolar
        Suprimentos para Escritório

11. Automotivo

    Subcategorias:
        Peças e Acessórios para Carros
        Pneus e Rodas
        Produtos de Manutenção (óleos, lubrificantes)
        Ferramentas Automotivas
"""
