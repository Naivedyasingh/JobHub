# pages/signup.py

import streamlit as st
from utils.validation import validate_email, validate_phone, validate_password
from utils.auth import next_user_id
from utils.data_helpers import read_json, write_json
import os
import datetime

DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")

def signup_page():
    role_name = "Job Seeker" if st.session_state.role == "job" else "Employer"
    st.title(f"✨ {role_name} Sign Up")

    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("📛 Full Name", key="signup_name")
        phone = st.text_input("📱 Phone Number", key="signup_phone")
        email = st.text_input("📧 Email", key="signup_email")
    
    with col2:
        gender = st.selectbox("👤 Gender", ["Select", "Male", "Female", "Other"], key="signup_gender")
        pwd = st.text_input("🔒 Password", type="password", key="signup_password")
        cpwd = st.text_input("🔒 Confirm Password", type="password", key="signup_confirm_password")
    
    if st.session_state.role == "hire":
        company_name = st.text_input("🏢 Company Name", key="signup_company_name")
    
    agree = st.checkbox("I agree to the Terms and Conditions", key="signup_agree")

    if st.button("🚀 Create Account", use_container_width=True, type="primary", key="signup_submit"):
        required = [name.strip(), phone.strip(), email.strip(), pwd.strip(), cpwd.strip()]
        if st.session_state.role == "hire":
            required.append(company_name.strip() if 'company_name' in locals() else "")
        
        if not all(required) or gender == "Select":
            st.error("Please fill all required fields and select gender.")
            return
        if not agree:
            st.error("You must accept the Terms and Conditions.")
            return
        if pwd != cpwd:
            st.error("Passwords do not match.")
            return
        if not validate_phone(phone):
            st.error("Phone number must be exactly 10 digits.")
            return

        users = read_json("data/users.json")
        if any(u["phone"] == phone for u in users):
            st.error("Phone number already registered.")
            return

        user = {
            "id": next_user_id(users),
            "role": st.session_state.role,
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
            "gender": gender,
            "password": pwd.strip(),
            "availability_status": "available",
            "created_at": datetime.now().isoformat()
        }
        
        if st.session_state.role == "hire" and 'company_name' in locals():
            user["company_name"] = company_name.strip()
        
        users.append(user)
        write_json("data/users.json", users)

        st.success("Account created successfully!")
        st.session_state.current_user = user
        st.session_state.page = f"{user['role']}_dashboard"
        st.balloons()
        st.rerun()

    if st.button("← Back", key="signup_back"):
        st.session_state.page = "auth_choice"
        st.rerun()
