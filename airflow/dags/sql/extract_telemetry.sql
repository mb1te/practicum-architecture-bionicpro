SELECT
    user_id,
    created_at,
    battery_level,
    signal_strength
FROM telemetry
WHERE created_at >= %(interval_start)s AND created_at < %(interval_end)s
