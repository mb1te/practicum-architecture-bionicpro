from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig

from .routes import get_reports, health

cors_config = CORSConfig(
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app = Litestar(
    route_handlers=[health, get_reports],
    cors_config=cors_config,
    openapi_config=OpenAPIConfig(
        title="Reports API",
        version="0.1.0",
        description="API for retrieving reports",
    ),
)
