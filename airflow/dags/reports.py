from datetime import datetime

from airflow.decorators import dag, task

from reports_etl.extract import extract_clients as _extract_clients
from reports_etl.extract import extract_telemetry as _extract_telemetry
from reports_etl.load import load_to_clickhouse as _load_to_clickhouse
from reports_etl.transform import transform_and_join as _transform_and_join


@dag(
    dag_id="reports",
    description="Reports ETL DAG",
    schedule="0 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["reports"],
)
def reports_dag():

    @task(multiple_outputs=True)
    def get_interval(data_interval_start=None, data_interval_end=None):
        return {
            "interval_start": data_interval_start.isoformat(),
            "interval_end": data_interval_end.isoformat(),
        }

    @task
    def extract_clients(interval_start: str, interval_end: str):
        return _extract_clients(interval_start, interval_end)

    @task
    def extract_telemetry(interval_start: str, interval_end: str):
        return _extract_telemetry(interval_start, interval_end)

    @task
    def transform_and_join(clients, telemetry):
        return _transform_and_join(clients, telemetry)

    @task
    def load_to_clickhouse(rows):
        return _load_to_clickhouse(rows)

    interval = get_interval()
    clients = extract_clients(interval["interval_start"], interval["interval_end"])
    telemetry = extract_telemetry(interval["interval_start"], interval["interval_end"])
    transformed = transform_and_join(clients, telemetry)
    load_to_clickhouse(transformed)


reports_dag()
