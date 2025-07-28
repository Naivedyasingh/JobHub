import streamlit as st
from utils.auth import calculate_profile_completion, update_user_profile

def render_sidebar():
    # Don't render anything for guests
    if st.session_state.current_user is None:
        return

    user = st.session_state.current_user

    with st.sidebar:

        # Enhanced avatar with status for job seekers
        if user['role'] == 'job':
            avatar = "👨‍💼" if user.get('gender') == 'Male' else \
                     "👩‍💼" if user.get('gender') == 'Female' else "🧑‍💼"
            current_status = user.get('availability_status', 'available')
            status_info = {
                'available': ('🟢', '#28a745', 'Ready to Work'),
                'busy': ('🟡', '#ffc107', 'Currently Busy'),
                'not_available': ('🔴', '#dc3545', 'Not Available')
            }
            icon, color, text = status_info.get(current_status)

            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 1rem;
                border: 2px solid {color};
                border-radius: 15px;
                background: linear-gradient(135deg, {color}15, {color}25);
            ">
                <div style="font-size: 4rem;">{avatar}</div>
                <h3>{user['name']}</h3>
                <p style="color: #666;">Job Seeker</p>
                <div style="
                    background: {color};
                    color: white;
                    padding: 5px 10px;
                    border-radius: 20px;
                    margin: 5px 0;
                ">
                    <strong>{icon} {text}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Quick status changer
            new_status = st.selectbox(
                "Change Status:",
                list(status_info.keys()),
                index=list(status_info.keys()).index(current_status),
                format_func=lambda x: f"{status_info[x][0]} {status_info[x][2]}",
                key="sidebar_status_change"
            )
            if new_status != current_status:
                update_user_profile(user['id'], {'availability_status': new_status})
                st.session_state.current_user['availability_status'] = new_status
                st.success("Status updated!")
                st.rerun()

        else:
            # Regular employer avatar
            avatar = "👨‍💼" if user.get('gender') == 'Male' else \
                     "👩‍💼" if user.get('gender') == 'Female' else "🏢"
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 4rem;">{avatar}</div>
                <h3>{user['name']}</h3>
                <p style="color: #666;">Employer</p>
            </div>
            """, unsafe_allow_html=True)

        # Profile Completion with custom small text (Solution 2)
        completion = calculate_profile_completion(user)
        st.markdown(f"""
        <div style=" margin: 10px 0; padding: 8px; background: #f0f2f6; border-radius: 8px;">
            <div style="font-size: 1rem; color: #666; margin-bottom: 2px;">Profile Completion</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #1f77b4;">{completion}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(completion / 100)

        st.markdown("---")
        st.subheader("🧭 Navigation")

        if st.button("🏠 Dashboard", use_container_width=True, key="sidebar_dashboard"):
            st.session_state.page = f"{user['role']}_dashboard"
            st.rerun()

        if st.button("👤 My Profile", use_container_width=True, key="sidebar_profile"):
            st.session_state.page = "profile"
            st.rerun()

        if user['role'] == 'job':
            if st.button("📋 My Applications", use_container_width=True, key="sidebar_my_applications"):
                st.session_state.page = "my_applications"
                st.rerun()
        else:
            if st.button("👥 Browse Job Seekers", use_container_width=True, key="sidebar_browse_seekers"):
                st.session_state.page = "browse_job_seekers"
                st.rerun()
            if st.button("📝 Post Job", use_container_width=True, key="sidebar_post_job"):
                st.session_state.page = "post_job"
                st.rerun()
            if st.button("📋 Applications", use_container_width=True, key="sidebar_view_applications"):
                st.session_state.page = "view_applications"
                st.rerun()

        if st.button("📞 Contact Us", use_container_width=True, key="sidebar_contact"):
            st.session_state.page = "contact"
            st.rerun()

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="secondary", key="sidebar_logout"):
            st.session_state.current_user = None
            st.session_state.page = "home"
            st.rerun()
