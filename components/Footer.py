import streamlit as st

def render_footer():

    st.divider()

    st.markdown(
        """
        <h2 style='text-align:center;color:#B3B3B3;'>
            PolicyPal AI
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='text-align:center;color:#888888;'>
            AI-Powered Contract Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='text-align:center;color:#888888;'>
            © 2026 PolicyPal AI
        </div>
        """,
        unsafe_allow_html=True
    )