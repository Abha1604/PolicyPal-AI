import streamlit as st

def render_navbar():

    col1, col2 = st.columns([2,4])

    with col1:
        logo_col, text_col = st.columns([1,4])

        with logo_col: st.image("assets/logo.png", width=50)
        with text_col:
            st.markdown("""
            <div style="
                font-size:18px;
                font-weight:600;
                margin-top:5px;
            ">
                PolicyPal AI
            </div>
            """, unsafe_allow_html=True)
    # with col2:
    #     st.markdown(
    #         """
    #         <div style="
    #             display:flex;
    #             justify-content:center;
    #             gap:50px;
    #             font-size:18px;
    #             font-weight:600;
    #         ">
    #             <span>Home</span>
    #             <span>Dashboard</span>
    #             <span>About</span>
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )
    with col2:

        nav1, nav2, nav3 = st.columns(3)

        with nav1:
            st.button("Home")

        with nav2:
            if st.button("Dashboard"):
                st.switch_page("pages/Dashboard.py")

        with nav3:
            st.button("About")