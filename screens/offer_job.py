# pages/offer_job.py

import streamlit as st
from utils.data_helpers import read_json, write_json
from utils.offers import save_job_offer
import time

def offer_job_page():
    """Enhanced page for employers to offer job to specific candidate"""
    user = st.session_state.current_user
    candidate = st.session_state.get('selected_candidate')
    
    if not candidate:
        st.error("No candidate selected")
        return
    
    st.title(f"💼 Offer Job to {candidate['name']}")
    
    # Show candidate summary
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 10px; padding: 15px; margin: 10px 0;">
        <h4>📋 Candidate Summary</h4>
        <p><strong>📱 Phone:</strong> {candidate['phone']} | <strong>✉️ Email:</strong> {candidate['email']}</p>
        <p><strong>🛠️ Skills:</strong> {', '.join(candidate.get('job_types', []))} | <strong>📈 Experience:</strong> {candidate.get('experience', 'Not specified')}</p>
        <p><strong>💰 Expected Salary:</strong> ₹{candidate.get('expected_salary', 'Not specified')} | <strong>📍 Location:</strong> {candidate.get('city', 'Not specified')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Job offer form
    with st.form("job_offer_form"):
        st.subheader("💼 Job Offer Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title *", placeholder="e.g., House Maid, Cook, Driver")
            location = st.text_input("Job Location *", value=user.get('city', ''), placeholder="City, Area")
            salary_offered = st.number_input("Salary Offer (₹) *", min_value=5000, max_value=100000, value=candidate.get('expected_salary', 15000), step=1000)
        
        with col2:
            job_type = st.selectbox("Job Category", ["Maid", "Cook", "Driver", "Cleaner", "Babysitter", "Gardener", "Security Guard", "Electrician", "Plumber", "Other"])
            working_hours = st.selectbox("Working Hours", ["Full Time", "Part Time", "Weekends Only", "Flexible"])
            start_date = st.date_input("Preferred Start Date")
        
        job_description = st.text_area("Job Description *", placeholder="Describe the job responsibilities and requirements...")
        personal_message = st.text_area("Personal Message to Candidate", placeholder="Why do you think they're perfect for this role?")
        
        submitted = st.form_submit_button("📤 Send Job Offer", type="primary")
    
    if submitted:
        if not all([job_title.strip(), location.strip(), job_description.strip()]):
            st.error("Please fill all required fields marked with *")
        else:
            # Create job offer
            offer_data = {
                'job_title': job_title.strip(),
                'job_description': job_description.strip(),
                'location': location.strip(),
                'salary_offered': salary_offered,
                'job_type': job_type,
                'working_hours': working_hours,
                'start_date': str(start_date),
                'personal_message': personal_message.strip(),
                'employer_id': user['id'],
                'employer_name': user.get('company_name', user['name']),
                'employer_phone': user['phone'],
                'employer_email': user['email'],
                'job_seeker_id': candidate['id'],
                'job_seeker_name': candidate['name'],
                'job_seeker_phone': candidate['phone'],
                'job_seeker_email': candidate['email']
            }
            
            if save_job_offer(offer_data):
                st.success(f"🎉 Job offer sent to {candidate['name']}!")
                st.session_state.page = "hire_dashboard"
                st.session_state.page_flag = None
                st.session_state.job_posting_disabled = False
                time.sleep(3)
                st.info("The candidate has 24 hours to respond to your offer.")
                st.info("You will be notified once they accept or decline the offer.")
            else:
                st.error("Failed to send job offer. Please try again.")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Browse Job Seekers", key="back_to_browse"):
            st.session_state.page = "browse_job_seekers"
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Dashboard", key="back_to_dashboard"):
            st.session_state.page = "hire_dashboard"
            st.rerun()
