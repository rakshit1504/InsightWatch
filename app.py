import streamlit as st
import pandas as pd
import psycopg


# Page configuration

st.set_page_config(
    page_title="InsightWatch",
    page_icon="📊",
    layout="wide"
)


# Load data from PostgreSQL

@st.cache_data(ttl=300)
def load_data():

    conn = psycopg.connect(
        st.secrets["NEON_DATABASE_URL"]
    )

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

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# Main application

st.title("InsightWatch")

st.markdown(
    """
    **Automated Business Anomaly Detection & Intelligence System**  
    [View project on GitHub ↗](https://github.com/rakshit1504/InsightWatch)
    """
)

st.write(
    "InsightWatch detects unusual business performance, "
    "provides AI-assisted anomaly context, and presents "
    "the results through an interactive monitoring interface."
)


try:

    df = load_data()

    st.success(
        "Connected to InsightWatch PostgreSQL database."
    )


    # KPI calculations

    total_revenue = df["revenue"].sum()
    total_orders = df["orders"].sum()

    anomaly_count = int(
        df["revenue_anomaly"].sum()
    )

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


    # Revenue trend

    st.subheader("Daily Revenue Trend")

    chart_data = df.set_index("metric_date")[
        ["revenue", "baseline_revenue"]
    ]

    st.line_chart(
        chart_data,
        width="stretch"
    )


    st.divider()


    # Anomaly table

    st.subheader("Detected Anomalies")

    anomalies = df[
        df["revenue_anomaly"] == True
    ].copy()

    anomaly_table = anomalies[
        [
            "metric_date",
            "severity",
            "anomaly_direction",
            "revenue",
            "revenue_deviation_pct",
            "revenue_zscore",
            "primary_driver"
        ]
    ].copy()

    anomaly_table = anomaly_table.rename(
        columns={
            "metric_date": "Date",
            "severity": "Severity",
            "anomaly_direction": "Direction",
            "revenue": "Revenue",
            "revenue_deviation_pct": "Deviation %",
            "revenue_zscore": "Z-Score",
            "primary_driver": "Primary Driver"
        }
    )

    st.dataframe(
        anomaly_table,
        width="stretch",
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                "Revenue",
                format="£%.2f"
            ),
            "Deviation %": st.column_config.NumberColumn(
                "Deviation %",
                format="%.2f%%"
            ),
            "Z-Score": st.column_config.NumberColumn(
                "Z-Score",
                format="%.2f"
            )
        }
    )


    st.divider()


    # Anomaly investigation

    st.subheader("Anomaly Investigation")

    anomaly_dates = anomalies[
        "metric_date"
    ].tolist()

    selected_date = st.selectbox(
        "Select an anomaly date",
        anomaly_dates
    )

    selected = anomalies[
        anomalies["metric_date"] == selected_date
    ].iloc[0]


    st.markdown(
        f"### {selected_date} — "
        f"{selected['severity']} "
        f"{selected['anomaly_direction']} Anomaly"
    )


    # Main anomaly metrics

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
        st.metric(
            "Orders",
            f"{selected['orders']:,}"
        )

    with col2:
        st.metric(
            "Customers",
            f"{selected['customers']:,}"
        )

    with col3:
        st.metric(
            "Units Sold",
            f"{selected['units_sold']:,}"
        )

    with col4:
        st.metric(
            "AOV",
            f"£{selected['aov']:,.2f}"
        )

    with col5:
        st.metric(
            "Return Value",
            f"£{selected['return_value']:,.2f}"
        )


    # AI-assisted insight

    st.markdown("#### AI-Assisted Insight")

    primary_driver = selected["primary_driver"]
    summary = selected["summary"]
    return_signal = selected["return_signal"]

    if pd.isna(summary):

        st.info(
            "AI-generated insight is not available "
            "for this anomaly."
        )

        if not pd.isna(primary_driver):
            st.markdown(
                f"**Primary Driver:** {primary_driver}"
            )

    else:

        st.markdown(
            f"**Primary Driver:** {primary_driver}"
        )

        st.write(summary)

        st.markdown(
            f"**Return Signal:** {return_signal}"
        )


    # Suggested investigations

    st.markdown("#### Suggested Investigations")

    investigations = selected["investigations"]

    if isinstance(investigations, list):

        for item in investigations:
            st.write(f"• {item}")

    elif pd.isna(investigations):

        st.write(
            "No AI-generated investigations "
            "are available for this anomaly."
        )

    else:

        st.write(investigations)


    st.divider()


    # Project note

    st.caption(
        "InsightWatch is demonstrated using historical "
        "Online Retail II data. The application reads "
        "preprocessed results from PostgreSQL and does "
        "not represent a live production monitoring system."
    )

    st.markdown(
        """
        <div style="text-align: center; color: #888888; padding-top: 10px;">
            Built by <strong>Rakshit Bansal</strong> ·
            <a href="https://github.com/rakshit1504/InsightWatch"
               target="_blank"
               style="text-decoration: none;">
                GitHub ↗
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


except Exception as e:

    st.error(
        "Could not load InsightWatch data."
    )

    st.code(str(e))
