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


    # Connection status

    st.success("Connected to InsightWatch PostgreSQL database.")


    # KPI calculations

    total_revenue = df["revenue"].sum()
    total_orders = df["orders"].sum()
    anomaly_count = int(df["revenue_anomaly"].sum())
    total_return_value = df["return_value"].sum()


    # KPI cards

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Revenue",
            f"£{total_revenue:,.0f}"
        )

    with col2:
        st.metric(
            "Total Orders",
            f"{total_orders:,.0f}"
        )

    with col3:
        st.metric(
            "Detected Anomalies",
            anomaly_count
        )

    with col4:
        st.metric(
            "Return Value",
            f"£{total_return_value:,.0f}"
        )


    st.divider()


    # -------------------------
    # Revenue trend
    # -------------------------

    st.subheader("Daily Revenue Trend")

    chart_data = df.set_index("metric_date")[
        ["revenue", "baseline_revenue"]
    ]

    st.line_chart(chart_data)


    st.divider()


    # -------------------------
    # Anomaly table
    # -------------------------

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


    st.divider()


    # -------------------------
    # Anomaly investigation
    # -------------------------

    st.subheader("Anomaly Investigation")

    selected_date = st.selectbox(
        "Select an anomaly date",
        anomalies["metric_date"].tolist()
    )

    selected = anomalies[
        anomalies["metric_date"] == selected_date
    ].iloc[0]


    # Anomaly overview

    st.markdown(
        f"### {selected_date} — "
        f"{selected['severity']} {selected['anomaly_direction']} Anomaly"
    )


    # Main metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Revenue",
            f"£{selected['revenue']:,.2f}"
        )

    with col2:
        st.metric(
            "Baseline Revenue",
            f"£{selected['baseline_revenue']:,.2f}"
        )

    with col3:
        st.metric(
            "Revenue Deviation",
            f"{selected['revenue_deviation_pct']:.2f}%"
        )

    with col4:
        st.metric(
            "Z-Score",
            f"{selected['revenue_zscore']:.2f}"
        )


    # Supporting metrics

    st.markdown("#### Supporting Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Orders", f"{selected['orders']:,}")

    with col2:
        st.metric("Customers", f"{selected['customers']:,}")

    with col3:
        st.metric("Units Sold", f"{selected['units_sold']:,}")

    with col4:
        st.metric("AOV", f"£{selected['aov']:,.2f}")

    with col5:
        st.metric(
            "Return Value",
            f"£{selected['return_value']:,.2f}"
        )


    # AI-generated insight

    st.markdown("#### AI-Assisted Insight")

    st.markdown(
        f"**Primary Driver:** {selected['primary_driver']}"
    )

    st.write(selected["summary"])


    st.markdown(
        f"**Return Signal:** {selected['return_signal']}"
    )


    # Investigations

    st.markdown("#### Suggested Investigations")

    investigations = selected["investigations"]

    if isinstance(investigations, list):
        for item in investigations:
            st.write(f"• {item}")
    else:
        st.write(investigations)


except Exception as e:
    st.error("Could not load InsightWatch data.")
    st.code(str(e))
