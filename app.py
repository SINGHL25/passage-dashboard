import streamlit as st
import pandas as pd
from utils.parser import parse_logs, generate_summary, plot_dashboard

st.set_page_config(page_title="Passage Dashboard", layout="wide")
st.title("🚦 Passage Dashboard")
st.markdown("Visualize transaction volume, SU alarms, and traffic flow")

uploaded_file = st.file_uploader("📄 Upload Toll Log File", type=["txt", "log"])

if uploaded_file:
    log_lines = uploaded_file.read().decode("utf-8").splitlines()
    df = parse_logs(log_lines)

    if df.empty:
        st.warning("No valid entries found.")
    else:
        st.success(f"Parsed {len(df)} log entries")
        st.dataframe(df.head(50))

        st.subheader("📊 Log Summary")
        summary_df = generate_summary(df)
        st.dataframe(summary_df)

        st.subheader("📈 Visualizations")
        plot_dashboard(df)
else:
    st.info("Upload a log file to begin.")
