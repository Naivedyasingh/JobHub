import streamlit as st
from datetime import datetime
import time
from utils.jobs import add_job_posting
from utils.data_helpers import read_json, write_json
from utils.applications import get_job_applications

DATA_FOLDER = "data"
JOBS_FILE = f"{DATA_FOLDER}/demo_jobs.json"

def post_job_page():
    user = st.session_state.current_user

    if "page_flag" not in st.session_state or st.session_state.page_flag != "post_job":
        st.session_state.job_posting_disabled = False
        st.session_state.page_flag = "post_job"

    st.title("📝 Post New Job")
    st.subheader("Find the perfect candidate for your job opening")

    with st.form("job_posting_form"):
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title *", placeholder="e.g., House Maid, Cook, Driver")
            location = st.text_input("Job Location *", placeholder="City, Area")
            salary = st.number_input("Monthly Salary (₹) *", 5000, 100000, 15000, 1000)
            job_type = st.selectbox(
                "Job Category *",
                ["Maid", "Cook", "Driver", "Cleaner", "Babysitter",
                 "Gardener", "Security Guard", "Electrician", "Plumber", "Other"]
            )
        with col2:
            experience    = st.selectbox("Experience Required", ["Any", "Fresher", "1-2 years", "2-5 years", "5+ years"])
            working_hours = st.selectbox("Working Hours", ["Full Time", "Part Time", "Weekends Only", "Flexible"])
            urgency       = st.selectbox("Urgency Level", ["Normal", "Urgent", "Very Urgent"])
            contract_type = st.selectbox("Contract Type", ["Permanent", "Temporary", "Contract", "Part-time"])

        description  = st.text_area("Job Description *", placeholder="Describe the job responsibilities, working conditions...")
        requirements = st.text_area("Requirements & Qualifications", placeholder="Specific skills, qualifications, or experience needed...")
        benefits     = st.text_area("Benefits & Perks", placeholder="Additional benefits like meals, accommodation, bonus, etc.")

        btn_txt   = "⌛ Posting..." if st.session_state.get("job_posting_disabled", False) else "📤 Post Job"
        submitted = st.form_submit_button(btn_txt, type="primary", disabled=st.session_state.job_posting_disabled)

    if submitted:
        if not (job_title.strip() and location.strip() and description.strip()):
            st.error("Please fill all required fields marked with *")
        else:
            st.session_state.job_posting_disabled = True
            job_data = {
                "title": job_title.strip(),
                "location": location.strip(),
                "salary": salary,
                "job_types": [job_type],
                "experience": experience,
                "working_hours": working_hours,
                "urgency": urgency,
                "contract_type": contract_type,
                "description": description.strip(),
                "requirements": requirements.strip(),
                "benefits": benefits.strip()
            }
            if add_job_posting(user["id"], job_data):
                st.success("🎉 Job posted successfully!")
                st.session_state.page = "hire_dashboard"
                st.session_state.page_flag = None
                st.session_state.job_posting_disabled = False
                time.sleep(3)
                st.rerun()
            else:
                st.error("Failed to post job. Please try again.")
                st.session_state.job_posting_disabled = False

    st.markdown("---")
    if st.button("🏠 Back to Dashboard"):
        st.session_state.page = "hire_dashboard"
        st.session_state.page_flag = None
        st.session_state.job_posting_disabled = False
        st.rerun()
