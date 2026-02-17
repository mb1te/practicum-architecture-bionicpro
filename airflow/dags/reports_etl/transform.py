from collections import defaultdict
from datetime import date, datetime


def transform_and_join(
    clients: list[dict],
    telemetry: list[dict],
) -> list[dict]:
    clients_by_id = {str(c["id"]): c for c in clients}

    grouped = defaultdict(lambda: {
        "events_count": 0,
        "battery_sum": 0.0,
        "signal_sum": 0.0,
    })

    for item in telemetry:
        user_id = str(item["user_id"])
        if user_id not in clients_by_id or not item["created_at"]:
            continue

        report_date = date.fromisoformat(item["created_at"][:10])
        key = (user_id, report_date)
        grouped[key]["events_count"] += 1
        grouped[key]["battery_sum"] += item["battery_level"]
        grouped[key]["signal_sum"] += item["signal_strength"]

    loaded_at = datetime.utcnow()
    rows = []
    for (user_id, report_date), agg in grouped.items():
        client = clients_by_id[user_id]
        count = agg["events_count"]
        rows.append({
            "user_id": user_id,
            "report_date": report_date,
            "full_name": client["full_name"],
            "email": client["email"],
            "city": client["city"],
            "events_count": count,
            "avg_battery_level": agg["battery_sum"] / count if count else 0.0,
            "avg_signal_strength": agg["signal_sum"] / count if count else 0.0,
            "loaded_at": loaded_at,
        })

    return rows
