# pages/hire_dashboard.py

import streamlit as st
from utils.data_helpers import read_json
from utils.applications import get_job_applications
from utils.offers import get_job_offers, update_offer_status
from utils.auth import calculate_profile_completion
from datetime import datetime


def hire_dashboard():
    user = st.session_state.current_user
    completion = calculate_profile_completion(user)
    
    st.title("🏢 Employer Dashboard")
    st.subheader(f"Welcome back, {user['name']}! 👋")
    
    # Quick actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Post New Job", use_container_width=True, type="primary", key="hire_post_job"):
            st.session_state.page = "post_job"
            st.rerun()
    
    with col2:
        if st.button("👥 Browse Job Seekers", use_container_width=True, key="hire_browse_seekers"):
            st.session_state.page = "browse_job_seekers"
            st.rerun()
    
    with col3:
        if st.button("📋 Applications", use_container_width=True, key="hire_view_applications"):
            st.session_state.page = "view_applications"
            st.rerun()
    
    with col4:
        if st.button("📊 My Jobs", use_container_width=True, key="hire_my_jobs"):
            st.session_state.page = "my_job_postings"
            st.rerun()
    
    st.markdown("---")
    
    # Show company stats
    applications = get_job_applications()
    my_applications = [app for app in applications if str(app.get('employer_id')) == str(user['id'])]
    my_jobs = user.get('job_postings', [])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jobs Posted", len(my_jobs))
    with col2:
        st.metric("Total Applications", len(my_applications))
    with col3:
        pending_apps = len([app for app in my_applications if app.get('status') == 'pending'])
        st.metric("Pending Applications", pending_apps)
    with col4:
        accepted_apps = len([app for app in my_applications if app.get('status') == 'accepted'])
        st.metric("Accepted", accepted_apps)
    
    # Recent applications preview
    st.subheader("📨 Recent Applications")
    recent_applications = sorted(my_applications, key=lambda x: x.get('applied_date', ''), reverse=True)[:3]
    
    if recent_applications:
        for app in recent_applications:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{app.get('applicant_name')}** applied for **{app.get('job_title')}**")
                    st.write(f"📱 {app.get('applicant_phone')} | ✉️ {app.get('applicant_email')}")
                
                with col2:
                    st.write(f"**Experience:** {app.get('applicant_experience')}")
                    st.write(f"**Skills:** {app.get('applicant_skills', 'Not specified')}")
                
                with col3:
                    status_colors = {
                        'pending': '🟡 Pending',
                        'accepted': '🟢 Accepted',
                        'rejected': '🔴 Rejected'
                    }
                    st.write(f"**Status:** {status_colors.get(app.get('status'), '🟡 Pending')}")
                
                st.divider()
    else:
        st.info("No applications received yet.")
