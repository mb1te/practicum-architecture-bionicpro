CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    city TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS telemetry (
    user_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    battery_level DOUBLE PRECISION,
    signal_strength DOUBLE PRECISION
);

-- Demo data: user IDs match Keycloak usernames
INSERT INTO clients (id, full_name, email, city, updated_at) VALUES
    ('user1',      'User One',        'user1@example.com',      'Moscow',           NOW() - INTERVAL '30 minutes'),
    ('user2',      'User Two',        'user2@example.com',      'Saint Petersburg',  NOW() - INTERVAL '30 minutes'),
    ('admin1',     'Admin One',       'admin1@example.com',     'Moscow',            NOW() - INTERVAL '30 minutes'),
    ('prothetic1', 'Prothetic One',   'prothetic1@example.com', 'Kazan',             NOW() - INTERVAL '30 minutes'),
    ('prothetic2', 'Prothetic Two',   'prothetic2@example.com', 'Novosibirsk',       NOW() - INTERVAL '30 minutes'),
    ('prothetic3', 'Prothetic Three', 'prothetic3@example.com', 'Sochi',             NOW() - INTERVAL '30 minutes');

INSERT INTO telemetry (user_id, created_at, battery_level, signal_strength) VALUES
    ('user1',      NOW() - INTERVAL '40 minutes', 80.0, 65.0),
    ('user1',      NOW() - INTERVAL '10 minutes', 78.0, 68.0),
    ('user2',      NOW() - INTERVAL '25 minutes', 92.0, 82.0),
    ('admin1',     NOW() - INTERVAL '35 minutes', 87.0, 74.0),
    ('prothetic1', NOW() - INTERVAL '45 minutes', 85.0, 70.0),
    ('prothetic1', NOW() - INTERVAL '15 minutes', 82.0, 75.0),
    ('prothetic2', NOW() - INTERVAL '30 minutes', 90.0, 80.0),
    ('prothetic3', NOW() - INTERVAL '20 minutes', 88.0, 72.0);
