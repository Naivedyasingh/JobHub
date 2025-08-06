import streamlit as st
import base64
import os
from utils.data_helpers import cleanup_user_data
from components.sidebar import render_sidebar
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


if "page" not in st.session_state:
    st.session_state.page = "home"
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None


def main():

    # Load video for background
    video_path = r".streamlit/background_video.mp4"  
    if not os.path.exists(video_path):
        st.error(f"Video file not found: {video_path}")
        st.stop()

    with open(video_path, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
        #bgvid {{
            position: fixed; top:0; left:0;
            width:100vw; height:100vh;
            object-fit:cover;
            z-index:-1;
            filter: blur(13px) brightness(0.92);
            pointer-events:none;
        }}
        .stApp {{ background: transparent; }}
        .css-1d391kg {{ background-color: #f8f9fa; }}   /* optional sidebar bg if needed */
        .block-container {{ background-color: transparent; }}
    </style>
    <video id="bgvid" autoplay muted loop>
        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

    # Set page config and custom background styles
    st.set_page_config(
        page_title="JobHub Portal",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    # Render sidebar if logged in
    if st.session_state.current_user:
        render_sidebar()

    # Cleanup user data once
    if 'data_cleaned' not in st.session_state:
        cleanup_user_data()
        st.session_state.data_cleaned = True

    # Page routing
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
