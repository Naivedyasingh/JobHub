# pages/browse_seekers.py

import datetime
import streamlit as st
from utils.auth import calculate_profile_completion
from utils.applications import get_job_applications
from utils.offers import get_job_offers
from utils.data_helpers import read_json
from datetime import datetime as dt  # for parsing ISO timestamps

def get_job_seekers():
    """Get all job seekers with complete profiles"""
    users = read_json("data/users.json")
    job_seekers = []
    for user in users:
        if user.get('role') == 'job' and calculate_profile_completion(user) == 100:
            job_seekers.append(user)
    return job_seekers

def browse_job_seekers_page():
    """Job seeker cards with clean native Streamlit styling"""
    user = st.session_state.current_user

    st.title("👥 Browse Job Seekers")
    st.subheader("Find the perfect candidate for your job")

    seekers = get_job_seekers()
    if not seekers:
        st.info("No job seekers with complete profiles found.")
        return

    # Filters
    cols = st.columns(3)
    with cols[0]:
        skill_filter = st.selectbox(
            "Filter by Skills",
            ["All"] + sorted({skill for s in seekers for skill in s.get('job_types', [])}),
            key="skill_filter"
        )
    with cols[1]:
        exp_filter = st.selectbox(
            "Experience",
            ["All", "Fresher", "1-2 years", "2-5 years", "5+ years"],
            key="experience_filter"
        )
    with cols[2]:
        avail_filter = st.selectbox(
            "Availability",
            ["All", "available", "busy", "not_available"],
            key="availability_filter"
        )

    # Apply filters
    filtered = seekers
    if skill_filter != "All":
        filtered = [s for s in filtered if skill_filter in s.get('job_types', [])]
    if exp_filter != "All":
        filtered = [s for s in filtered if s.get('experience') == exp_filter]
    if avail_filter != "All":
        filtered = [s for s in filtered if s.get('availability_status', 'available') == avail_filter]

    st.write(f"**Found {len(filtered)} job seekers**")

    # Pre-load offers once
    all_offers = get_job_offers()

    # Display seekers in grid layout (2 cards per row)
    for i in range(0, len(filtered), 2):
        cols = st.columns(2, gap="medium")
        
        for j, col in enumerate(cols):
            if i + j < len(filtered):
                seeker = filtered[i + j]
                
                with col:
                    # Get status and styling
                    status = seeker.get('availability_status', 'available')
                    
                    if status == 'available':
                        status_color = "🟢"
                        status_text = "Available"
                        card_type = "success"
                    elif status == 'busy':
                        status_color = "🟡"
                        status_text = "Busy"
                        card_type = "warning"
                    else:
                        status_color = "🔴"
                        status_text = "Not Available"
                        card_type = "error"

                    # Create card using Streamlit container with colored border
                    with st.container(border=True):
                        # Status header with colored background
                        if status == 'available':
                            st.success(f"{status_color} {status_text}", icon="✅")
                        elif status == 'busy':
                            st.warning(f"{status_color} {status_text}", icon="⚠️")
                        else:
                            st.error(f"{status_color} {status_text}", icon="❌")
                        
                        # Name and profile
                        st.markdown(f"### 👤 {seeker['name']}")

                        st.markdown(" ")

                        # Quick info in three columns (with divider)
                        info_col1, divider_col, info_col2 = st.columns([5, 1, 5])
                        
                        with info_col1:
                            st.markdown("**💼 Experience**")
                            st.write(f"⏱️ {str(seeker.get('experience', 'Not specified'))}")
                            salary = seeker.get("expected_salary", "Not specified")
                            st.write(f"💰 {str(salary)}")
                        
                        with divider_col:
                            st.markdown(
                                """
                                <div style="
                                    border-left: 2px solid #e0e0e0; 
                                    height: 110px; 
                                    margin-left: 10%;
                                "></div>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                        with info_col2:
                            st.markdown("**📞 Contact**")
                            st.write(f"📱 {str(seeker.get('phone', 'N/A'))}")
                            st.write(f"🏙️ {str(seeker.get('city', 'Not specified'))}")

                        st.markdown("---")

                        # Action buttons
                        # Check for recent offer
                        recent = None
                        for o in all_offers:
                            if o.get("employer_id") == user["id"] and o.get("job_seeker_id") == seeker["id"]:
                                odt = dt.fromisoformat(o["offered_date"])
                                delta = datetime.datetime.now() - odt
                                if delta.total_seconds() < 24*3600:
                                    recent = delta
                                    break
                        
                        # Action button row
                        action_col1, action_col2 = st.columns(2)
                        
                        with action_col1:
                            if status != 'available':
                                st.button("❌ Not Available", disabled=True, use_container_width=True, key=f"disabled_{seeker['id']}")
                            else:
                                if recent:
                                    hrs = int(recent.total_seconds() // 3600)
                                    st.button(f"⌛ Offered ({hrs}h ago)", disabled=True, use_container_width=True, key=f"recent_{seeker['id']}")
                                else:
                                    if st.button("💼 Offer Job", type="primary", use_container_width=True, key=f"offer_{seeker['id']}"):
                                        st.session_state.selected_candidate = seeker
                                        st.session_state.page = "offer_job"
                                        st.rerun()
                        
                        with action_col2:
                            # Toggle details button
                            details_key = f"show_details_{seeker['id']}"
                            if details_key not in st.session_state:
                                st.session_state[details_key] = False
                            
                            if st.button("👁️ Details", use_container_width=True, key=f"details_btn_{seeker['id']}"):
                                st.session_state[details_key] = not st.session_state[details_key]

                        # Show details if toggled
                        if st.session_state.get(details_key, False):
                            st.markdown("---")
                            st.markdown("### 📋 Full Details")
                            
                            # Detailed info in tabs for better organization
                            tab1, tab2, tab3 = st.tabs(["📧 Contact", "💼 Professional", "🚨 Emergency"])
                            
                            with tab1:
                                st.write(f"**📧 Email:** {str(seeker.get('email', 'N/A'))}")
                                st.write(f"**📱 Phone:** {str(seeker.get('phone', 'N/A'))}")
                                st.write(f"**🏠 Address:** {str(seeker.get('address', 'Not provided'))}")
                                st.write(f"**🏙️ City:** {str(seeker.get('city', 'Not specified'))}")
                            
                            with tab2:
                                st.write(f"**🎓 Education:** {str(seeker.get('education', 'Not specified'))}")
                                st.write(f"**⏱️ Experience:** {str(seeker.get('experience', 'Not specified'))}")
                                st.write(f"**💰 Expected Salary:** {str(seeker.get('expected_salary', 'Not specified'))}")
                                st.write(f"**📅 Notice Period:** {str(seeker.get('notice_period', 'Not specified'))}")
                                
                                st.write("**🛠️ All Skills:**")
                                skills = seeker.get("job_types", [])
                                if skills:
                                    for skill in skills:
                                        st.write(f"• {skill}")
                                else:
                                    st.write("No skills listed")
                            
                            with tab3:
                                st.write(f"**👤 Name:** {str(seeker.get('emergency_name', 'Not provided'))}")
                                st.write(f"**📞 Contact:** {str(seeker.get('emergency_contact', 'Not provided'))}")

                        st.markdown("")  # Add some spacing