# pages/hire_dashboard.py

import streamlit as st
from utils.applications import get_job_applications
from utils.auth import calculate_profile_completion

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
    my_applications = [
        app for app in applications
        if str(app.get("employer_id")) == str(user["id"])
    ]
    my_jobs = user.get("job_postings", [])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jobs Posted", len(my_jobs))
    with col2:
        st.metric("Total Applications", len(my_applications))
    with col3:
        pending_apps = len([app for app in my_applications if app.get("status") == "pending"])
        st.metric("Pending Applications", pending_apps)
    with col4:
        accepted_apps = len([app for app in my_applications if app.get("status") == "accepted"])
        st.metric("Accepted", accepted_apps)

    # Recent applications preview
    st.markdown("---")
    st.subheader("📨 Recent Applications")
    recent_applications = sorted(
        my_applications,
        key=lambda x: x.get("applied_date", ""),
        reverse=True
    )[:3]

    if recent_applications:
        for app in recent_applications:
            status = app.get("status", "pending")
            border_colors = {"pending": "#ffc107", "accepted": "#28a745", "rejected": "#dc3545"}
            status_colors = {"pending": "🟡 Pending", "accepted": "🟢 Accepted", "rejected": "🔴 Rejected"}
            
            border_color = border_colors.get(status, "#ffc107")
            status_text = status_colors.get(status, "🟡 Pending")
            
            name = app.get("applicant_name", "N/A")
            job = app.get("job_title", "N/A")
            phone = app.get("applicant_phone", "N/A")
            email = app.get("applicant_email", "N/A")
            experience = app.get("applicant_experience", "N/A")
            skills = app.get("applicant_skills", "Not specified")
            
            st.markdown(f"""
                <div style="border: 2px solid {border_color}; border-left: 5.5px solid {border_color}; border-radius: 10px; padding: 20px; margin: 15px 0; background-color: #f8f9fa; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="margin: 0 0 15px 0; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px;">{name} – {job}</h4>
                    <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 250px; margin-right: 20px;">
                            <p style="margin: 5px 0;"><strong>📱 Phone:</strong> {phone}</p>
                            <p style="margin: 5px 0;"><strong>✉️ Email:</strong> {email}</p>
                        </div>
                        <div style="flex: 1; min-width: 200px; margin-right: 20px;">
                            <p style="margin: 5px 0;"><strong>Experience:</strong> {experience}</p>
                            <p style="margin: 5px 0;"><strong>Skills:</strong> {skills}</p>
                        </div>
                        <div style="flex: 0 0 auto; min-width: 120px;">
                            <p style="margin: 5px 0;"><strong>Status:</strong> {status_text}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No applications received yet.")