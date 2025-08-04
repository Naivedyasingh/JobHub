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
    """Job seeker cards with clean native Streamlit styling and background colors"""
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
                    
                    # Clean data like applications page
                    name = str(seeker['name'])
                    phone = str(seeker.get('phone', 'N/A'))
                    experience = str(seeker.get('experience', 'Not specified'))
                    salary = str(seeker.get('expected_salary', 'Not specified'))
                    city = str(seeker.get('city', 'Not specified'))
                    
                    if status == 'available':
                        status_color = "🟢"
                        status_text = "Available"
                        icon = "🟢"
                        badge_bg = "#d4edda"
                        badge_color = "#155724"
                        card_bg = "#4CAF50"
                    elif status == 'busy':
                        status_color = "🟡"
                        status_text = "Busy"
                        icon = "🟡"
                        badge_bg = "#fff3cd"
                        badge_color = "#856404"
                        card_bg = "#FF9800"
                    else:
                        status_color = "🔴"
                        status_text = "Not Available"
                        icon = "🔴"
                        badge_bg = "#f8d7da"
                        badge_color = "#721c24"
                        card_bg = "#f44336"

                    # Create HTML card with ALL content inside (larger size)
                    html_card = f"""
                    <div style="
                        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                        border-radius: 18px; 
                        padding: 30px; 
                        margin: 20px 0; 
                        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); 
                        transition: transform 0.3s ease, box-shadow 0.3s ease; 
                        border-left: 6px solid {card_bg}; 
                        position: relative; 
                        overflow: hidden;
                        min-height: 180px;
                    ">
                      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                        <h3 style="margin:0; font-size:1.3rem; font-weight:600;">👤 {name}</h3>
                        <span style="
                            background:{badge_bg};
                            color:{badge_color};
                            padding:6px 12px;
                            border-radius:12px;
                            font-weight:bold;
                            font-size:0.9rem;
                        ">
                          {icon} {status_text}
                        </span>
                      </div>
                      <div style="font-size:0.95rem; color:#495057; line-height:1.8;">
                        <div style="display:grid; grid-template-columns:1fr auto 1fr; gap:20px;">
                            <div>
                                <strong style="color:#666; font-size:1rem;">💼 Experience</strong><br>
                                <div style="margin-top:8px;">⏱️ {experience}</div>
                                <div style="margin-top:5px;">💰 ₹{salary}</div>
                            </div>
                            <div style="border-left: 3px solid #e0e0e0; height: 80px;"></div>
                            <div>
                                <strong style="color:#666; font-size:1rem;">📞 Contact</strong><br>
                                <div style="margin-top:8px;">📱 {phone}</div>
                                <div style="margin-top:5px;">🏙️ {city}</div>
                            </div>
                        </div>
                      </div>
                    </div>
                    """

                    st.markdown(html_card, unsafe_allow_html=True)

                    # Action buttons (outside HTML card, like applications page)
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

                    if st.session_state.get(details_key, False):
                        with st.expander("📋 Full Details", expanded=True):
                    
                            tab1, tab2, tab3 = st.tabs(["📧 Contact", "💼 Professional", "🚨 Emergency"])
                    
                            with tab1:
                                st.write(f"**📧 Email:** {seeker.get('email','N/A')}")
                                st.write(f"**📱 Phone:** {seeker.get('phone','N/A')}")
                                st.write(f"**🏠 Address:** {seeker.get('address','Not provided')}")
                                st.write(f"**🏙️ City:** {seeker.get('city','Not specified')}")
                    
                            with tab2:
                                st.write(f"**🎓 Education:** {seeker.get('education','Not specified')}")
                                st.write(f"**⏱️ Experience:** {seeker.get('experience','Not specified')}")
                                st.write(f"**💰 Expected Salary:** {seeker.get('expected_salary','Not specified')}")
                                st.write(f"**📅 Notice Period:** {seeker.get('notice_period','Not specified')}")
                                st.write("**🛠️ All Skills:**")
                                skills = seeker.get("job_types", [])
                                if skills:
                                    for skill in skills:
                                        st.write(f"• {skill}")
                                else:
                                    st.write("No skills listed")
                    
                            with tab3:
                                st.write(f"**👤 Name:** {seeker.get('emergency_name','Not provided')}")
                                st.write(f"**📞 Contact:** {seeker.get('emergency_contact','Not provided')}")
                    
                            # close the white-background container
                            st.markdown("</div>", unsafe_allow_html=True)





                    