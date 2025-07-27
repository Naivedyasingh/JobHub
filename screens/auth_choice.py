#/auth_choice.py

import streamlit as st

def auth_choice_page():
    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    st.title(f"{role_name} – Authentication")
    st.write("What would you like to do?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True, type="primary", key="auth_login"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("✨ Sign Up", use_container_width=True, type="secondary", key="auth_signup"):
            st.session_state.page = "signup"
            st.rerun()

    if st.button("← Back", help="Change role selection", key="auth_back"):
        st.session_state.page = "home"
        st.session_state.role = None
        st.rerun()