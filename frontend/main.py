import streamlit as st
import sys
import os

# Add parent dir to path if needed to find modules, though usually running from root works
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabs import books, users, borrowing, fines

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("📚 Library Management System")

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Go to",
        ["Home", "Books", "Users", "Borrow/Return", "Fines"]
    )

    if selection == "Home":
        st.markdown("""
        ### Welcome to the Library Management System
        
        Use the sidebar to navigate to different modules:
        - **Books**: Manage book inventory (Add, View).
        - **Users**: Manage library members (Add, View).
        - **Borrow/Return**: Issue books and return them.
        - **Fines**: View and manage overdue fines.
        """)
        
    elif selection == "Books":
        books.render()
    
    elif selection == "Users":
        users.render()
        
    elif selection == "Borrow/Return":
        borrowing.render()
        
    elif selection == "Fines":
        fines.render()

if __name__ == "__main__":
    main()
