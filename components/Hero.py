import streamlit as st

def render_hero():

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:

        st.markdown("""
        <h1 style="
            font-size:64px;
            font-weight:800;
            line-height:1.1;
            margin-bottom:20px;
        ">
            Understand Contracts<br>
            in Seconds
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="
            font-size:20px;
            color:#B3B3B3;
            line-height:1.8;
            margin-bottom:35px;
        ">
            Upload any legal contract and let PolicyPal AI
            automatically extract important clauses, identify risks,
            generate executive summaries, and explain complex legal
            language in simple English.
            <br><br>
            Save hours of manual review and make better decisions
            with AI-powered contract intelligence.
        </p>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1,1])

        with c1:
            st.button(
                "Upload Contract",
                use_container_width=True
            )

        with c2:
            st.button(
                "Learn More",
                use_container_width=True
            )

    with right:

        st.image(
            "assets/HeroImage.png",
            use_container_width=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
