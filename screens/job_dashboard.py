import time
import streamlit as st
from utils.data_helpers import read_json
from utils.applications import get_job_applications, save_job_application
from utils.offers import get_job_offers, update_offer_status
from datetime import datetime
from utils.auth import calculate_profile_completion
from utils.jobs import get_demo_jobs

def job_dashboard():
    user = st.session_state.current_user
    completion = calculate_profile_completion(user)
    st.markdown(
        f"""
        <div style="text-align:center;">
          <span style="font-size:2.2rem;"><b>🔍 Job Seeker Dashboard</b></span><br>
          <span style="font-size:1.2rem; color:#222;">Welcome back, <b>{user['name']}</b>! 👋</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Profile completion
    if completion < 100:
        st.error(f"⚠️ **Profile Incomplete ({completion}%)** - Complete your profile to apply for jobs and receive offers!")
        if st.button("📝 Complete Profile Now", type="primary", key="dashboard_complete_profile"):
            st.session_state.page = "profile"
            st.rerun()
        st.markdown("---")
        return

    # Job Offers
    offers = get_job_offers()
    my_offers = [
        offer for offer in offers
        if offer.get('job_seeker_id') == user['id'] and offer.get('status') == 'pending'
    ]
    active_offers = []
    for offer in my_offers:
        try:
            expires = datetime.fromisoformat(offer.get('expires_at', datetime.now().isoformat()))
        except Exception:
            expires = datetime.now()
        if datetime.now() <= expires:
            active_offers.append(offer)
    if active_offers:
        st.markdown("### 🎯 **Job Offers for You!**")
        for offer in active_offers:
            expires = datetime.fromisoformat(offer.get('expires_at', datetime.now().isoformat()))
            hours_left = max(0, int((expires-datetime.now()).total_seconds() // 3600))
            st.markdown(
                f"""
                <div style="border: 3px solid #ff6b35; border-radius: 15px; padding: 20px; margin: 10px 0;
                            background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);">
                    <b>💼 {offer.get('job_title')}</b><br>
                    <b>🏢 Company:</b> {offer.get('employer_name')}<br>
                    <b>💰 Salary:</b> ₹{offer.get('salary_offered')}<br>
                    <b>📍 Location:</b> {offer.get('location', 'Not specified')}<br>
                    <b>💬 Message:</b> {offer.get('personal_message', 'No message')}<br>
                    <b>⏰ Expires in:</b> {hours_left} hours
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_accept, col_reject = st.columns(2)
            with col_accept:
                if st.button("✅ Accept", key=f"accept_offer_{offer['id']}", type="primary"):
                    update_offer_status(offer['id'], 'accepted', 'Job offer accepted by job seeker')
                    st.success("🎉 Job offer accepted! The employer will be notified.")
                    st.balloons()
                    st.rerun()
            with col_reject:
                if st.button("❌ Decline", key=f"decline_offer_{offer['id']}"):
                    update_offer_status(offer['id'], 'rejected', 'Job offer declined by job seeker')
                    st.info("Job offer declined.")
                    st.rerun()
        st.markdown("---")

    # Collect job listings
    st.subheader("💼 Available Job Opportunities")
    users = read_json("data/users.json")
    employers = [u for u in users if u.get('role') == 'hire']
    all_jobs = []
    demo_jobs = get_demo_jobs()
    for job in demo_jobs:
        job['employer_info'] = {
            'id': 'demo',
            'name': 'Demo Employer',
            'company': job['company'],
            'phone': job['contact'],
            'email': 'demo@jobconnect.com'
        }
        all_jobs.append(job)
    for employer in employers:
        for job in employer.get('job_postings', []):
            if job.get('status') == 'active':
                job['employer_info'] = {
                    'id': employer['id'],
                    'name': employer['name'],
                    'company': employer.get('company_name', 'Company'),
                    'phone': employer['phone'],
                    'email': employer['email']
                }
                all_jobs.append(job)

    if not all_jobs:
        st.info("📭 No job postings available at the moment. Please check back later!")
        return

    # Job Categories (always includes standard types)
    default_job_categories = [
        "Cook", "Maid", "Plumber", "Electrician", "Babysitter",
        "Gardener", "Driver", "Cleaner", "Security Guard"
    ]
    job_categories_set = set(s.lower() for s in default_job_categories)
    for job in all_jobs:
        job_types = job.get('job_types', [])
        if isinstance(job_types, str):
            job_types = [job_types]
        job_categories_set.update(jt.strip().lower() for jt in job_types if jt)
    display_job_categories = sorted({jt.title() for jt in job_categories_set})
    display_to_lower = {jt.title(): jt.lower() for jt in job_categories_set}

    # Other filters
    locations = sorted({job.get('location', 'Not specified') for job in all_jobs})
    companies = sorted({job['employer_info']['company'] for job in all_jobs})
    salaries = [job.get('salary', 0) or 0 for job in all_jobs if 'salary' in job]
    min_salary = min(salaries) if salaries else 0
    max_salary = max(salaries) if salaries else 0

    filter_cols = st.columns([2, 2, 2, 4])
    with filter_cols[0]:
        location_filter = st.selectbox("By Location:", ["All"] + locations, index=0)
    with filter_cols[1]:
        job_category_filter = st.selectbox("Job Category:", ["All"] + display_job_categories, index=0)
    with filter_cols[2]:
        company_filter = st.selectbox("By Company:", ["All"] + companies, index=0)
    with filter_cols[3]:
        if min_salary < max_salary:
            salary_range = st.slider(
                "Salary Range (₹):",
                int(min_salary), int(max_salary), (int(min_salary), int(max_salary)), step=1000)
        else:
            salary_range = (int(min_salary), int(max_salary))

    # Apply filters
    selected_category_lower = display_to_lower.get(job_category_filter, "all").lower()
    filtered_jobs = []
    for job in all_jobs:
        loc_match = location_filter == "All" or job.get('location', 'Not specified') == location_filter

        job_types = job.get('job_types', [])
        if isinstance(job_types, str):
            job_types = [job_types]
        job_types = [jt.lower() for jt in job_types if jt]
        category_match = (selected_category_lower == "all") or (selected_category_lower in job_types)

        comp_match = company_filter == "All" or job['employer_info']['company'] == company_filter

        salary = job.get('salary', 0) or 0
        salary_match = salary_range[0] <= salary <= salary_range[1]

        if loc_match and category_match and comp_match and salary_match:
            filtered_jobs.append(job)
    st.info(f"**Found {len(filtered_jobs)} job(s) matching your filters**")

    # Job cards in grid
    if filtered_jobs:
        grid_cols = st.columns(2)
        for idx, job in enumerate(filtered_jobs):
            with grid_cols[idx % 2]:
                st.markdown(
                    f"""
                    <div style="border:2px solid #f4a261;border-radius:15px;background:#fffdf4;padding:18px;
                    margin-bottom:1.5rem;box-shadow:0 2px 6px #eedc8210;">
                        <h4 style="margin-bottom:.5rem;font-weight:700;">
                            💼 {job.get('title')}
                        </h4>
                        <b>🏢 {job['employer_info']['company']}</b>
                        | <b>📍 {job.get('location', 'Not specified')}</b><br>
                        <b>💰 Salary:</b> ₹{job.get('salary', 'Not specified')}
                        <b>Type:</b> {job.get('working_hours', job.get('type', 'Not specified'))}<br>
                        <b>📈 Experience:</b> {job.get('experience', 'Any')}<br>
                        <b>🗓️ Posted:</b> {job.get('posted_date', '')[:10] or 'N/A'}<br>
                        <b>📞 Contact:</b> {job['employer_info']['phone']}
                        | <b>✉️</b> {job['employer_info']['email']}<br>
                        <span style='font-size:0.97em; color:#444;'>
                            {(job.get('description','')[:120]+'...') if len(job.get('description','')) > 120 else job.get('description','')}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                applications = get_job_applications()
                already_applied = any(
                    app.get('job_id') == job.get('id') and
                    str(app.get('employer_id')) == str(job['employer_info']['id']) and
                    app.get('applicant_id') == user['id']
                    for app in applications
                )
                col_btn = st.columns([1, 2, 1])[1]  # Center button
                with col_btn:
                    if already_applied:
                        st.button("✅ Already Applied",
                                  key=f"applied_{job['employer_info']['id']}_{job.get('id')}",
                                  use_container_width=True, type="secondary", disabled=True)
                    else:
                        if st.button("🟢 Apply Now",
                                     key=f"apply_job_{job['employer_info']['id']}_{job.get('id')}",
                                     use_container_width=True, type="primary"):
                            application = {
                                'job_id': job.get('id'),
                                'job_title': job.get('title'),
                                'employer_id': job['employer_info']['id'],
                                'employer_name': job['employer_info']['company'],
                                'applicant_id': user['id'],
                                'applicant_name': user['name'],
                                'applicant_phone': user['phone'],
                                'applicant_email': user['email'],
                                'applicant_skills': ', '.join(user.get('job_types', [])),
                                'applicant_experience': user.get('experience', 'Not specified'),
                                'expected_salary': user.get('expected_salary', 'Not specified')
                            }
                            if save_job_application(application):
                                st.success("✅ Application sent successfully!")
                                st.balloons()
                                time.sleep(1)
                                st.rerun()
    else:
        st.warning("No job postings match your chosen filters.")

# Use job_dashboard() as your entrypoint in your Streamlit app routing.
