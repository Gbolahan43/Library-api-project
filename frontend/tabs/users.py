import streamlit as st
import pandas as pd
from api_client import api

def render():
    st.header("👤 Users Management")
    
    if "user_success" in st.session_state:
        st.success(st.session_state.pop("user_success"))

    tab1, tab2 = st.tabs(["View Users", "Register User"])

    with tab1:
        st.subheader("Registered Users")
        users = api.get("users/")
        if users:
            df = pd.DataFrame(users)
            if not df.empty:
                st.dataframe(df[["name", "email", "employee_id", "role", "is_active"]])
            else:
                st.info("No users found.")
        
        if st.button("Refresh Users"):
            st.rerun()

    with tab2:
        st.subheader("Register New User")
        with st.form("add_user_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            employee_id = st.text_input("Employee ID / Member ID")
            
            submitted = st.form_submit_button("Register User")
            
            if submitted:
                payload = {
                    "name": name,
                    "email": email,
                    "employee_id": employee_id
                }
                if api.post("users/", payload):
                    st.session_state["user_success"] = "User registered successfully!"
                    st.rerun()
