import streamlit as st
import base64
from pathlib import Path

def _logo_base64() -> str:
    try:
        logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        return base64.b64encode(logo_path.read_bytes()).decode("utf-8")
    except Exception:
        return ""

def render_navbar():
    # 1. Inject pure CSS to force Streamlit columns and page links to form a tight header row
    st.markdown("""
    <style>
        /* Target the top row columns row container */
        div[data-testid="stHorizontalBlock"] {
            align-items: center !important;
            padding-bottom: 12px !important;
            margin-bottom: 1.5rem !important;
        }


        /* Logo Brand Container layout styling */
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 7px;
        }
        .navbar-brand img {
            width: 44px;
            height: 44px;
            object-fit: contain;
        }
        .navbar-brand span {
            font-size: 20px;
            font-weight: 600;
            color: #ffffff;
            white-space: nowrap;
        }
        .block-container {
            padding-top: 0.5rem !important;
        }

        /* Strip native Streamlit buttons into minimal aesthetic text links */
        div[data-testid="stPageLink-Container"] a {
            background-color: transparent !important;
            color: #b3b3b3 !important;
            border: none !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            padding: 0 0 4px 0 !important;
            text-decoration: none !important;
            transition: color 0.15s ease;
            box-shadow: none !important;
            border-bottom: 2px solid transparent !important;
            border-radius: 0px !important;
        }
        
        /* Link hover state styling */
        div[data-testid="stPageLink-Container"] a:hover {
            color: #ffffff !important;
            background-color: transparent !important;
        }

        /* Dynamic white underline active highlight */
        div[data-testid="stPageLink-Container"] a[aria-current="page"] {
            color: #ffffff !important;
            border-bottom: 2px solid #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. Use Streamlit columns safely, letting CSS collapse the space between them
    col_brand, spacer1, col_link1, col_link2, col_link3, spacer2 = st.columns(
        [4, 2, 1, 1.5, 1, 4]
    )

    with col_brand:
        st.markdown(f"""
        <div class="navbar-brand">
            <img src="data:image/png;base64,{_logo_base64()}" alt="PolicyPal logo" />
            <span>PolicyPal AI</span>
        </div>
        """, unsafe_allow_html=True)

    with col_link1:
        st.page_link("app.py", label="Home", icon=None)

    with col_link2:
        st.page_link("pages/Dashboard.py", label="Dashboard", icon=None)

    with col_link3:
        st.page_link("pages/About.py", label="About", icon=None)
