from pathlib import Path

from .connections import REPORT_MART_COLUMNS, REPORT_MART_TABLE, get_clickhouse_client

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def load_to_clickhouse(rows: list[dict]) -> int:
    client = get_clickhouse_client()

    ddl = (SQL_DIR / "create_report_mart.sql").read_text()
    client.command(ddl)

    if not rows:
        return 0

    data = [
        [r[col] for col in REPORT_MART_COLUMNS]
        for r in rows
    ]
    client.insert(
        table=REPORT_MART_TABLE,
        data=data,
        column_names=REPORT_MART_COLUMNS,
    )
    return len(data)
