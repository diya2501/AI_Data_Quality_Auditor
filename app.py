import streamlit as st
import pandas as pd


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Data Quality Auditor",
    page_icon="🔍",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🔍 AI Data Quality Auditor")
st.subheader(
    "Automated Data Quality Detection, Cleaning and Analysis"
)

st.write(
    "This dashboard analyzes a dirty dataset, detects data-quality "
    "issues, provides correction suggestions and compares data "
    "quality before and after cleaning."
)


# ==========================================
# LOAD FILES
# ==========================================

dirty_df = pd.read_csv(
    "AI_Auditor_Input_Dirty_1000.csv"
)

cleaned_df = pd.read_csv(
    "cleaned_orders.csv"
)

error_report = pd.read_csv(
    "Complete_Error_Report.csv"
)

quality_report = pd.read_csv(
    "Data_Quality_Score_Report.csv"
)

ml_report = pd.read_csv(
    "ML_Anomaly_Report.csv"
)


# ==========================================
# BASIC METRICS
# ==========================================

total_records = len(dirty_df)

total_errors = error_report["Error Count"].sum()

before_score = quality_report.loc[
    quality_report["Metric"] == "Before Cleaning Score",
    "Score"
].iloc[0]

after_score = quality_report.loc[
    quality_report["Metric"] == "After Cleaning Score",
    "Score"
].iloc[0]

ml_anomalies = len(ml_report)


# ==========================================
# DASHBOARD METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        total_records
    )

with col2:
    st.metric(
        "Detected Issues",
        int(total_errors)
    )

with col3:
    st.metric(
        "Before Score",
        f"{before_score:.2f}/100"
    )

with col4:
    st.metric(
        "After Score",
        f"{after_score:.2f}/100"
    )


# ==========================================
# QUALITY IMPROVEMENT
# ==========================================

st.divider()

improvement = after_score - before_score

st.success(
    f"Data Quality Improvement: {improvement:.2f} points"
)


# ==========================================
# ERROR REPORT
# ==========================================

st.header("📊 Data Quality Error Analysis")

st.dataframe(
    error_report,
    use_container_width=True
)


# ==========================================
# ERROR CHART
# ==========================================

st.header("📈 Error Distribution")

st.bar_chart(
    error_report.set_index("Error Type")["Error Count"]
)


# ==========================================
# ML ANOMALIES
# ==========================================

st.header("🤖 Machine Learning Anomalies")

st.write(
    "Isolation Forest identified potentially unusual "
    "price and quantity combinations."
)

st.metric(
    "ML Anomalies Detected",
    ml_anomalies
)

st.dataframe(
    ml_report,
    use_container_width=True
)


# ==========================================
# DATA PREVIEW
# ==========================================

st.header("📋 Cleaned Dataset Preview")

st.dataframe(
    cleaned_df.head(20),
    use_container_width=True
)


# ==========================================
# DOWNLOAD CLEAN DATASET
# ==========================================

st.download_button(
    label="⬇️ Download Cleaned Dataset",
    data=cleaned_df.to_csv(index=False),
    file_name="cleaned_orders.csv",
    mime="text/csv"
)


# ==========================================
# PROJECT SUMMARY
# ==========================================

st.divider()

st.header("📌 Project Summary")

st.write(
    """
    The AI Data Quality Auditor combines SQL validation,
    Python-based data auditing, rule-based correction suggestions,
    and machine-learning anomaly detection.

    The system identifies data-quality problems and generates
    a cleaned dataset along with reports and quality metrics.
    """
)

st.caption(
    "AI Data Quality Auditor — Final Year Project"
)