# /auth_choice.py

import streamlit as st

def auth_choice_page():
    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="color: #1f77b4; font-size: 2.5rem;">{role_name} – Authentication</h1>
        <p style="color: #555; font-size: 1.2rem; margin-top: 0.25rem;">
            What would you like to do?
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🔑 Login", type="primary",use_container_width=True, key="auth_login"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("✨ Sign Up", type="primary",use_container_width=True, key="auth_signup"):
            st.session_state.page = "signup"
            st.rerun()
    
      # Space between buttons and back button
   # Add vertical space above if needed
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Center the button in the middle of three columns
    _, col2, _ = st.columns([6.5, 4, 4])
    with col2:
        if st.button("← Back"):
            st.session_state.page = "home"
            st.session_state.role = None
            st.rerun()

