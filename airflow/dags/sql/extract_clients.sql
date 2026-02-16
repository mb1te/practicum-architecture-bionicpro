SELECT
    id,
    full_name,
    email,
    city,
    updated_at
FROM clients
WHERE updated_at >= %(interval_start)s AND updated_at < %(interval_end)s
