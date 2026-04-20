CREATE TABLE IF NOT EXISTS ingested_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ingestion_metrics (
    id SERIAL PRIMARY KEY,
    total_records INTEGER DEFAULT 0,
    last_ingestion TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO ingestion_metrics (id, total_records, last_ingestion) 
VALUES (1, 0, NULL);

