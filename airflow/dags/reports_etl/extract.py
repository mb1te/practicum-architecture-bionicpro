from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook

from .connections import CRM_CONN_ID, TELEMETRY_CONN_ID

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def extract_clients(interval_start: str, interval_end: str) -> list[dict]:
    hook = PostgresHook(postgres_conn_id=CRM_CONN_ID)
    sql = (SQL_DIR / "extract_clients.sql").read_text()
    return [
        {
            "id": r[0],
            "full_name": r[1],
            "email": r[2],
            "city": r[3],
            "updated_at": r[4].isoformat() if r[4] else None,
        }
        for r in hook.get_records(
            sql,
            parameters={"interval_start": interval_start, "interval_end": interval_end},
        )
    ]


def extract_telemetry(interval_start: str, interval_end: str) -> list[dict]:
    hook = PostgresHook(postgres_conn_id=TELEMETRY_CONN_ID)
    sql = (SQL_DIR / "extract_telemetry.sql").read_text()
    return [
        {
            "user_id": r[0],
            "created_at": r[1].isoformat() if r[1] else None,
            "battery_level": float(r[2]) if r[2] is not None else 0.0,
            "signal_strength": float(r[3]) if r[3] is not None else 0.0,
        }
        for r in hook.get_records(
            sql,
            parameters={"interval_start": interval_start, "interval_end": interval_end},
        )
    ]
