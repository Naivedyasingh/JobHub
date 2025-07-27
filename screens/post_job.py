# pages/post_job.py

import streamlit as st
from utils.data_helpers import read_json, write_json
from datetime import datetime
from utils.jobs import add_job_posting
from utils.applications import get_job_applications
DATA_FOLDER = "data"
JOBS_FILE = f"{DATA_FOLDER}/demo_jobs.json"  # or your persisted jobs file


def load_jobs():
    """Read and return list of posted jobs."""
    return read_json(JOBS_FILE)


def save_job_application(application):
    """Save a new job application"""
    applications = get_job_applications()
    application['id'] = len(applications) + 1
    application['applied_date'] = datetime.now().isoformat()
    application['status'] = 'pending'
    applications.append(application)
    write_json("data/applications.json", applications)
    return True


def post_job_page():
    """Enhanced job posting page"""
    user = st.session_state.current_user

    st.title("📝 Post New Job")
    st.subheader("Find the perfect candidate for your job opening")

    with st.form("job_posting_form"):
        col1, col2 = st.columns(2)

        with col1:
            job_title = st.text_input("Job Title *", placeholder="e.g., House Maid, Cook, Driver")
            location = st.text_input("Job Location *", placeholder="City, Area")
            salary = st.number_input("Monthly Salary (₹) *", min_value=5000, max_value=100000, value=15000, step=1000)
            job_type = st.selectbox(
                "Job Category *",
                ["Maid", "Cook", "Driver", "Cleaner", "Babysitter", "Gardener", "Security Guard", "Electrician", "Plumber", "Other"]
            )

        with col2:
            experience = st.selectbox("Experience Required", ["Any", "Fresher", "1-2 years", "2-5 years", "5+ years"])
            working_hours = st.selectbox("Working Hours", ["Full Time", "Part Time", "Weekends Only", "Flexible"])
            urgency = st.selectbox("Urgency Level", ["Normal", "Urgent", "Very Urgent"])
            contract_type = st.selectbox("Contract Type", ["Permanent", "Temporary", "Contract", "Part-time"])

        description = st.text_area("Job Description *", placeholder="Describe the job responsibilities, working conditions, and what you're looking for...")
        requirements = st.text_area("Requirements & Qualifications", placeholder="Specific skills, qualifications, or experience needed...")
        benefits = st.text_area("Benefits & Perks", placeholder="Additional benefits like meals, accommodation, bonus, etc.")

        submitted = st.form_submit_button("📤 Post Job", type="primary")

    if submitted:
        if not all([job_title.strip(), location.strip(), description.strip()]):
            st.error("Please fill all required fields marked with *")
        else:
            job_data = {
                'title': job_title.strip(),
                'location': location.strip(),
                'salary': salary,
                'job_types': [job_type],  # <-- CORRECTED: always as a list, key is 'job_types'
                'experience': experience,
                'working_hours': working_hours,
                'urgency': urgency,
                'contract_type': contract_type,
                'description': description.strip(),
                'requirements': requirements.strip(),
                'benefits': benefits.strip()
            }

            if add_job_posting(user['id'], job_data):
                st.success("🎉 Job posted successfully!")
                st.balloons()
                st.info("Your job is now visible to all job seekers on the platform.")
            else:
                st.error("Failed to post job. Please try again.")

    st.markdown("---")
    if st.button("🏠 Back to Dashboard"):
        st.session_state.page = "hire_dashboard"
        st.rerun()
