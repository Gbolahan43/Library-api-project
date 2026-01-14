import streamlit as st
import pandas as pd
from api_client import api

def render():
    st.header("📖 Books Management")
    
    # Show success message if pending from previous run
    if "book_success" in st.session_state:
        st.success(st.session_state.pop("book_success"))

    tab1, tab2 = st.tabs(["View Books", "Add Book"])

    with tab1:
        st.subheader("Inventory")
        books = api.get("books/")
        if books:
            df = pd.DataFrame(books)
            if not df.empty:
                # Reorder columns for better view
                cols = ["title", "author", "isbn", "available_quantity", "quantity", "section_id"]
                st.dataframe(df[cols])
            else:
                st.info("No books found.")
        
        if st.button("Refresh Books"):
            st.rerun()

        st.divider()
        st.subheader("Delete Book")
        if books:
            book_options = {f"{b['title']} (ID: {b['id']})": b['id'] for b in books}
            book_to_delete = st.selectbox("Select Book to Delete", 
                                        options=list(book_options.keys()), 
                                        index=None,
                                        placeholder="Choose a book..."
                                        )
            
            if book_to_delete and st.button("Delete Selected Book", type="primary"):
                book_id = book_options[book_to_delete]
                if api.delete(f"books/{book_id}"):
                    st.session_state["book_success"] = "Book deleted successfully!"
                    st.rerun()

    with tab2:
        st.subheader("Add New Book")
        
        # Fetch sections for dropdown
        sections = api.get("sections/")
        section_options = {s['name']: s['id'] for s in sections} if sections else {}
        
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            isbn = st.text_input("ISBN")
            year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
            
            section_name = st.selectbox("Section", options=list(section_options.keys()) if section_options else [])
            
            quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
            
            submitted = st.form_submit_button("Add Book")
            
            if submitted:
                selected_section_id = section_options.get(section_name)
                
                if not selected_section_id:
                    st.error("Please create and select a valid section first.")
                else:
                    payload = {
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                        "publication_year": year,
                        "section_id": selected_section_id,
                        "quantity": quantity
                    }
                    if api.post("books/", payload):
                        st.session_state["book_success"] = "Book added successfully!"
                        st.rerun()
