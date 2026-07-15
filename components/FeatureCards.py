import streamlit as st

def render_feature_cards():

    st.markdown("## Features")

    row1 = st.columns(3)

    features = [
        (
            "⚡ Instant Analysis",
            "Analyze contracts in seconds."
        ),
        (
            "📑 Clause Extraction",
            "Extract payment, renewal and termination clauses."
        ),
        (
            "⚠ Risk Assessment",
            "Detect risky contract terms automatically."
        ),
        (
            "🤖 AI Assistant",
            "Ask questions in plain English."
        ),
        (
            "📊 Executive Summary",
            "Get concise contract insights."
        ),
        (
            "✅ Compliance Review",
            "Check for missing clauses."
        )
    ]

    for i, feature in enumerate(features):

        if i % 3 == 0:
            cols = st.columns(3)

        with cols[i % 3]:

            st.markdown(f"""
            <div style="
                border:1px solid #2a2a2a;
                border-radius:16px;
                padding:20px;
                min-height:180px;
                margin-bottom:20px;
            ">
                <h3>{feature[0]}</h3>
                <p>{feature[1]}</p>
            </div>
            """, unsafe_allow_html=True)