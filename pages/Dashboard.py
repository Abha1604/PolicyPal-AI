import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

result = {
    "risk_score": 72,
    "risk_level": "Medium",
    "summary": "This contract contains payment, renewal and termination clauses.",
    "risks": [
        "Automatic Renewal",
        "Long Notice Period"
    ],
    "answer": "The contract is moderately risky because it automatically renews unless cancelled."
}

st.title("📊 Contract Analysis Dashboard")

st.markdown("---")

# Metrics Row

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Risk Score",
        f"{result['risk_score']}/100"
    )

with col2:
    st.metric(
        "Risk Level",
        result["risk_level"]
    )

with col3:
    st.metric(
        "Clauses Found",
        "3"
    )

with col4:
    st.metric(
        "Critical Risks",
        len(result["risks"])
    )

st.markdown("---")

# Executive Summary

st.subheader("Executive Summary")

st.info(result["summary"])

st.markdown("---")

# Detected Clauses

st.subheader("Detected Clauses")

c1, c2, c3 = st.columns(3)

with c1:
    st.success("✅ Payment")

with c2:
    st.success("✅ Renewal")

with c3:
    st.success("✅ Termination")

st.markdown("---")

# Risks

st.subheader("Key Risks")

for risk in result["risks"]:
    st.warning(risk)

st.markdown("---")

# AI Explanation

st.subheader("AI Explanation")

st.write(result["answer"])