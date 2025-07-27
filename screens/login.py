# pages/login.py

import streamlit as st
from utils.validation import validate_email, validate_phone
from utils.auth import authenticate
from utils.data_helpers import read_json

def login_page():
    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    st.title(f"🔑 {role_name} Login")

    identifier = st.text_input("📛 Name or Phone Number", key="login_identifier")
    pwd = st.text_input("🔒 Password", type="password", key="login_password")

    if st.button("🚀 Login", use_container_width=True, type="primary", key="login_submit"):
        if not identifier or not pwd:
            st.error("Please fill in all fields.")
            return

        user = authenticate(identifier.strip(), pwd.strip(), st.session_state.role)
        if user:
            st.success(f"Welcome back, {user['name']}!")
            st.session_state.current_user = user
            st.session_state.page = f"{user['role']}_dashboard"
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid credentials.")

    if st.button("← Back", key="login_back"):
        st.session_state.page = "auth_choice"
        st.rerun()