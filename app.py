import streamlit as st
import pandas as pd
import psycopg


st.set_page_config(
    page_title="InsightWatch",
    page_icon="📊",
    layout="wide"
)

st.title("InsightWatch")
st.subheader("Automated Business Anomaly Detection & Intelligence System")


# Connect to Neon PostgreSQL
try:
    conn = psycopg.connect(st.secrets["NEON_DATABASE_URL"])

    query = """
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
            returned_units,
            return_value,
            cancellation_count,
            revenue_anomaly,
            severity,
            anomaly_direction,
            is_partial_day,
            primary_driver,
            summary,
            return_signal,
            supporting_metrics,
            investigations
        FROM insightwatch_dashboard
        ORDER BY metric_date
    """

    df = pd.read_sql(query, conn)

    conn.close()

    st.success("Connected to InsightWatch PostgreSQL database.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Daily Records", len(df))

    with col2:
        st.metric(
            "Detected Anomalies",
            int(df["revenue_anomaly"].sum())
        )

    st.divider()

    st.subheader("Detected Anomalies")

    anomalies = df[df["revenue_anomaly"] == True].copy()

    st.dataframe(
        anomalies[
            [
                "metric_date",
                "severity",
                "anomaly_direction",
                "revenue",
                "revenue_deviation_pct",
                "revenue_zscore",
                "primary_driver"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error("Could not load InsightWatch data.")
    st.code(str(e))
