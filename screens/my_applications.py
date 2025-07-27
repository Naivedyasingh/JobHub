# pages/my_applications.py

import streamlit as st
from utils.applications import get_job_applications
from datetime import datetime
from utils.offers import get_job_offers,update_offer_status

def my_applications_page():
    """Enhanced page showing job seeker's applications and offers"""
    user = st.session_state.current_user
    
    st.title("📋 My Applications & Offers")
    
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
            for app in my_applications:
                status_colors = {
                    'pending': ('#ffc107', '🟡 Under Review'),
                    'accepted': ('#28a745', '✅ Accepted'),
                    'rejected': ('#dc3545', '❌ Rejected')
                }
                
                color, status_text = status_colors.get(app.get('status'), ('#ffc107', '🟡 Under Review'))
                
                st.markdown(f"""
                <div style="border: 2px solid {color}; border-radius: 10px; padding: 15px; margin: 10px 0;">
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### 💼 {app.get('job_title')}")
                    st.write(f"🏢 **Company:** {app.get('employer_name')}")
                    st.write(f"📅 **Applied:** {app.get('applied_date', '')[:10]}")
                    if app.get('response_message'):
                        st.write(f"💬 **Response:** {app.get('response_message')}")
                
                with col2:
                    st.write(f"**Status:** {status_text}")
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("You haven't applied for any jobs yet.")
