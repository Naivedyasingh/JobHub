import streamlit as st
from utils.data_helpers import read_json
hide_streamlit_style = """
<style>
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def stat_card(value, label, delta=None, delta_color="green"):
    """Create a statistics card with optional delta"""
    colors = {"green": "#28a745", "red": "#dc3545", "blue": "#007bff", "orange": "#fd7e14", "gray": "#e8f4fd"}
    delta_html = f"<div style='color: {colors.get(delta_color, '#28a745')}; font-size: 0.8rem; font-weight: 600; margin-top: 0.3rem;'>{delta}</div>" if delta else ""
    return f"""<div style='text-align: center; padding: 1.5rem; background-color: #e8f4fd; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #6495ed;'>
        <div style='font-size: 1.8rem; font-weight: bold; color: #2c3e50; margin-bottom: 0.5rem;'>{value}</div>
        <div style='color: #666; font-size: 0.9rem;'>{label}</div>{delta_html}</div>"""

def info_card(title, content, bg_color, border_color, title_color, icon):
    """Create an information card"""
    return f"""<div style='padding: 2rem; background-color: {bg_color}; border-radius: 15px; margin: 1rem 0; border-left: 5px solid {border_color};'>
        <h4 style='text-align: center; margin-bottom: 1.5rem; color: {title_color};'>{icon} <strong>{title}</strong></h4>
        <div style='color: #2c3e50; line-height: 1.8;'>{content}</div></div>"""

def home_page():
    st.markdown("""
    <style>
      #MainMenu {visibility: hidden;}
      header {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.image(r".streamlit/public/title_logo.png", width=500)
        st.markdown("""
        <div style='text-align: center; padding: 0; margin: 0;'>
          <h3 style='color: #000000; font-weight: 500; margin: 0;padding:0;'>Connecting Dreams with Opportunities</h3><br><br><br><br><br><br>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("<h3 style='text-align: center; color: #2c3e50; margin-bottom: 1.5rem;'>🚀 <strong>Get Started Today!</strong></h3>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stButton > button {
            height: 55px;
            font-size: 60rem;
            padding: 10px 24px;
            border: 1.5px solid #000;
            border-radius: 10px;
            background-color: #fff;
            color: #000;
            font-weight: 900;
        }
        div.stButton > button:hover {
            background-color: #dcdcdc ;
            border-color: #999;
        }
        .info-div {
            text-align: center;
            padding: 1rem;
            background-color: #e8f4fd;
            border-left: 5px solid #6495ed;
            border-radius: 10px;
            margin-top: 0.5rem;
            font-weight: 600;
            
        }
        </style>
        """, unsafe_allow_html=True)


    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 I WANT A JOB ", key="job_button", use_container_width=True, type="secondary"):
            st.session_state.role = "job"
            st.session_state.page = "auth_choice"
            st.rerun()
        st.markdown("""
            <div class="info-div">
                <strong>Perfect for:</strong><br>🔧 Skilled workers<br>🏠 Household helpers<br>🚀 Service providers
            </div>""", unsafe_allow_html=True)
    
    with col2:
        if st.button("🏢 I WANT TO HIRE ", key="hire_button", use_container_width=True, type="secondary"):
            st.session_state.role = "hire"
            st.session_state.page = "auth_choice"
            st.rerun()
        st.markdown("""
            <div class="info-div">
                <strong>Perfect for:</strong><br>🏢 Companies<br>🚀 Startups<br>🏭 Organizations
            </div>""", unsafe_allow_html=True)
    
    st.markdown("\n")
    st.markdown("""
    <hr style="width: 100%; height: 2px; background-color: #444; border: none; margin: 1.5rem 0; border-radius: 2px;">
    """, unsafe_allow_html=True)


    users = read_json("data/users.json")
    job_seekers = [u for u in users if u.get('role') == 'job']
    employers = [u for u in users if u.get('role') == 'hire']
    
    st.markdown("### 📊 **Platform Impact**")
    col1, col2, col3, col4 = st.columns(4)
    stats = [(len(job_seekers), "Job Seekers", "Active", "green"), (len(employers), "Employers", "Hiring", "blue"), 
             (len(job_seekers) * 2, "Connections", "+12%", "green"), ("85%" if len(users) > 5 else "Growing", "Success Rate", "High", "orange")]
    
    for col, (value, label, delta, delta_color) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(stat_card(value, label, delta, delta_color), unsafe_allow_html=True)
    
    st.markdown("""
    <hr style="width: 100%; height: 2px; background-color: #444; border: none; margin: 1.5rem 0; border-radius: 2px;">
    """, unsafe_allow_html=True)
    st.markdown("### 🔄 **Our Impact on Employment**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(info_card("Before JobConnect", "• Job seekers struggled to find reliable work<br>• Employers had difficulty finding trusted help<br>• Time-consuming manual searching process<br>• High agency fees and commissions<br>• Limited job visibility and opportunities<br>• No proper verification system", "#f9ecec", "#e74c3c", "#c0392b", "😔"), unsafe_allow_html=True)
    with col2:
        st.markdown(info_card("After JobConnect", "• Easy access to verified job opportunities<br>• Secure platform with identity verification<br>• Digital profiles showcase skills & experience<br>• Fair salary expectations and transparency<br>• Quick job matching and applications<br>• Direct communication between parties", "#e9f4ec", "#27ae60", "#27ae60", "🌟"), unsafe_allow_html=True)
    
    st.markdown("""
    <hr style="width: 100%; height: 2px; background-color: #444; border: none; margin: 1.5rem 0; border-radius: 2px;">
    """, unsafe_allow_html=True)
    st.markdown("\n### 🎉 **Platform Growth**")
    cities_represented = len(set([u.get('city', '').lower() for u in users if u.get('city')]))
    skills_count = len(set([skill for u in job_seekers for skill in u.get('work_type', [])]))
    
    st.markdown(f"""<div style='text-align: center; padding: 2rem; background-color: #f0f0ff; border-radius: 15px; margin: 1rem 0; border-left: 5px solid #1f77b4;'>
        <h4 style='color: #1f77b4; margin-bottom: 1.5rem;'>📊 Our Growing Community</h4>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='margin: 0.5rem;'><div style='font-size: 1.5rem; font-weight: bold; color: #2c3e50;'>{cities_represented if cities_represented > 0 else 5}+</div><div style='color: #666; font-size: 0.9rem;'>Cities Covered</div></div>
            <div style='margin: 0.5rem;'><div style='font-size: 1.5rem; font-weight: bold; color: #2c3e50;'>{skills_count if skills_count > 0 else 15}+</div><div style='color: #666; font-size: 0.9rem;'>Skills Available</div></div>
            <div style='margin: 0.5rem;'><div style='font-size: 1.5rem; font-weight: bold; color: #2c3e50;'>{"Expert" if job_seekers else "All"}</div><div style='color: #666; font-size: 0.9rem;'>Experience Levels</div></div>
        </div><p style='margin-top: 1rem; color: #666; font-style: italic;'>"Connecting talent with opportunities across the region"</p></div>""", unsafe_allow_html=True)
    
   
    st.markdown("""
    <hr style="width: 100%; height: 2px; background-color: #444; border: none; margin: 1.5rem 0; border-radius: 2px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .contact-link {
        cursor: pointer;
        color: #1f77b4 !important;
        text-decoration: underline;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    .contact-link:hover {
        color: #0d5aa7 !important;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; color: #333; font-size: 0.9rem;'>
        💡 <strong>Why Choose JobConnect?</strong><br>
        ✅ Verified profiles • 🔒 Secure platform • 💰 Fair pricing • ⭐ Quality assurance<br>
        🤝 Personalized support • 🧑‍💻 Easy job posting & application • ⚡ Fast response times<br><br>
        <span style='font-size: 1.1rem; color: #2c3e50; font-weight: 600;'>
            📱 Email us: <a href="mailto:support@JobHub.com" style="color: #2c3e50;">support@JobHub.com</a> | 📞 +91-91114-39303
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("📞 Visit Contact Page", use_container_width=True, type="primary"):
            st.session_state.page = "contact"
            st.rerun()
    

