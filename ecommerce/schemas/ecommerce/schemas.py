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


class ProductSaudeMedicamentos(BaseModel):
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Raspador de Lingua"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[15.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Prata"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Adukto"])


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


class ProductAutomotivoID(BaseModel):
    id: int
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
    id: int
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
    id: int
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
    id: int
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Velocipe"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[50.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Branco e Azul"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Policia"])

class ProductSaudeMedicamentosID(BaseModel):
    id: int
    name: str = Field(..., title="Name Product",description="Name of product",examples=["Raspador de Lingua"])
    description: str = Field(None, title="Description product", description="Description of products", examples=["Good Product, Stars 5"])
    price: float = Field(..., title="Price Product", description="Price of product",examples=[15.00])
    quantity: int = Field(..., title="Amount of product", description="Amount of product", examples=[1])
    tax: float = Field(None, title="Tax Product", description="Tax of product",examples=[0.1])
    stars: float = Field(None, title="Stars of product", description="Stars of avaliation product", examples=[5.0])
    color: str = Field(..., title="color product", description="Color of product", examples=["Prata"])
    size: int = Field(..., title="size product", description="size product in CM", examples=["34"])
    details: str = Field(None, title="details products", description="details of products", examples=["Adukto"])


class ProductLivrosPapelariaID(BaseModel):
    id: int
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

class EspecificacoesBelezaCuidados(ProductBelezaeCuidadosID):
    category: Literal["Beleza_e_cuidados"] = "Beleza_e_cuidados" 

class EspecificacoesEsporteLazer(ProductEsporteLazerID):
    category: Literal["Esporte_Lazer"] = "Esporte_Lazer" 

class EspecificacoesBrinquedosJogos(ProductBrinquedosJogosID):
    category: Literal["Brinquedos_Jogos"] = "Brinquedos_Jogos" 

class EspecificacoesSaudeMedicamentos(ProductSaudeMedicamentosID):
    category: Literal["Saude_Medicamentos"] = "Saude_Medicamentos" 

class EspecificacoesLivrosPapelaria(ProductLivrosPapelariaID):
    category: Literal["Livros_Papelaria"] = "Livros_Papelaria" 

class EspecificacoesAutomotivo(ProductAutomotivoID):
    category: Literal["Automotivo"] = "Automotivo" # somente passando a Litral é suficiente para setar o valor desejado


""" # Este método valida que o campo "category" não seja modificado
    def dict(self, *args, **kwargs):
        kwargs['exclude_unset'] = True
        original = super().dict(*args, **kwargs)
        if 'category' in original:
            original['category'] = self.category
        return original
 """   

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

10. Livros_Papelaria

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
