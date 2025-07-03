import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def parse_logs(lines):
    pattern = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<event>TR START|TR END|SU ERROR) passage=(?P<passage>\w+) device=(?P<device>\w+)",
        re.IGNORECASE
    )

    entries = []
    for line in lines:
        match = pattern.search(line)
        if match:
            entries.append(match.groupdict())

    return pd.DataFrame(entries)

def generate_summary(df):
    summary = {
        "Total Logs": len(df),
        "Transactions Start": (df["event"] == "TR START").sum(),
        "Transactions End": (df["event"] == "TR END").sum(),
        "SU Errors": (df["event"] == "SU ERROR").sum(),
        "Unique Passages": df["passage"].nunique()
    }

    return pd.DataFrame.from_dict(summary, orient="index", columns=["Count"])

def plot_dashboard(df):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔄 Event Type Distribution")
        st.bar_chart(df["event"].value_counts())

    with col2:
        st.markdown("#### 🚧 Traffic Flow by Passage ID")
        st.bar_chart(df["passage"].value_counts())
