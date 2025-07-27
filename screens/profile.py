# pages/profile.py

import streamlit as st
from utils.auth import calculate_profile_completion, update_user_profile
from utils.data_helpers import read_json, write_json
from utils.validation import validate_email, validate_phone, validate_aadhaar
import os

DATA_FOLDER = "data"
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")

def _load_current_user():
    """Helper to reload current_user from disk after profile update."""
    users = read_json(USERS_FILE)
    uid = st.session_state.current_user["id"]
    for u in users:
        if u["id"] == uid:
            st.session_state.current_user = u
            return u
    return st.session_state.current_user

def profile_page():
    user = st.session_state.current_user
    st.title("👤 My Profile")
    
    if user['role'] == 'job':
        job_seeker_profile()
    else:
        employer_profile()

def job_seeker_profile():
    user = st.session_state.current_user
    
    # Profile sections
    tab1, tab2, tab3 = st.tabs(["📋 Personal Info", "💼 Professional Info", "📍 Location & Contact"])
    
    with tab1:
        st.subheader("Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=user.get('name', ''), key="profile_name")
            phone = st.text_input("Phone Number", value=user.get('phone', ''), key="profile_phone")
            email = st.text_input("Email", value=user.get('email', ''), key="profile_email")
        
        with col2:
            # Safe gender selection with fallback
            gender_options = ["Male", "Female", "Other"]
            user_gender = user.get('gender', 'Male')
            if user_gender not in gender_options:
                user_gender = 'Male'  # Default fallback
            
            gender = st.selectbox("Gender", gender_options, 
                                index=gender_options.index(user_gender), key="profile_gender")
            
            aadhaar = st.text_input("Aadhaar Number", value=user.get('aadhaar', ''), placeholder="12-digit number", key="profile_aadhaar")
            date_of_birth = st.date_input("Date of Birth", key="profile_dob")
    
    with tab2:
        st.subheader("Professional Information")
        
        col1, col2 = st.columns(2)
        with col1:
            # Safe experience selection with fallback
            exp_options = ["Fresher", "1-2 years", "2-5 years", "5+ years"]
            user_exp = user.get('experience', 'Fresher')
            if user_exp not in exp_options:
                user_exp = 'Fresher'  # Default fallback
            
            experience = st.selectbox("Experience Level", exp_options,
                                    index=exp_options.index(user_exp), key="profile_experience")
            
            job_types = st.multiselect("Job Types/Skills", 
                                     ["Maid", "Cook", "Driver", "Cleaner", "Babysitter", "Gardener", "Security Guard", "Electrician", "Plumber"],
                                     default=user.get('job_types', []), key="profile_job_types")
        
        with col2:
            # Safe salary value with proper range validation
            user_salary = user.get('expected_salary', 15000)
            # Ensure salary is within valid range
            if not isinstance(user_salary, (int, float)) or user_salary < 5000:
                user_salary = 15000  # Default fallback
            elif user_salary > 100000:
                user_salary = 100000  # Cap at maximum
            
            expected_salary = st.number_input("Expected Monthly Salary (₹)", 
                                            min_value=5000, max_value=100000, 
                                            value=int(user_salary), step=1000, key="profile_salary")
            
            availability = st.multiselect("Availability", 
                                        ["Full Time", "Part Time", "Weekends", "Night Shifts"],
                                        default=user.get('availability', []), key="profile_availability")
        
        # Safe education selection with fallback
        edu_options = ["Primary", "Secondary", "Higher Secondary", "Graduate", "Post Graduate"]
        user_edu = user.get('education', 'Secondary')
        if user_edu not in edu_options:
            user_edu = 'Secondary'  # Default fallback
            
        education = st.selectbox("Education Level", edu_options,
                               index=edu_options.index(user_edu), key="profile_education")
        
        languages = st.multiselect("Languages Known", 
                                 ["Hindi", "English", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati"],
                                 default=user.get('languages', []), key="profile_languages")
    
    with tab3:
        st.subheader("Location & Contact")
        
        col1, col2 = st.columns(2)
        with col1:
            address = st.text_area("Full Address", value=user.get('address', ''), key="profile_address")
            city = st.text_input("City", value=user.get('city', ''), key="profile_city")
            
            # Safe state selection with fallback
            state_options = ["Maharashtra", "Madhya Pradesh", "Karnataka", "Gujarat", "West Bengal"]
            user_state = user.get('state', 'Maharashtra')
            if user_state not in state_options:
                user_state = 'Maharashtra'  # Default fallback
                
            state = st.selectbox("State", state_options,
                               index=state_options.index(user_state), key="profile_state")
        
        with col2:
            pincode = st.text_input("PIN Code", value=user.get('pincode', ''), key="profile_pincode")
            emergency_contact = st.text_input("Emergency Contact", value=user.get('emergency_contact', ''), key="profile_emergency_contact")
            emergency_name = st.text_input("Emergency Contact Name", value=user.get('emergency_name', ''), key="profile_emergency_name")
    
    # Save button
    if st.button("💾 Save Profile", type="primary", use_container_width=True, key="save_job_profile"):
        updates = {
            'name': name, 'phone': phone, 'email': email, 'gender': gender,
            'aadhaar': aadhaar, 'experience': experience, 'job_types': job_types,
            'expected_salary': expected_salary, 'availability': availability,
            'education': education, 'languages': languages, 'address': address,
            'city': city, 'state': state, 'pincode': pincode,
            'emergency_contact': emergency_contact, 'emergency_name': emergency_name
        }
        
        if validate_phone(phone) and (not aadhaar or validate_aadhaar(aadhaar)):
            updated_user = update_user_profile(user['id'], updates)
            if updated_user:
                st.session_state.current_user = updated_user
                st.success("✅ Profile saved successfully!")
                st.balloons()
                st.rerun()  # Refresh to show updated data
            else:
                st.error("Failed to save profile")
        else:
            st.error("Please check phone number and Aadhaar format")

def employer_profile():
    user = st.session_state.current_user
    
    # Profile sections for employer
    tab1, tab2, tab3 = st.tabs(["📋 Personal Info", "🏢 Company Info", "📍 Business Location"])
    
    with tab1:
        st.subheader("Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=user.get('name', ''), key="employer_name")
            phone = st.text_input("Phone Number", value=user.get('phone', ''), key="employer_phone")
            email = st.text_input("Email", value=user.get('email', ''), key="employer_email")
        
        with col2:
            # Safe gender selection with fallback
            gender_options = ["Male", "Female", "Other"]
            user_gender = user.get('gender', 'Male')
            if user_gender not in gender_options:
                user_gender = 'Male'  # Default fallback
                
            gender = st.selectbox("Gender", gender_options,
                                index=gender_options.index(user_gender), key="employer_gender")
            
            designation = st.text_input("Designation", value=user.get('designation', ''), key="employer_designation")
    
    with tab2:
        st.subheader("Company Information")
        
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name", value=user.get('company_name', ''), key="employer_company_name")
            
            # Safe company type selection with fallback
            company_type_options = ["Family", "Small Business", "Medium Enterprise", "Large Corporation"]
            user_company_type = user.get('company_type', 'Family')
            if user_company_type not in company_type_options:
                user_company_type = 'Family'  # Default fallback
                
            company_type = st.selectbox("Company Type", company_type_options,
                                      index=company_type_options.index(user_company_type), key="employer_company_type")
        
        with col2:
            # Safe industry selection with fallback
            industry_options = ["Domestic Services", "Healthcare", "Technology", "Manufacturing", "Retail", "Other"]
            user_industry = user.get('industry', 'Domestic Services')
            if user_industry not in industry_options:
                user_industry = 'Domestic Services'  # Default fallback
                
            industry = st.selectbox("Industry", industry_options,
                                  index=industry_options.index(user_industry), key="employer_industry")
            
            # Safe company size selection with fallback
            size_options = ["1-10", "11-50", "51-200", "200+"]
            user_size = user.get('company_size', '1-10')
            if user_size not in size_options:
                user_size = '1-10'  # Default fallback
                
            company_size = st.selectbox("Company Size", size_options,
                                      index=size_options.index(user_size), key="employer_company_size")
        
        business_description = st.text_area("Business Description", value=user.get('business_description', ''), key="employer_business_description")
    
    with tab3:
        st.subheader("Business Location")
        
        col1, col2 = st.columns(2)
        with col1:
            address = st.text_area("Company Address", value=user.get('address', ''), key="employer_address")
            city = st.text_input("City", value=user.get('city', ''), key="employer_city")
            
            # Safe state selection with fallback
            state_options = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal"]
            user_state = user.get('state', 'Maharashtra')
            if user_state not in state_options:
                user_state = 'Maharashtra'  # Default fallback
                
            state = st.selectbox("State", state_options,
                               index=state_options.index(user_state), key="employer_state")
        
        with col2:
            pincode = st.text_input("PIN Code", value=user.get('pincode', ''), key="employer_pincode")
            website = st.text_input("Website (Optional)", value=user.get('website', ''), key="employer_website")
    
    # Save button
    if st.button("💾 Save Profile", type="primary", use_container_width=True, key="save_employer_profile"):
        updates = {
            'name': name, 'phone': phone, 'email': email, 'gender': gender,
            'designation': designation, 'company_name': company_name, 
            'company_type': company_type, 'industry': industry, 'company_size': company_size,
            'business_description': business_description, 'address': address,
            'city': city, 'state': state, 'pincode': pincode, 'website': website
        }
        
        if validate_phone(phone):
            updated_user = update_user_profile(user['id'], updates)
            if updated_user:
                st.session_state.current_user = updated_user
                st.success("✅ Profile saved successfully!")
                st.balloons()
                st.rerun()  # Refresh to show updated data
            else:
                st.error("Failed to save profile")
        else:
            st.error("Please check phone number format")
