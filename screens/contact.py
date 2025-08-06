# pages/contact.py

import streamlit as st
def contact_page():
    st.title("📞 Contact Us")
    
    st.markdown("""
    ### Get in Touch with JobConnect Team
    
    We're here to help you with any questions or concerns!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📍 Contact Information
        
        **Phone:** +91-9876543210  
        **Email:** support@jobHub.com  
        **Address:** IT park near yash technologies, Indore, India
        
        **Business Hours:**  
        Monday - Friday: 9:00 AM - 6:00 PM  
        Saturday: 10:00 AM - 4:00 PM  
        Sunday: Closed
        """)
    
    with col2:
        st.markdown("#### 💬 Send us a Message")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name", key="contact_name")
            email = st.text_input("Email Address", key="contact_email")
            subject = st.selectbox("Subject", ["General Inquiry", "Technical Support", "Account Issues", "Feedback"], key="contact_subject")
            message = st.text_area("Message", height=100, key="contact_message")
            
            if st.form_submit_button("📤 Send Message", type="primary"):
                if name and email and message:
                    st.success("✅ Message sent successfully! We'll get back to you soon.")
                else:
                    st.error("Please fill all required fields")
    st.markdown("\n")
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        if st.button("<- Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
