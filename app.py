import os
from dotenv import load_dotenv

load_dotenv()
print("API KEY =", os.getenv("GEMINI_API_KEY"))

import streamlit as st

from components.Navbar import render_navbar
from components.Hero import render_hero
from components.UploadSection import render_upload_section
from components.FeatureCards import render_feature_cards
from components.Footer import render_footer

st.set_page_config(
    page_title="PolicyPal AI",
    layout="wide"
)

# Custom Page Styling
st.markdown("""
<style>

/* Hide sidebar completely */
[data-testid="stSidebar"] {
    display: none;
}

/* Hide sidebar nav toggle button */
[data-testid="collapsedControl"] {
    display: none;
}

.block-container{
    padding-top:0.5rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)

render_navbar()
render_hero()
render_upload_section()
render_feature_cards()
render_footer()