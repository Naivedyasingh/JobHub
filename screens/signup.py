import streamlit as st
from utils.validation import validate_email, validate_phone, validate_password
from utils.auth import next_user_id
from utils.data_helpers import read_json, write_json
import os
from datetime import datetime


DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")


def signup_page():
    st.markdown("""
    <style>
      #MainMenu {visibility: hidden;}
      header {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    
    st.markdown(f"<h1 style='text-align:center;color:#1f77b4;'>✨ {role_name} Sign Up</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:center;color:#222;margin-top:-10px;font-weight:400;'>Create your account and start your journey today.</h4>", unsafe_allow_html=True)


    st.markdown("""<style>.terms-checkbox{margin-top:-10px;margin-bottom:20px;}.back-button{margin-top:20px;}</style>""", unsafe_allow_html=True)


    with st.container():
        col1, col2 = st.columns(2, gap="large")
        with col1:
            name = st.text_input("📛 Full Name", key="signup_name")
            phone = st.text_input("📱 Phone Number", key="signup_phone")
            email = st.text_input("📧 Email", key="signup_email")
        with col2:
            gender = st.selectbox("👤 Gender", ["Select", "Male", "Female", "Other"], key="signup_gender")
            pwd = st.text_input("🔒 Password", type="password", key="signup_password")
            cpwd = st.text_input("🔒 Confirm Password", type="password", key="signup_confirm_password")


        company_name = ""
        if st.session_state.role == "hire":
            company_name = st.text_input("🏢 Company Name", key="signup_company_name")


        agree = st.checkbox("I agree to the Terms and Conditions", key="signup_agree")


        if st.button("🚀 Create Account", use_container_width=True, type="primary", key="signup_submit"):
 
            name_clean = name.strip()
            phone_clean = phone.strip()
            email_clean = email.strip()
            pwd_clean = pwd.strip()
            cpwd_clean = cpwd.strip()
            company_name_clean = company_name.strip() if st.session_state.role == "hire" else ""
            
            required = [name_clean, phone_clean, email_clean, pwd_clean, cpwd_clean]
            if st.session_state.role == "hire":
                required.append(company_name_clean)
            
            if not all(required):
                empty_fields = []
                if not name_clean: empty_fields.append("Full Name")
                if not phone_clean: empty_fields.append("Phone Number")
                if not email_clean: empty_fields.append("Email")
                if not pwd_clean: empty_fields.append("Password")
                if not cpwd_clean: empty_fields.append("Confirm Password")
                if st.session_state.role == "hire" and not company_name_clean: 
                    empty_fields.append("Company Name")
                
                st.error(f"Please fill the following required fields: {', '.join(empty_fields)}")
            elif gender == "Select":
                st.error("Please select your gender.")    
            elif not agree:
                st.error("You must accept the Terms and Conditions.")
            elif pwd_clean != cpwd_clean:
                st.error("Passwords do not match.")
            elif not validate_phone(phone_clean):
                st.error("Phone number must be exactly 10 digits.")
            elif not validate_email(email_clean):
                st.error("Invalid email address.")
            else:
                is_valid, error_msg = validate_password(pwd_clean)
                if not is_valid:
                    st.error(error_msg)
                else:
                    users = read_json(USERS_FILE)
                    if any(u["phone"] == phone_clean for u in users):
                        st.error("Phone number already registered.")
                    elif any(u["email"].lower() == email_clean.lower() for u in users):
                        st.error("Email already registered.")
                    else:
                        user = {
                            "id": next_user_id(users), 
                            "role": st.session_state.role, 
                            "name": name_clean, 
                            "phone": phone_clean, 
                            "email": email_clean, 
                            "gender": gender, 
                            "password": pwd_clean, 
                            "availability_status": "available", 
                            "created_at": datetime.now().isoformat()
                        }
                        if st.session_state.role == "hire" and company_name_clean:
                            user["company_name"] = company_name_clean
                        users.append(user)
                        write_json(USERS_FILE, users)
                        st.success("Account created successfully!")
                        st.session_state.current_user = user
                        st.session_state.page = f"{user['role']}_dashboard"
                        st.rerun()
    
    st.markdown("\n")
    st.markdown("".join(["─"] * 97),)
    st.markdown("\n")


    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "auth_choice"
            st.rerun()
    with col2:
        if st.button("📝 Already have Account", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
