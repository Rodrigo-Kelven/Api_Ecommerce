from enum import Enum
from controllers.routes_ecommrece.eletronics.route import route_eletronicos
from controllers.routes_ecommrece.Moda.route import route_moda
from controllers.routes_ecommrece.CasaDecoracao.route import route_cada_decoracao
from controllers.routes_ecommrece.Automotivo.route import route_automotivo
from controllers.routes_ecommrece.Beleza.route import route_Beleza
from controllers.routes_ecommrece.BrinquedosJogos.route import route_brinquedos_jogos
from controllers.routes_ecommrece.EsportesLazer.route import route_esporte_lazer
from controllers.routes_ecommrece.LivrosPapelaria.route import route_livros_papelaria

from controllers.all_routes.route_all import route_all
from controllers.routes_users.routes import route_users
from controllers.Painel_Administrativo.route import router

# tags para ficar mais organizado
class Tags(Enum):
    eletronicos = "Eletronicos"
    moda = "Moda"
    beleza = "Beleza e Saude"
    casa_decoracao = "Casa e decoracao"
    users = "Users"
    user2 = "Teste Painel Admin Users"
    all_products = "All Products"
    automotivo = "Automotivo"
    brinquedos_jogos = "Brinquedos Jogos"
    esporte_lazer = "Esporte Lazer"
    livros_papelaria = "Livros Papelaria"




# definir todas as configuracoes de todas as rotas aqui, para deixar mais organizado possivel
def routes(app):
    app.include_router(route_eletronicos, tags=[Tags.eletronicos], prefix="/ecommerce")
    app.include_router(route_moda, tags=[Tags.moda], prefix="/ecommerce")
    app.include_router(route_cada_decoracao, tags=[Tags.casa_decoracao], prefix="/ecommerce")
    app.include_router(route_all, tags=[Tags.all_products], prefix="/ecommerce")
    app.include_router(route_users, tags=[Tags.users], prefix="/ecommerce")
    app.include_router(router, tags=[Tags.user2], prefix="/ecommerce/admin") # se for mudar a rota aqui, mude em todos as paginas HTML
    app.include_router(route_automotivo, tags=[Tags.automotivo], prefix="/ecommerce") 
    app.include_router(route_Beleza, tags=[Tags.beleza], prefix="/ecommerce") 
    app.include_router(route_brinquedos_jogos, tags=[Tags.brinquedos_jogos], prefix="/ecommerce") 
    app.include_router(route_esporte_lazer, tags=[Tags.esporte_lazer], prefix="/ecommerce") 
    app.include_router(route_livros_papelaria, tags=[Tags.livros_papelaria], prefix="/ecommerce") 


# atalho
"""
include_router(
    router: APIRouter,
    *,
    prefix: str = "",
    tags: List[str | Enum] | None = None,
    dependencies: Sequence[Depends] | None = None,
    responses: Dict[int | str, Dict[str, Any]] | None = None,
    deprecated: bool | None = None,
    include_in_schema: bool = True,
    default_response_class: type[Response] = Default(JSONResponse),
    callbacks: List[BaseRoute] | None = None,
    generate_unique_id_function: (APIRoute) -> str = Default(generate_unique_id)
) -> None
"""
