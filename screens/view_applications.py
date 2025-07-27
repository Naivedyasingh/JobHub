# pages/view_applications.py

import streamlit as st
from utils.applications import get_job_applications, update_application_status
from utils.offers import get_job_offers,update_offer_status
from datetime import datetime

def view_applications_page():
    """Page for employers to view and manage applications"""
    user = st.session_state.current_user
    
    st.title("📋 Manage Applications")
    
    applications = get_job_applications()
    my_applications = [app for app in applications if str(app.get('employer_id')) == str(user['id'])]
    
    if not my_applications:
        st.info("No applications received yet.")
        return
    
    # Separate by status
    pending_apps = [app for app in my_applications if app.get('status') == 'pending']
    accepted_apps = [app for app in my_applications if app.get('status') == 'accepted']
    rejected_apps = [app for app in my_applications if app.get('status') == 'rejected']
    
    # Tabs for different statuses
    tab1, tab2, tab3 = st.tabs([f"🟡 Pending ({len(pending_apps)})", f"🟢 Accepted ({len(accepted_apps)})", f"🔴 Rejected ({len(rejected_apps)})"])
    
    with tab1:
        st.subheader("Pending Applications")
        for app in pending_apps:
            display_application_card(app, show_actions=True)
    
    with tab2:
        st.subheader("Accepted Applications")
        for app in accepted_apps:
            display_application_card(app, show_actions=False)
    
    with tab3:
        st.subheader("Rejected Applications")
        for app in rejected_apps:
            display_application_card(app, show_actions=False)

def display_application_card(app, show_actions=True):
    """Display an application card with optional action buttons"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 👤 {app.get('applicant_name')}")
            st.write(f"**Applied for:** {app.get('job_title')}")
            st.write(f"📱 **Phone:** {app.get('applicant_phone')}")
            st.write(f"✉️ **Email:** {app.get('applicant_email')}")
            st.write(f"🛠️ **Skills:** {app.get('applicant_skills', 'Not specified')}")
            st.write(f"📈 **Experience:** {app.get('applicant_experience', 'Not specified')}")
            st.write(f"💰 **Expected Salary:** ₹{app.get('expected_salary', 'Not specified')}")
            st.write(f"📅 **Applied:** {app.get('applied_date', '')[:10]}")
        
        with col2:
            if show_actions and app.get('status') == 'pending':
                st.write("**Actions:**")
                
                # Accept button
                if st.button("✅ Accept", key=f"accept_app_{app['id']}", type="primary"):
                    update_application_status(app['id'], 'accepted', 'Application accepted')
                    st.success("Application accepted!")
                    st.rerun()
                
                # Reject button
                if st.button("❌ Reject", key=f"reject_app_{app['id']}"):
                    update_application_status(app['id'], 'rejected', 'Application rejected')
                    st.info("Application rejected.")
                    st.rerun()
                
                # Contact button
                if st.button("📞 Contact", key=f"contact_app_{app['id']}"):
                    st.success(f"📱 Call: {app.get('applicant_phone')}")
                    st.info(f"✉️ Email: {app.get('applicant_email')}")
        
        st.divider()
