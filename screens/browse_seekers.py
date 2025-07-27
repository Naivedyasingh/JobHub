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
    """Job seeker cards with container styling and 24h-offer logic"""
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

    for seeker in filtered:
        status = seeker.get('availability_status', 'available')
        if status == 'available':
            bg, border = "#e8f5e8", "#28a745"
            icon, text = "🟢", "Available"
        elif status == 'busy':
            bg, border = "#fff3cd", "#ffc107"
            icon, text = "🟡", "Busy"
        else:
            bg, border = "#f8d7da", "#dc3545"
            icon, text = "🔴", "Not Available"

        st.markdown(
            f"<hr style='border:none; height:3px; background:{border}; margin:20px 0;'>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div style='background:{bg}; border:2px solid {border}; border-radius:8px; padding:16px;'>", unsafe_allow_html=True)

        # Header
        hcol, mcol = st.columns([3,1])
        with hcol:
            st.markdown(f"<h4 style='margin:0;'>👤 {seeker['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin:4px 0;'>{icon} {text}</p>", unsafe_allow_html=True)
        with mcol:
            pct = calculate_profile_completion(seeker)
            st.metric("", f"{pct}%", label_visibility="collapsed")

        # Info
        icol, scol, acol = st.columns(3)
        with icol:
            st.markdown("**📞 Contact**")
            st.write(seeker["phone"])
            st.write(seeker.get("city", "-"))
        with scol:
            st.markdown("**💼 Skills**")
            skills = ", ".join(seeker.get("job_types", [])[:2])
            if len(seeker.get("job_types", [])) > 2:
                skills += "…"
            st.write(skills)
            st.write(seeker.get("experience", "-"))
        with acol:
            st.markdown("**⚡ Actions**")
            # Check for recent offer
            recent = None
            for o in all_offers:
                if o.get("employer_id") == user["id"] and o.get("job_seeker_id") == seeker["id"]:
                    odt = dt.fromisoformat(o["offered_date"])
                    delta = datetime.datetime.now() - odt
                    if delta.total_seconds() < 24*3600:
                        recent = delta
                        break
            if status != 'available':
                st.button("❌ Not Available", disabled=True, use_container_width=True)
            else:
                if recent:
                    hrs = int(recent.total_seconds() // 3600)
                    st.button(f"⌛ Offered ({hrs}h ago)", disabled=True, use_container_width=True)
                else:
                    if st.button("💼 Offer Job", type="primary", use_container_width=True, key=f"offer_{seeker['id']}"):
                        st.session_state.selected_candidate = seeker
                        st.session_state.page = "offer_job"
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Expander for more details
        with st.expander(f"{icon} More Details – {seeker['name']}"):
            d1, d2 = st.columns(2)
            with d1:
                st.markdown("**📧 Email**")
                st.write(seeker.get("email","-"))
                st.markdown("**🏠 Address**")
                addr = seeker.get("address","-")
                st.write(addr if len(addr)<30 else addr[:30]+"…")
            with d2:
                st.markdown("**🚨 Emergency Contact**")
                ec = seeker.get("emergency_name","-")
                emc = seeker.get("emergency_contact","-")
                st.write(f"{ec}: {emc}")

