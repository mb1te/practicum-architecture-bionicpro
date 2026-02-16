from datetime import date, datetime

import clickhouse_connect
from clickhouse_connect.driver import Client

from .config import ClickHouseConfig


def get_client(config: ClickHouseConfig) -> Client:
    return clickhouse_connect.get_client(
        host=config.host,
        port=config.port,
        username=config.username,
        password=config.password,
        database=config.database,
    )


def get_max_processed_date(client: Client, table_name: str) -> date | None:
    try:
        result = client.query(f"SELECT max(report_date) FROM {table_name}")
    except Exception:
        return None
    if not result.result_rows:
        return None
    value = result.result_rows[0][0]
    if value is None:
        return None
    if isinstance(value, datetime):
        value = value.date()
    elif not isinstance(value, date):
        value = datetime.strptime(str(value), "%Y-%m-%d").date()
    if value == date(1970, 1, 1):
        return None
    return value


def fetch_reports(
    client: Client,
    table_name: str,
    user_id: str,
    report_date: str | None = None,
    limit: int = 100,
) -> list[dict[str, object]]:
    where_parts: list[str] = [f"user_id = '{user_id}'"]
    if report_date:
        where_parts.append(f"report_date = toDate('{report_date}')")

    where_sql = f"WHERE {' AND '.join(where_parts)}"
    query = f"""
        SELECT
            user_id,
            report_date,
            full_name,
            email,
            city,
            events_count,
            avg_battery_level,
            avg_signal_strength,
            loaded_at
        FROM {table_name}
        {where_sql}
        ORDER BY report_date DESC, user_id
        LIMIT {limit}
    """

    try:
        result = client.query(query)
    except Exception:
        return []

    return [
        {
            column: _to_json_value(value)
            for column, value in zip(result.column_names, row)
        }
        for row in result.result_rows
    ]


def _to_json_value(value: object) -> object:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value
