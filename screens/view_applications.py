# pages/view_applications.py
import streamlit as st
from utils.applications import get_job_applications, update_application_status
from datetime import datetime
import html

def view_applications_page():
    st.markdown("<h2 style='text-align:center;color:#1f77b4;'>📋 Manage Applications</h2><br>", unsafe_allow_html=True)
    apps = [a for a in get_job_applications() if str(a.get('employer_id')) == str(st.session_state.current_user['id'])]
    if not apps:
        return st.info("No applications received yet.")
    tabs = st.tabs([f"🟡 Pending ({sum(a['status']=='pending' for a in apps)})",
                    f"🟢 Accepted ({sum(a['status']=='accepted' for a in apps)})",
                    f"🔴 Rejected ({sum(a['status']=='rejected' for a in apps)})"])
    for tab, status in zip(tabs, ["pending","accepted","rejected"]):
        with tab:
            display_grid([a for a in apps if a['status']==status], status=="pending")

def display_grid(apps, show_actions):
    if not apps:
        return st.info("No applications here.")
    for i in range(0, len(apps), 2):
        cols = st.columns(2, gap="medium")
        for col, app in zip(cols, apps[i:i+2]):
            with col:
                display_card(app, show_actions)

def clean(text): 
    return html.escape(str(text).strip()) if text and str(text).lower() not in ("none","null","") else "Not provided"

def fmt_date(ds):
    if not ds: return "Not available"
    try:
        dt = datetime.fromisoformat(ds.replace("Z","+00:00")) if isinstance(ds,str) else ds
        d = (datetime.now() - dt).days
        rel = ("Today","Yesterday")[d==1] if d<2 else (f"{d} days ago" if d<7 else f"{d//7} weeks ago")
        return f"{dt.strftime('%B %d, %Y at %I:%M %p')} ({rel})"
    except:
        return str(ds)[:10]

def display_card(a, show_actions):
    name, title, phone, skills, salary = map(clean, (a.get("applicant_name"),a.get("job_title"),
                                                    a.get("applicant_phone"),a.get("applicant_skills"),
                                                    a.get("expected_salary")))
    status = a.get("status","pending")

    cfg = {
        "pending":  ("🟡", "#fff3cd", "#856404", "#E79E0C"),
        "accepted": ("✅", "#d4edda", "#155724", "#0ad741"),
        "rejected": ("❌", "#f8d7da", "#721c24", "#f01b30"),
    }
    icon, badge_bg, badge_color, card_bg = cfg.get(status, cfg["pending"])
    
    html_card = f"""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 15px; padding: 20px; margin: 15px 0; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; border-left: 5px solid {card_bg}; position: relative; overflow: hidden;
    ">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <h4 style="margin:0;">👤 {name}</h4>
        <span style="
            background:{badge_bg};
            color:{badge_color};
            padding:2px 8px;
            border-radius:8px;
        ">
          {icon} {status.title()}
        </span>
      </div>
      <p style="color:#6c757d; margin:4px 0;">
        💼 <strong>{title}</strong>
      </p>
      <div style="font-size:0.85rem; color:#495057; line-height:1.4;">
        <div>📞 {phone}</div>
        <div>🛠️ {skills}</div>
        <div>💰 ₹{salary}</div>
      </div>
    </div>
    """

    st.markdown(html_card, unsafe_allow_html=True)
    with st.expander("📋 More Details"):
        email = clean(a.get("applicant_email"))
        exp = clean(a.get("applicant_experience"))
        date = fmt_date(a.get("applied_date"))
        st.markdown(f"**✉️ Email:** {email}")
        st.markdown(f"**📈 Experience:** {exp}")
        st.markdown(f"**📅 Applied Date:** {date}")
        contact = f"Phone: {phone}\nEmail: {email}"
        st.code(contact, language=None)
    if show_actions:
        c1,c2,c3 = st.columns(3)
        if c1.button("✅ Accept", key=f"acc{a['id']}", use_container_width=True):
            update_application_status(a['id'],"accepted","Accepted") and st.success("✅ Accepted!") and st.rerun()
        if c2.button("❌ Reject", key=f"rej{a['id']}", use_container_width=True):
            update_application_status(a['id'],"rejected","Rejected") and st.info("❌ Rejected") and st.rerun()
        if c3.button("📞 Contact", key=f"con{a['id']}", use_container_width=True):
            st.balloons(); st.success(f"📱 {phone}"); st.success(f"✉️ {email}")
    st.markdown("<br>", unsafe_allow_html=True)
