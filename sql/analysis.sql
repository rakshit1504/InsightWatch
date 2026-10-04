-- InsightWatch Analytical Queries
-- PostgreSQL / Neon


-- 1. Daily anomaly overview

SELECT
    metric_date,
    day_of_week,
    revenue,
    baseline_revenue,
    revenue_deviation_pct,
    revenue_zscore,
    orders,
    customers,
    units_sold,
    aov,
    severity,
    anomaly_direction
FROM daily_metrics
WHERE revenue_anomaly = TRUE
ORDER BY metric_date;


-- 2. Highest-severity anomalies

SELECT
    metric_date,
    severity,
    anomaly_direction,
    revenue,
    revenue_deviation_pct,
    revenue_zscore,
    orders,
    customers,
    units_sold,
    aov
FROM daily_metrics
WHERE revenue_anomaly = TRUE
ORDER BY
    CASE severity
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        ELSE 4
    END,
    ABS(revenue_zscore) DESC;


-- 3. AI-generated anomaly insights

SELECT
    anomaly_date,
    primary_driver,
    summary,
    return_signal,
    supporting_metrics,
    investigations
FROM anomaly_insights
ORDER BY anomaly_date;


-- 4. Dashboard view

CREATE OR REPLACE VIEW insightwatch_dashboard AS
SELECT
    d.metric_date,
    d.day_of_week,
    d.revenue,

    NULLIF(d.baseline_revenue, 'NaN'::numeric)
        AS baseline_revenue,

    NULLIF(d.revenue_deviation_pct, 'NaN'::numeric)
        AS revenue_deviation_pct,

    NULLIF(d.revenue_zscore, 'NaN'::numeric)
        AS revenue_zscore,

    d.orders,
    d.customers,
    d.units_sold,
    d.aov,

    d.returned_units,
    d.return_value,
    d.cancellation_count,

    d.revenue_anomaly,
    d.severity,
    d.anomaly_direction,
    d.is_partial_day,

    a.primary_driver,
    a.summary,
    a.return_signal,
    a.supporting_metrics,
    a.investigations

FROM daily_metrics d

LEFT JOIN anomaly_insights a
    ON d.metric_date = a.anomaly_date;


-- 5. Dashboard dataset check

SELECT COUNT(*) AS dashboard_rows
FROM insightwatch_dashboard;


-- 6. Alert history

SELECT
    anomaly_date,
    severity,
    anomaly_direction,
    revenue,
    revenue_deviation_pct,
    revenue_zscore,
    primary_driver,
    alert_status,
    sent_at
FROM alert_history
ORDER BY anomaly_date;
