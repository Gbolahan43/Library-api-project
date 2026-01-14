import streamlit as st
import pandas as pd
from api_client import api

def render():
    st.header("💰 Fines Management")
    
    if "fine_success" in st.session_state:
        st.success(st.session_state.pop("fine_success"))
    
    users = api.get("users/")
    user_options = {f"{u['name']} ({u['employee_id']})": u['id'] for u in users} if users else {}
    
    selected_user_key = st.selectbox("Select User to View Fines", options=list(user_options.keys()) if user_options else [])
    
    if selected_user_key:
        user_id = user_options[selected_user_key]
        fines = api.get(f"fines/?user_id={user_id}")
        
        if fines:
            df = pd.DataFrame(fines)
            if not df.empty:
                st.subheader("Fine History")
                # Clean up display
                st.dataframe(df[["amount", "status", "fine_date", "paid_at"]])
                
                # Payment Action for Pending Fines
                pending_fines = [f for f in fines if f['status'] == 'Pending']
                if pending_fines:
                    st.subheader("Pay Outstanding Fines")
                    for fine in pending_fines:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"Fine: ${fine['amount']} (Date: {fine['fine_date'][:10]})")
                        with col2:
                            if st.button("Pay", key=fine['id']):
                                if api.put(f"fines/{fine['id']}/pay", {"amount_paid": fine['amount'], "payment_method": "Cash"}):
                                    st.session_state["fine_success"] = "Fine paid!"
                                    st.rerun()
            else:
                st.info("No fines recorded for this user.")
        else:
            st.info("No fines found.")
