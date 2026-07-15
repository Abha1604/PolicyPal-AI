import streamlit as st

def render_upload_section():

    st.markdown("## Upload & Analyze")

    left, right = st.columns([2,1])

    with left:
        with st.container(border=True):

            st.markdown(
                "<h2 style='text-align:center;'>📄 Upload Contract</h2>",
                unsafe_allow_html=True
            )

            uploaded_file = st.file_uploader(
                "Drop your contract here",
                type=["pdf", "docx", "txt"]
            )

            st.markdown(
                "<p style='text-align:center;color:#888;'>PDF, DOCX, TXT</p>",
                unsafe_allow_html=True
            )

    with right:

        st.markdown("### Analysis Type")

        analysis_type = st.selectbox(
            "",
            [
                "Full Analysis",
                "Risk Detection",
                "Compliance Review",
                "Clause Extraction"
            ]
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.button(
            "Analyze Contract",
            use_container_width=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)