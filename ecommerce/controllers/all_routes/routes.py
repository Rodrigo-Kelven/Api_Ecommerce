from enum import Enum
from controllers.routes_ecommrece.routes import route_ecom

# tags para ficar mais organizado
class Tags(Enum):
    ecommerce = "Ecommerce"
    products = "Products"
    users = "Users"

# adicionar mais rotas neste ecommerce

def routes(app):
    app.include_router(route_ecom, tags=[Tags.ecommerce], prefix="/ecoomerce")

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
