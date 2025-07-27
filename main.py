import streamlit as st
from utils.data_helpers import cleanup_user_data
from components.sidebar import render_sidebar

# Import each page module
from screens.home import home_page 
from screens.auth_choice import auth_choice_page
from screens.login import login_page
from screens.signup import signup_page
from screens.job_dashboard import job_dashboard
from screens.hire_dashboard import hire_dashboard
from screens.browse_seekers import browse_job_seekers_page
from screens.offer_job import offer_job_page
from screens.post_job import post_job_page
from screens.my_applications import my_applications_page
from screens.view_applications import view_applications_page
from screens.profile import profile_page
from screens.contact import contact_page

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def main():
    st.set_page_config(
        page_title="JobConnect Portal", 
        page_icon="💼", 
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ─── Sidebar toggle logic ───────────────────────────────────────
    if st.session_state.current_user is None:
        # Hide entire sidebar for guests (landing, login, signup)
        st.markdown(
            """
            <style>
              /* Hide sidebar panel and toggle button */
              [data-testid="stSidebar"] { display: none; }
              [data-testid="collapsedControl"] { display: none; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # Show your custom sidebar only when logged in
        render_sidebar()

    # ─── One-time cleanup ────────────────────────────────────────────
    if 'data_cleaned' not in st.session_state:
        cleanup_user_data()
        st.session_state.data_cleaned = True

    # ─── Main content area ──────────────────────────────────────────
    page = st.session_state.page

    if page == "home":
        home_page()
    elif page == "auth_choice":
        auth_choice_page()
    elif page == "login":
        login_page()
    elif page == "signup":
        signup_page()
    elif page == "job_dashboard":
        job_dashboard()
    elif page == "hire_dashboard":
        hire_dashboard()
    elif page == "profile":
        profile_page()
    elif page == "contact":
        contact_page()
    elif page == "browse_job_seekers":
        browse_job_seekers_page()
    elif page == "offer_job":
        offer_job_page()
    elif page == "my_applications":
        my_applications_page()
    elif page == "view_applications":
        view_applications_page()
    elif page == "post_job":
        post_job_page()
    else:
        st.session_state.page = "home"
        home_page()

if __name__ == "__main__":
    main()

