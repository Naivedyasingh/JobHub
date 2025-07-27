# pages/home.py

import streamlit as st

def home_page():
    st.title("🏢 JobConnect Portal")
    st.markdown("### Welcome! Choose your role to continue:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Job Seeker", use_container_width=True, type="secondary", key="home_job_seeker"):
            st.session_state.role = "job"
            st.session_state.page = "auth_choice"
            st.rerun()
    with col2:
        if st.button("🏢 Employer", use_container_width=True, type="secondary", key="home_employer"):
            st.session_state.role = "hire"
            st.session_state.page = "auth_choice"
            st.rerun()