# pages/my_applications.py

import streamlit as st
from utils.applications import get_job_applications
from datetime import datetime
from utils.offers import get_job_offers,update_offer_status

def my_applications_page():
    """Enhanced page showing job seeker's applications and offers"""
    user = st.session_state.current_user
    
    # Simple centered header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2c3e50; font-size: 2.2rem; margin-bottom: 10px;">📋 My Applications & Offers</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Get applications and offers
    applications = get_job_applications()
    offers = get_job_offers()
    
    my_applications = [app for app in applications if app.get('applicant_id') == user['id']]
    my_offers = [offer for offer in offers if offer.get('job_seeker_id') == user['id']]
    
    # Create tabs
    tab1, tab2 = st.tabs([f"💼 Job Offers ({len(my_offers)})", f"📤 My Applications ({len(my_applications)})"])
    
    with tab1:
        st.subheader("💼 Job Offers Received")
        
        if my_offers:
            for offer in my_offers:
                expires = datetime.fromisoformat(offer.get('expires_at', datetime.now().isoformat()))
                is_expired = datetime.now() > expires
                
                # Status styling
                if offer.get('status') == 'accepted':
                    border_color = "#28a745"
                    status_text = "✅ Accepted"
                elif offer.get('status') == 'rejected':
                    border_color = "#dc3545"
                    status_text = "❌ Declined"
                elif is_expired:
                    border_color = "#6c757d"
                    status_text = "⏰ Expired"
                else:
                    border_color = "#ffc107"
                    status_text = "🟡 Pending"
                
                st.markdown(f"""
                <div style="border: 2px solid {border_color}; border-radius: 10px; padding: 15px; margin: 10px 0;">
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### 💼 {offer.get('job_title')}")
                    st.write(f"🏢 **Company:** {offer.get('employer_name')}")
                    st.write(f"💰 **Salary:** ₹{offer.get('salary_offered')}")
                    st.write(f"📍 **Location:** {offer.get('location')}")
                    st.write(f"📅 **Start Date:** {offer.get('start_date')}")
                    st.write(f"💬 **Message:** {offer.get('personal_message', 'No message')}")
                    
                    if not is_expired:
                        time_left = expires - datetime.now()
                        hours_left = int(time_left.total_seconds() / 3600)
                        st.write(f"⏰ **Expires in:** {hours_left} hours")
                
                with col2:
                    st.write(f"**Status:** {status_text}")
                    
                    if offer.get('status') == 'pending' and not is_expired:
                        if st.button("✅ Accept", key=f"accept_{offer['id']}", type="primary"):
                            update_offer_status(offer['id'], 'accepted', 'Offer accepted')
                            st.success("Offer accepted!")
                            st.rerun()
                        
                        if st.button("❌ Decline", key=f"decline_{offer['id']}"):
                            update_offer_status(offer['id'], 'rejected', 'Offer declined')
                            st.info("Offer declined.")
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No job offers received yet.")
    
    with tab2:
        st.subheader("📤 My Job Applications")
        
        if my_applications:
            # Add filter controls
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Accepted", "Rejected"])
            with col2:
                sort_by = st.selectbox("Sort By", ["Date Applied", "Company", "Job Title"])
            
            # Apply filters and sorting
            filtered_apps = my_applications
            if status_filter != "All":
                filtered_apps = [app for app in my_applications if app.get('status', '').title() == status_filter]
            
            # Apply sorting
            sort_keys = {"Date Applied": lambda a: a.get('applied_date', ''), "Company": lambda a: a.get('employer_name', ''), "Job Title": lambda a: a.get('job_title', '')}
            filtered_apps.sort(key=sort_keys.get(sort_by, sort_keys["Date Applied"]), reverse=(sort_by == "Date Applied"))
            
            # Add CSS styles
            st.markdown("""<style>
            .job-card {background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 15px; padding: 20px; margin: 15px 0; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; border-left: 5px solid; position: relative; overflow: hidden;}
            .job-card:hover {transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);}
            .job-card::before {content: ''; position: absolute; top: 0; right: 0; width: 50px; height: 50px; background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.3)); border-radius: 0 15px 0 50px;}
            .job-title {color: #2c3e50; font-size: 1.3rem; font-weight: 600; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
            .job-company {color: #34495e; font-size: 1.1rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;}
            .job-date {color: #7f8c8d; font-size: 0.95rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
            .job-status {display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 0.9rem; font-weight: 500; margin-bottom: 10px;}
            .status-pending {background: #fff3cd; color: #856404; border: 1px solid #ffeaa7;}
            .status-accepted {background: #d4edda; color: #155724; border: 1px solid #c3e6cb;}
            .status-rejected {background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;}
            .job-response {background: #e8f4fd; border-left: 4px solid #3498db; padding: 10px; border-radius: 5px; margin-top: 10px; font-style: italic; color: #2c3e50;}
            </style>""", unsafe_allow_html=True)
            
            # Status configurations
            status_config = {
                'pending': ('#ffc107', 'status-pending', '🟡 Under Review'),
                'accepted': ('#28a745', 'status-accepted', '✅ Accepted'),
                'rejected': ('#dc3545', 'status-rejected', '❌ Rejected')
            }
            
            # Display applications in grid
            for i in range(0, len(filtered_apps), 2):
                col1, col2 = st.columns([1, 1], gap="large")
                
                # Helper function to render application card
                def render_card(app, column):
                    border_color, status_class, status_text = status_config.get(app.get('status'), status_config['pending'])
                    
                    with column:
                        st.markdown(f"""
                        <div class="job-card" style="border-left-color: {border_color};">
                            <div class="job-title">💼 {app.get('job_title', 'N/A')}</div>
                            <div class="job-company">🏢 {app.get('employer_name', 'N/A')}</div>
                            <div class="job-date">📅 Applied: {app.get('applied_date', '')[:10]}</div>
                            <div class="job-status {status_class}">{status_text}</div>
                            {f'<div class="job-response">💬 <strong>Response:</strong> {app.get("response_message")}</div>' if app.get('response_message') else ''}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Render first application
                render_card(filtered_apps[i], col1)
                
                # Render second application if exists
                if i + 1 < len(filtered_apps):
                    render_card(filtered_apps[i + 1], col2)
                else:
                    with col2:
                        st.markdown('<div style="height: 200px;"></div>', unsafe_allow_html=True)
        else:
            st.info("You haven't applied for any jobs yet.")