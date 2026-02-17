import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClickHouseConfig:
    host: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_HOST", "clickhouse"))
    port: int = field(default_factory=lambda: int(os.getenv("CLICKHOUSE_PORT", "8123")))
    username: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_USER", "airflow"))
    password: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_PASSWORD", "airflow"))
    database: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_DB", "default"))


@dataclass(frozen=True)
class KeycloakConfig:
    url: str = field(default_factory=lambda: os.getenv("KEYCLOAK_URL", "http://keycloak:8080").rstrip("/"))
    realm: str = field(default_factory=lambda: os.getenv("KEYCLOAK_REALM", "reports-realm"))
    user_claim: str = field(default_factory=lambda: os.getenv("REPORTS_USER_CLAIM", "sub"))

    @property
    def jwks_url(self) -> str:
        return f"{self.url}/realms/{self.realm}/protocol/openid-connect/certs"


@dataclass(frozen=True)
class AppConfig:
    clickhouse: ClickHouseConfig = field(default_factory=ClickHouseConfig)
    keycloak: KeycloakConfig = field(default_factory=KeycloakConfig)
    reports_table: str = field(default_factory=lambda: os.getenv("REPORTS_TABLE", "report_mart"))


def get_config() -> AppConfig:
    return AppConfig()
