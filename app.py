import streamlit as st
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

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_metrics")
        daily_count = cur.fetchone()[0]

    conn.close()

    st.success("Connected to InsightWatch PostgreSQL database.")

    st.metric(
        "Daily Records",
        daily_count
    )

except Exception as e:
    st.error("Could not connect to the database.")
    st.code(str(e))
