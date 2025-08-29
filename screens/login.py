import streamlit as st
from utils.auth import authenticate

def login_page():
    st.markdown("""
    <style>
      #MainMenu {visibility: hidden;}
      header {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    role_icon = "🔍" if st.session_state.role == "job" else "🏢"

    st.markdown("""<style>
      .main>div{padding-left:0;padding-right:0;}
      h2{color:#1f77b4!important;}
      .stTextInput{width:860px!important;margin:0 auto!important;}
      .stTextInput>div{width:860px!important;max-width:860px!important;margin:0 auto!important;}
      .stTextInput>div>div>input{width:860px!important;max-width:860px!important;height:40px!important;font-size:1.2rem!important;padding:0.65rem 0.75rem!important;margin:0 auto!important;}
      .stTextInput>label{font-size:2rem!important;font-weight:800!important;margin-bottom:0.5rem!important;width:900px!important;margin-left:auto!important;margin-right:auto!important;color:#2c3e50!important;}
      .stButton>button[kind="primary"]{height:46px!important;width:500px!important;max-width:400px!important;font-size:0.9rem!important;padding:0.4rem 1.2rem!important;margin:0 auto!important;display:block!important;}
      .error-message{background:#f8d7da;color:#721c24;padding:0.6rem 0.9rem;border-radius:3px;border-left:3px solid #dc3545;margin:0.8rem auto;font-size:0.9rem;font-weight:600;max-width:600px;text-align:center;}
    </style>""", unsafe_allow_html=True)

    st.markdown(f"""<div style='text-align:center;margin-bottom:1.5rem;'><h2>{role_icon} {role_name} Login</h2><p style='color:#222;margin-top:0.5rem;'>Sign in to access your dashboard</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.markdown('<label style="font-size:1.1rem;font-weight:800;color:#2c3e50;margin-bottom:0.5rem;display:block;width:850px;margin:0 auto;">Name or Phone</label>', unsafe_allow_html=True)
    identifier = st.text_input("", key="login_identifier", placeholder="Enter name / phone", label_visibility="collapsed")
    st.markdown('<label style="font-size:1.1rem;font-weight:800;color:#2c3e50;margin-bottom:0.5rem;display:block;width:850px;margin:0 auto;">Password</label>', unsafe_allow_html=True)
    pwd = st.text_input("", type="password", key="login_password", placeholder="Enter password", label_visibility="collapsed")

    if st.button("🚀 Login", key="login_submit", type="primary"):
        if not identifier or not pwd:
            st.markdown('<div class="error-message">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            user = authenticate(identifier.strip(), pwd.strip(), st.session_state.role)
            if user:
                st.success(f"Welcome back, {user['name']}!")
                st.session_state.current_user = user
                st.session_state.page = f"{user['role']}_dashboard"
                st.rerun()
            else:
                st.markdown('<div class="error-message">❌ Invalid credentials. Please try again.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("".join(["─"] * 97))

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔑 Forgot Password", use_container_width=True):
            st.info("Please contact support to reset your password.")
    with col2:
        if st.button("📝 Create Account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
