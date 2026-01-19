import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="UIDAI Enrolment Intelligence",
    layout="wide"
)

# ===============================
# 📂 DEPLOYMENT-SAFE PATH SETUP
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "output")

# ===============================
# 📊 LOAD ONLY REQUIRED DATASETS
# ===============================
district_month = pd.read_csv(
    os.path.join(DATA_DIR, "district_month_features.csv")
)
age_state = pd.read_csv(
    os.path.join(DATA_DIR, "age_state_summary.csv")
)

intelligence = pd.read_csv(
    os.path.join(DATA_DIR, "enrolment_intelligence.csv")
)



st.title("📊 Aadhaar Enrolment Intelligence Dashboard")
st.markdown(
    "Advanced analytics-driven insights for coverage, stability, and risk prioritization."
)


# ===============================
# STATE SELECTION
# ===============================
state_list = sorted(district_month["state"].unique())

selected_state = st.sidebar.selectbox(
    "Select State",
    state_list
)


    # Filter age data for selected state
age_state_filtered = age_state[
    age_state["state"] == selected_state
]

    
)



district_month = district_month[district_month["state"] == selected_state]
intelligence = intelligence[intelligence["state"] == selected_state]
#enrolment = enrolment[enrolment["state"] == selected_state]

trend = (
    district_month.groupby(["year", "month"])["enrolments"]
    .sum()
    .reset_index()
)

fig = px.line(
    trend,
    x="month",
    y="enrolments",
    title="Monthly Enrolment Trend"
)

st.plotly_chart(fig, use_container_width=True)


risk_count = intelligence["risk_level"].value_counts().reset_index()
risk_count.columns = ["Risk Level", "District Count"]

fig = px.bar(
    risk_count,
    x="Risk Level",
    y="District Count",
    title="District Risk Distribution",
    color="Risk Level"
)

st.plotly_chart(fig, use_container_width=True)


fig = px.scatter(
    intelligence,
    x="mean_enrolments",
    y="volatility",
    color="cluster",
    title="District Behaviour Clusters",
    hover_data=["district"]
)

st.plotly_chart(fig, use_container_width=True)


age_summary = enrolment.groupby("state")[[
    "age_0_5", "age_5_17", "age_18_greater"
]].sum().reset_index()

age_melt = age_state_filtered.melt(
    id_vars="state",
    value_vars=["age_0_5", "age_5_17", "age_18_greater"],
    var_name="Age Group",
    value_name="Enrolments"
)

fig = px.pie(
    age_melt,
    names="Age Group",
    values="Enrolments",
    title="Age-wise Enrolment Distribution"
)

st.plotly_chart(fig, width="stretch")

st.subheader("👶🧑 Age-wise Enrolment Composition")

high_risk = intelligence[intelligence["risk_level"] == "High"][
    ["district", "mean_enrolments", "volatility", "risk_score"]
]

st.dataframe(high_risk)






