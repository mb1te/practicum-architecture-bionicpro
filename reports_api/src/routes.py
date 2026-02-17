import re
from datetime import datetime

from litestar import Request, get
from litestar.exceptions import HTTPException

from .auth import extract_user_id
from .config import get_config
from .db import fetch_reports, get_client, get_max_processed_date

config = get_config()


@get("/health")
async def health() -> dict[str, str]:
    try:
        client = get_client(config.clickhouse)
        client.command("SELECT 1")
        return {"status": "ok"}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"ClickHouse unavailable: {exc}",
        ) from exc


@get("/reports")
async def get_reports(
    request: Request,
    date: str | None = None,
    user_id: str | None = None,
) -> dict[str, list[dict[str, object]]]:
    current_user_id = extract_user_id(request, config.keycloak)

    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail="date must be YYYY-MM-DD",
            ) from exc

    if user_id and user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You can request reports only for yourself",
        )

    effective_user_id = current_user_id
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", effective_user_id):
        raise HTTPException(
            status_code=400,
            detail="user_id must match [A-Za-z0-9_-]{1,64}",
        )

    requested_date = (
        datetime.strptime(date, "%Y-%m-%d").date() if date else None
    )

    client = get_client(config.clickhouse)
    max_processed_date = get_max_processed_date(client, config.reports_table)

    if requested_date and (
        not max_processed_date or requested_date > max_processed_date
    ):
        max_str = (
            max_processed_date.isoformat()
            if max_processed_date
            else "not available yet"
        )
        raise HTTPException(
            status_code=409,
            detail=(
                f"Requested date {requested_date.isoformat()} is not processed "
                f"by Airflow yet. Latest available date: {max_str}"
            ),
        )

    items = fetch_reports(
        client=client,
        table_name=config.reports_table,
        user_id=effective_user_id,
        report_date=date,
    )

    return {"items": items}
