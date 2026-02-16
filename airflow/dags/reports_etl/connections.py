import clickhouse_connect
from airflow.hooks.base import BaseHook

CRM_CONN_ID = "crm_postgres"
TELEMETRY_CONN_ID = "telemetry_postgres"
CLICKHOUSE_CONN_ID = "clickhouse"

REPORT_MART_TABLE = "report_mart"
REPORT_MART_COLUMNS = [
    "user_id",
    "report_date",
    "full_name",
    "email",
    "city",
    "events_count",
    "avg_battery_level",
    "avg_signal_strength",
    "loaded_at",
]


def get_clickhouse_client():
    conn = BaseHook.get_connection(CLICKHOUSE_CONN_ID)
    return clickhouse_connect.get_client(
        host=conn.host,
        port=conn.port or 8123,
        username=conn.login or "default",
        password=conn.password or "",
        database=conn.schema or "default",
    )
