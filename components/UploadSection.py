import streamlit as st
import os

from utils.integration import analyze_document

ANALYSIS_TYPES = [
    "Full Analysis",
    "Risk Detection",
    "Compliance Review",
    "Clause Extraction",
]


def render_upload_section():

    st.markdown("## Upload & Analyze")

    left, right = st.columns([2, 1])

    with left:
        with st.container(border=True):

            st.markdown(
                "<h2 style='text-align:center;'>📄 Upload Contract</h2>",
                unsafe_allow_html=True,
            )

            uploaded_file = st.file_uploader(
                "Drop your contract here",
                type=["pdf", "docx", "txt"],
            )

            st.markdown(
                "<p style='text-align:center;color:#888;'>PDF, DOCX, TXT</p>",
                unsafe_allow_html=True,
            )

    with right:

        st.markdown("### Analysis Type")

        analysis_type = st.selectbox(
            "Analysis Type",
            ANALYSIS_TYPES,
            label_visibility="collapsed",
        )

        st.markdown("### Your Question")
        st.caption("Optional for Full Analysis. Other modes use a focused default if left blank.")

        question = st.text_area(
            "Your Question",
            placeholder="e.g. What happens if I terminate early?",
            label_visibility="collapsed",
            height=100,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Analyze Contract",
            use_container_width=True,
        ):

            if uploaded_file is None:

                st.error("Please upload a contract first.")

            else:

                os.makedirs("temp", exist_ok=True)

                save_path = f"temp/{uploaded_file.name}"

                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with st.spinner("Analyzing Contract..."):

                    try:
                        structured_contract, analysis, metadata = analyze_document(
                            save_path,
                            question,
                            analysis_type,
                        )
                    except ValueError as e:
                        st.error(str(e))
                        st.stop()
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        st.stop()

                st.session_state.analysis = analysis
                st.session_state.structured_contract = structured_contract
                st.session_state.analysis_metadata = metadata

                st.switch_page("pages/Dashboard.py")

    st.markdown("<br><br>", unsafe_allow_html=True)
