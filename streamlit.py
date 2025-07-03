import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Toll Log Dashboard", layout="wide")
st.title("🚦 Tolling Log Dashboard")

# File upload or local CSVs
log_file = st.file_uploader("Upload parsed_logs.csv", type="csv")
map_file = st.file_uploader("Upload vehicle_passage_map.csv", type="csv")
alarm_file = st.file_uploader("Upload alarm_thresholds.csv", type="csv")

# Load data
if log_file and map_file and alarm_file:
    df_logs = pd.read_csv(log_file)
    df_map = pd.read_csv(map_file)
    df_alarm = pd.read_csv(alarm_file)

    st.success("✅ Data loaded successfully")

    # Metrics
    total_entries = len(df_logs)
    tr_starts = (df_logs['event'] == 'TR Start').sum()
    tr_ends = (df_logs['event'] == 'TR End').sum()
    unique_usn = df_logs['USN'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Log Entries", total_entries)
    col2.metric("TR Start Events", tr_starts)
    col3.metric("TR End Events", tr_ends)
    col4.metric("Unique USNs", unique_usn)

    st.markdown("---")

    # Line Chart: TR Start and End Over Time
    df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
    df_logs['hour'] = df_logs['timestamp'].dt.floor('H')
    df_chart = df_logs.groupby(['hour', 'event']).size().unstack().fillna(0)

    st.subheader("📈 Hourly Transaction Events")
    st.line_chart(df_chart)

    st.markdown("---")

    # Passage ID vs USN mapping
    st.subheader("🔍 Vehicle to Passage ID Map")
    st.dataframe(df_map)

    st.markdown("---")

    # Alarms & Thresholds
    st.subheader("⚠️ Alarm Threshold Stats")
    st.dataframe(df_alarm)

    # Optional bar chart of any alarm %s
    percent_cols = df_alarm.select_dtypes(include='float').columns
    if not percent_cols.empty:
        col_option = st.selectbox("Select metric to plot", percent_cols)
        st.bar_chart(df_alarm.set_index('parameter')[col_option])
else:
    st.info("👈 Please upload all 3 CSV files to begin analysis.")
