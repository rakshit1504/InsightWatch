-- InsightWatch Database Schema
-- PostgreSQL / Neon

-- Daily business metrics and anomaly detection results

CREATE TABLE IF NOT EXISTS daily_metrics (
    metric_date DATE PRIMARY KEY,
    day_of_week VARCHAR(20),

    revenue NUMERIC,
    baseline_revenue NUMERIC,
    revenue_deviation_pct NUMERIC,
    revenue_zscore NUMERIC,

    orders INTEGER,
    customers INTEGER,
    units_sold BIGINT,
    aov NUMERIC,

    returned_units BIGINT,
    return_value NUMERIC,
    cancellation_count INTEGER,

    revenue_anomaly BOOLEAN,
    severity VARCHAR(20),
    anomaly_direction VARCHAR(20),

    is_partial_day BOOLEAN
);


-- AI-generated business insights for detected anomalies

CREATE TABLE IF NOT EXISTS anomaly_insights (
    anomaly_date DATE PRIMARY KEY,

    summary TEXT,
    primary_driver TEXT,
    supporting_metrics TEXT[],
    return_signal TEXT,
    investigations TEXT[]
);


-- Alert history

CREATE TABLE IF NOT EXISTS alert_history (
    id SERIAL PRIMARY KEY,

    anomaly_date DATE UNIQUE NOT NULL,
    severity VARCHAR(20),
    anomaly_direction VARCHAR(20),

    revenue NUMERIC,
    revenue_deviation_pct NUMERIC,
    revenue_zscore NUMERIC,

    primary_driver TEXT,

    alert_status VARCHAR(20) DEFAULT 'PENDING',
    sent_at TIMESTAMP
);


-- Helpful indexes


CREATE INDEX IF NOT EXISTS idx_daily_metrics_anomaly
ON daily_metrics (revenue_anomaly);

CREATE INDEX IF NOT EXISTS idx_anomaly_insights_date
ON anomaly_insights (anomaly_date);

CREATE INDEX IF NOT EXISTS idx_alert_history_status
ON alert_history (alert_status);
