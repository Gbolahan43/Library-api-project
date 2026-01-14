import streamlit as st
import pandas as pd
from api_client import api

def render():
    st.header("🔄 Borrowing & Returns")

    tab1, tab2 = st.tabs(["Borrow Book", "Return Book"])

    # Load shared data
    users = api.get("users/")
    books = api.get("books/")
    
    user_options = {f"{u['name']} ({u['employee_id']})": u['id'] for u in users} if users else {}
    book_options = {f"{b['title']} (Avail: {b['available_quantity']})": b['id'] for b in books if b['available_quantity'] > 0} if books else {}

    with tab1:
        st.subheader("Issue a Book")
        with st.form("borrow_form"):
            user_key = st.selectbox("Select User", options=list(user_options.keys()) if user_options else [])
            book_key = st.selectbox("Select Book", options=list(book_options.keys()) if book_options else [])
            days = st.number_input("Borrowing Period (Days)", min_value=1, value=14)
            
            submitted = st.form_submit_button("Borrow Book")
            
            if submitted:
                if not user_key or not book_key:
                    st.error("Please select both a user and a book.")
                else:
                    payload = {
                        "user_id": user_options[user_key],
                        "book_id": book_options[book_key],
                        "borrowing_period_days": days
                    }
                    if api.post("borrowing/", payload):
                        st.success("Book borrowed successfully!")
                        st.rerun()

    with tab2:
        st.subheader("Return a Book")
        
        # Select user to filter active loans
        return_user_key = st.selectbox("Select User to Return For", options=list(user_options.keys()) if user_options else [], key="return_user_select")
        
        if return_user_key:
            user_id = user_options[return_user_key]
            active_loans = api.get(f"borrowing/user/{user_id}")
            
            if active_loans:
                # Filter client-side for "Active" status just in case endpoint returns history too
                active_loans = [l for l in active_loans if l['status'] == 'Active']
                
                if not active_loans:
                    st.info("No active loans for this user.")
                else:
                    for loan in active_loans:
                        # Find book title for display
                        book_title = "Unknown Book"
                        # We might need to fetch book details or if loan object has it.
                        # The API response model 'Borrowing' usually has just IDs unless populated.
                        # Let's check schema.. Usually just IDs.
                        # For better UX, we could fetch book info, but let's stick to IDs/Dates for mvp speed or map from existing loaded books.
                        b_id = loan['book_id']
                        # Try to find in loaded books list (even if 0 qty)
                        # We only loaded available books above. Better fetch all books for title lookup.
                        all_books = api.get("books/?limit=1000") # Optimistic
                        book_map = {b['id']: b['title'] for b in all_books} if all_books else {}
                        book_title = book_map.get(b_id, f"Book ID: {b_id}")

                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.write(f"**{book_title}**")
                            st.caption(f"Borrowed: {loan['borrowed_at'][:10]} | Due: {loan['due_date'][:10]}")
                        with col3:
                            if st.button("Return", key=loan['id']):
                                if api.put(f"borrowing/{loan['id']}/return"):
                                    st.success("Returned successfully!")
                                    st.rerun()
                        st.divider()
            else:
                st.info("No active loans found.")
