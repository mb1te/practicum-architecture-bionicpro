CREATE TABLE IF NOT EXISTS report_mart (
    user_id String,
    report_date Date,
    full_name Nullable(String),
    email Nullable(String),
    city Nullable(String),
    events_count UInt64,
    avg_battery_level Float64,
    avg_signal_strength Float64,
    loaded_at DateTime
)
ENGINE = MergeTree
ORDER BY (user_id, report_date)
