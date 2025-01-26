from enum import Enum
from controllers.routes_ecommrece.eletronics.route import route_eletronicos
from controllers.routes_ecommrece.Moda.route import route_moda
from controllers.routes_ecommrece.CasaDecoracao.route import route_cada_decoracao

# tags para ficar mais organizado
class Tags(Enum):
    eletronicos = "Eletronicos"
    moda = "Moda"
    casa_decoracao = "Casa e decoracao"
    users = "Users"


def routes(app):
    app.include_router(route_eletronicos, tags=[Tags.eletronicos], prefix="/ecoomerce")
    app.include_router(route_moda, tags=[Tags.moda], prefix="/ecoomerce")
    app.include_router(route_cada_decoracao, tags=[Tags.casa_decoracao], prefix="/ecoomerce")

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
