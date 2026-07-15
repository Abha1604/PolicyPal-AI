import streamlit as st

from components.Footer import render_footer
from components.Navbar import render_navbar

st.set_page_config(
    page_title="About — PolicyPal AI",
    layout="wide",
)

st.markdown(
    """
<style>
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
.block-container {
    padding-top: 0.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
iframe[title="streamlit.components.v1.html"] {
    margin-bottom: -8px;
}
</style>
""",
    unsafe_allow_html=True,
)

render_navbar()

st.title("About PolicyPal AI")

st.markdown(
    """
PolicyPal AI helps you understand contracts quickly by combining:

- **Document processing** — extract text from PDF, DOCX, and TXT files
- **Clause intelligence** — identify parties, dates, obligations, and key clauses
- **Risk scoring** — flag missing protections and risky terms with rule-based checks
- **AI explanations** — get summaries and answers in plain language

Upload a contract on the home page, choose an analysis type, and review the
results on the dashboard.
"""
)

render_footer()
