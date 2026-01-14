import streamlit as st
import pandas as pd
from api_client import api

def render():
    st.header("🗂️ Sections Management")
    
    # Show success message if pending from previous run
    if "section_success" in st.session_state:
        st.success(st.session_state.pop("section_success"))

    tab1, tab2 = st.tabs(["View Sections", "Add Section"])

    with tab1:
        st.subheader("Library Sections")
        sections = api.get("sections/")
        
        if sections:
            df = pd.DataFrame(sections)
            if not df.empty:
                # Reorder or select columns if needed
                st.dataframe(df[["id", "name", "description"]])
                
                # simple deletion UI
                st.write("---")
                st.subheader("Delete Section")
                section_to_delete = st.selectbox("Select Section to Delete", 
                                               options=[f"{s['name']} (ID: {s['id']})" for s in sections],
                                               index=None,
                                               placeholder="Choose a section..."
                                              )
                
                if section_to_delete and st.button("Delete Selected Section", type="primary"):
                    # efficient string parsing or just use a dict map
                    # recreating map for safety
                    sec_map = {f"{s['name']} (ID: {s['id']})": s['id'] for s in sections}
                    s_id = sec_map[section_to_delete]
                    
                    if api.delete(f"sections/{s_id}"):
                        st.session_state["section_success"] = "Section deleted successfully!"
                        st.rerun()
            else:
                st.info("No sections found.")
        else:
            st.info("No sections found.")
            
        if st.button("Refresh Sections"):
            st.rerun()

    with tab2:
        st.subheader("Create New Section")
        
        with st.form("add_section_form"):
            name = st.text_input("Section Name (e.g., 'Fiction', 'Science')")
            description = st.text_area("Description")
            
            submitted = st.form_submit_button("Create Section")
            
            if submitted:
                if not name:
                    st.error("Section name is required.")
                else:
                    payload = {
                        "name": name,
                        "description": description
                    }
                    if api.post("sections/", payload):
                        st.session_state["section_success"] = f"Section '{name}' created successfully!"
                        st.rerun()
