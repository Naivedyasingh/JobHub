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

    st.markdown(f"""
        <div style="text-align:center;">
          <span style="font-size:2.2rem;"><b>🔍 Job Seeker Dashboard</b></span><br>
          <span style="font-size:1.2rem; color:#222;">Welcome back, <b>{user['name']}</b>! 👋</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    if completion < 100:
        st.error(f"⚠️ **Profile Incomplete ({completion}%)** - Complete your profile to apply for jobs and receive offers!")
        if st.button("📝 Complete Profile Now", type="primary", key="dashboard_complete_profile"):
            st.session_state.page = "profile"
            st.rerun()
        st.markdown("---")
        return

    def is_active(o):
        try:
            expires = datetime.fromisoformat(o.get("expires_at", datetime.now().isoformat()))
        except Exception:
            expires = datetime.now()
        return datetime.now() <= expires

    active_offers = [o for o in get_job_offers() if o.get('job_seeker_id') == user['id'] and o.get('status') == 'pending' and is_active(o)]
    
    if active_offers:
        st.markdown("### 🎯 **Job Offers for You!**")
        for offer in active_offers:
            expires = datetime.fromisoformat(offer.get("expires_at", datetime.now().isoformat()))
            hours_left = max(0, int((expires - datetime.now()).total_seconds() // 3600))
            st.markdown(f"""
                <div style="border:3px solid #ff6b35; border-radius:15px; padding:20px; margin:10px 0;
                            background:linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);">
                  <b>💼 {offer.get('job_title')}</b><br>
                  <b>🏢 Company:</b> {offer.get('employer_name')}<br>
                  <b>💰 Salary:</b> ₹{offer.get('salary_offered')}<br>
                  <b>📍 Location:</b> {offer.get('location', 'Not specified')}<br>
                  <b>💬 Message:</b> {offer.get('personal_message', 'No message')}<br>
                  <b>⏰ Expires in:</b> {hours_left} hours
                </div>""", unsafe_allow_html=True)
            
            col_accept, col_reject = st.columns(2)
            with col_accept:
                if st.button("✅ Accept", key=f"accept_offer_{offer['id']}", type="primary"):
                    update_offer_status(offer['id'], 'accepted', 'Job offer accepted by job seeker')
                    st.success("🎉 Job offer accepted! The employer will be notified.")
                    st.rerun()
            with col_reject:
                if st.button("❌ Decline", key=f"decline_offer_{offer['id']}"):
                    update_offer_status(offer['id'], 'rejected', 'Job offer declined by job seeker')
                    st.info("Job offer declined.")
                    st.rerun()
        st.markdown("---")

    users = read_json("data/users.json")
    employers = [u for u in users if u.get('role') == 'hire']
    
    all_jobs = []
    for job in get_demo_jobs():
        job['employer_info'] = {'id':'demo','name':'Demo Employer','company':job['company'],'phone':job['contact'],'email':'demo@jobconnect.com'}
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

    default_categories = ["Cook","Maid","Plumber","Electrician","Babysitter","Gardener","Driver","Cleaner","Security Guard"]
    job_categories_set = set(x.lower() for x in default_categories)
    for job in all_jobs:
        job_types = job.get('job_types', [])
        if isinstance(job_types, str): job_types = [job_types]
        job_categories_set.update(jt.strip().lower() for jt in job_types if jt)
    display_job_categories = sorted(j.title() for j in job_categories_set)
    display_to_lower = {j.title():j.lower() for j in job_categories_set}

    locations = sorted(set(job.get('location', 'Not specified') for job in all_jobs))
    companies = sorted(set(job['employer_info']['company'] for job in all_jobs))
    salaries = [job.get('salary', 0) or 0 for job in all_jobs if 'salary' in job]
    min_sal, max_sal = (min(salaries) if salaries else 0, max(salaries) if salaries else 0)

    c1, c2, c3, c4 = st.columns([2,2,2,4])
    with c1:
        location_filter = st.selectbox("By Location:", ["All"] + locations, index=0)
    with c2:
        job_category_filter = st.selectbox("Job Category:", ["All"] + display_job_categories, index=0)
    with c3:
        company_filter = st.selectbox("By Company:", ["All"] + companies, index=0)
    with c4:
        if min_sal < max_sal:
            salary_range = st.slider("Salary Range (₹):", int(min_sal), int(max_sal), (int(min_sal), int(max_sal)), step=1000)
        else:
            salary_range = (int(min_sal), int(max_sal))

    selected_cat_lower = display_to_lower.get(job_category_filter, "all")

    filtered_jobs = [job for job in all_jobs
                    if (location_filter=="All" or job.get('location', 'Not specified') == location_filter) and
                       (selected_cat_lower=="all" or selected_cat_lower in [jt.lower() for jt in (job.get('job_types') if isinstance(job.get('job_types'), list) else [job.get('job_types')]) if jt]) and
                       (company_filter=="All" or job['employer_info']['company'] == company_filter) and
                       (salary_range[0] <= (job.get('salary', 0) or 0) <= salary_range[1])
                    ]

    st.info(f"**Found {len(filtered_jobs)} job(s) matching your filters**")

    applications = get_job_applications()
    applied_set = {(app.get('job_id'), str(app.get('employer_id'))) for app in applications if app.get('applicant_id') == user['id']}

    applied_jobs, not_applied_jobs = [], []
    for job in filtered_jobs:
        key = (job.get('id'), str(job['employer_info']['id']))
        (applied_jobs if key in applied_set else not_applied_jobs).append(job)

    tab_avail, tab_applied = st.tabs([f"🟢 Available Jobs ({len(not_applied_jobs)})", f"✅ Applied Jobs ({len(applied_jobs)})"])

    with tab_avail:
        if not_applied_jobs:
            cols = st.columns(2)
            for idx, job in enumerate(not_applied_jobs):
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div style="border:2px solid #ffff9d; border-radius:15px; background:#f9f9ec; padding:18px;
                        margin-bottom:1.5rem; box-shadow:0 2px 6px #aad7b4;">
                            <h4 style="margin-bottom:.5rem; font-weight:700;">💼 {job.get('title')}</h4>
                            <b>🏢 {job['employer_info']['company']}</b> | <b>📍 {job.get('location', 'Not specified')}</b><br>
                            <b>💰 Salary:</b> ₹{job.get('salary', 'Not specified')}
                            <b>Type:</b> {job.get('working_hours', job.get('type', 'Not specified'))}<br>
                            <b>📈 Experience:</b> {job.get('experience', 'Any')}<br>
                            <b>🗓️ Posted:</b> {job.get('posted_date', '')[:10] or 'N/A'}<br>
                            <b>📞 Contact:</b> {job['employer_info']['phone']} | <b>✉️</b> {job['employer_info']['email']}<br>
                            <span style='font-size:0.97em; color:#444;'>
                                {(job.get('description','')[:120]+'...') if len(job.get('description','')) > 120 else job.get('description','')}
                            </span>
                        </div>""", unsafe_allow_html=True)

                    if st.button("🟢 Apply Now", key=f"apply_{job['employer_info']['id']}_{job.get('id')}", use_container_width=True, type="primary"):
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
                            'expected_salary': user.get('expected_salary', 'Not specified'),
                        }
                        if save_job_application(application):
                            st.success("✅ Application sent successfully!")
                            time.sleep(1)
                            st.rerun()
        else:
            st.info("🎉 No new jobs available to apply for!")

    with tab_applied:
        if applied_jobs:
            cols = st.columns(2)
            for idx, job in enumerate(applied_jobs):
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div style="border:2px solid #6c757d; border-radius:15px; background:#f0f0f0; padding:18px;
                        margin-bottom:1.5rem; box-shadow:0 2px 6px #ccc;">
                            <h4 style="margin-bottom:.5rem; font-weight:700; color:#555;">💼 {job.get('title')}</h4>
                            <b>🏢 {job['employer_info']['company']}</b> | <b>📍 {job.get('location', 'Not specified')}</b><br>
                            <b>💰 Salary:</b> ₹{job.get('salary', 'Not specified')}
                            <b>Type:</b> {job.get('working_hours', job.get('type', 'Not specified'))}<br>
                            <b>📈 Experience:</b> {job.get('experience', 'Any')}<br>
                            <b>🗓️ Posted:</b> {job.get('posted_date', '')[:10] or 'N/A'}<br>
                            <b>📞 Contact:</b> {job['employer_info']['phone']} | <b>✉️</b> {job['employer_info']['email']}<br>
                            <span style='font-size:0.97em; color:#444;'>
                                {(job.get('description','')[:120] + '...') if len(job.get('description','')) > 120 else job.get('description','')}
                            </span><br><br>
                            <button disabled style="padding:6px 12px; background:#6c757d; color:#fff; border:none; border-radius:4px;">
                                ✅ Already Applied
                            </button>
                        </div>""", unsafe_allow_html=True)
        else:
            st.info("🙌 You have not applied for any jobs yet.")
