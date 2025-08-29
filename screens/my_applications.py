import streamlit as st
from utils.applications import get_job_applications
from datetime import datetime
from utils.offers import get_job_offers, update_offer_status

def my_applications_page():
    user = st.session_state.current_user

    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2c3e50; font-size: 2.2rem; margin-bottom: 10px;">📋 My Applications & Offers</h1>
    </div>
    """, unsafe_allow_html=True)

    applications = get_job_applications()
    offers = get_job_offers()

    my_apps = [a for a in applications if a.get('applicant_id') == user['id']]
    my_offs = [o for o in offers if o.get('job_seeker_id') == user['id']]

    st.markdown("""
    <style>
    .card {
        background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
        border-radius: 15px; padding: 20px; margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 6px solid; position: relative;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .job-title, .offer-title {
        font-weight: 700; font-size: 1.3rem; color: #2c3e50; margin-bottom: 10px;
    }
    .job-company, .offer-company {
        font-size: 1.1rem; color: #34495e; margin-bottom: 8px;
    }
    .job-date {
        color: #7f8c8d; font-size: 0.95rem; margin-bottom: 10px;
    }
    .status-badge {
        display: inline-block; padding: 6px 12px; border-radius: 20px;
        font-weight: 600; margin-bottom: 10px; user-select: none;
    }
    .status-pending { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
    .status-accepted { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .status-rejected { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-expired { background: #e2e3e5; color: #6c757d; border: 1px solid #d6d8db; }
    .job-response {
        background: #e8f4fd; border-left: 4px solid #3498db; padding: 10px;
        border-radius: 5px; margin-top: 10px; font-style: italic; color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

    tab_offers, tab_apps = st.tabs([f"💼 Job Offers ({len(my_offs)})", f"📤 My Applications ({len(my_apps)})"])

    def render_status(status, expired=False):
        if expired:
            return "#6c757d", "⏰ Expired", "status-expired"
        map_status = {
            "pending": ("#ffc107", "🟡 Pending", "status-pending"),
            "accepted": ("#28a745", "✅ Accepted", "status-accepted"),
            "rejected": ("#dc3545", "❌ Declined", "status-rejected")
        }
        return map_status.get(status, ("#ffc107", "🟡 Pending", "status-pending"))

    def render_offer_card(offer, col):
        expires = datetime.fromisoformat(offer.get("expires_at", datetime.now().isoformat()))
        is_expired = datetime.now() > expires
        border_color, status_text, status_class = render_status(offer.get("status", "pending"), is_expired)

        with col:
            st.markdown(f"""
            <div class="card" style="border-left-color: {border_color};">
                <div class="offer-title">💼 {offer.get('job_title')}</div>
                <div class="offer-company">🏢 {offer.get('employer_name')}</div>
                <div>💰 <strong>Salary:</strong> ₹{offer.get('salary_offered')}</div>
                <div>📍 <strong>Location:</strong> {offer.get('location')}</div>
                <div>📅 <strong>Start Date:</strong> {offer.get('start_date')}</div><br>
                <div class="status-badge {status_class}">{status_text}</div>
            """, unsafe_allow_html=True)

            if offer.get("status") == "pending" and not is_expired:
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Accept", key=f"accept_{offer['id']}", type="primary", use_container_width=True):
                        update_offer_status(offer["id"], "accepted", "Offer accepted")
                        st.success("Offer accepted!")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Decline", key=f"decline_{offer['id']}", use_container_width=True):
                        update_offer_status(offer["id"], "rejected", "Offer declined")
                        st.info("Offer declined.")
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


    def render_application_card(app, col):
        border_color, status_class, status_text = {
            'pending': ('#ffc107', 'status-pending', '🟡 Under Review'),
            'accepted': ('#28a745', 'status-accepted', '✅ Accepted'),
            'rejected': ('#dc3545', 'status-rejected', '❌ Rejected')
        }.get(app.get('status'), ('#ffc107', 'status-pending', '🟡 Under Review'))

        with col:
            resp = app.get("response_message", "")
            st.markdown(f"""
            <div class="card" style="border-left-color: {border_color};">
                <div class="job-title">💼 {app.get('job_title', 'N/A')}</div>
                <div class="job-company">🏢 {app.get('employer_name', 'N/A')}</div>
                <div class="job-date">📅 Applied: {app.get('applied_date', '')[:10]}</div>
                <div class="status-badge {status_class}">{status_text}</div>
                {f'<div class="job-response">💬 <strong>Response:</strong> {resp}</div>' if resp else ''}
            </div>
            """, unsafe_allow_html=True)

    with tab_offers:
        if my_offs:
            for i in range(0, len(my_offs), 2):
                cols = st.columns(2, gap="large")
                render_offer_card(my_offs[i], cols[0])
                if i + 1 < len(my_offs):
                    render_offer_card(my_offs[i+1], cols[1])
                else:
                    with cols[1]:
                        st.markdown("<div style='height:200px'></div>", unsafe_allow_html=True)
        else:
            st.info("No job offers received yet.")

    with tab_apps:
        if my_apps:
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Accepted", "Rejected"])
            with col2:
                sort_by = st.selectbox("Sort By", ["Date Applied", "Company", "Job Title"])

            filtered = my_apps if status_filter == "All" else [a for a in my_apps if a.get("status", "").title() == status_filter]
            sort_keys = {
                "Date Applied": lambda a: a.get("applied_date", ""),
                "Company": lambda a: a.get("employer_name", ""),
                "Job Title": lambda a: a.get("job_title", ""),
            }
            filtered.sort(key=sort_keys.get(sort_by, sort_keys["Date Applied"]), reverse=(sort_by == "Date Applied"))
            for i in range(0, len(filtered), 2):
                cols = st.columns(2, gap="large")
                render_application_card(filtered[i], cols[0])
                if i + 1 < len(filtered):
                    render_application_card(filtered[i+1], cols[1])
                else:
                    with cols[1]:
                        st.markdown('<div style="height:200px;"></div>', unsafe_allow_html=True)
        else:
            st.info("You haven't applied for any jobs yet.")
