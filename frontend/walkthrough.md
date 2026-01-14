# 🚶 Frontend Walkthrough

This guide provides a step-by-step walkthrough of the Library Management System frontend features.

## 🏁 Pre-requisites
1.  **Backend Running**: Ensure `uvicorn app.main:app --reload` is running.
2.  **Frontend Running**: Ensure `streamlit run main.py` is running.
3.  **Open Browser**: Go to `http://localhost:8501`.

## 1. 🗂️ Managing Sections
*Before adding books, it's best to organize your library into sections.*

1.  Navigate to **Sections** in the sidebar.
2.  **Create a Section**:
    *   Click the **Add Section** tab.
    *   Enter a name (e.g., "Science Fiction") and a description.
    *   Click "Create Section".
    *   ✅ *Verify*: A green success message appears.
3.  **View & Delete**:
    *   Switch to the **View Sections** tab to see your list.
    *   To remove one, select it from the "Delete Section" dropdown and click "Delete".

## 2. 📚 Managing Books
1.  Navigate to **Books**.
2.  **Add a Book**:
    *   Go to the **Add Book** tab.
    *   Fill in details (Title, Author, ISBN, Year).
    *   **Important**: Select the "Section" you created in step 1.
    *   Click "Add Book".
    *   ✅ *Verify*: Success message appears.
3.  **Inventory & Deletion**:
    *   Go to **View Books**.
    *   See the list of books and their availability.
    *   To delete, scroll down to the "Delete Book" section, select a book, and click Delete.
    *   *Note*: The system will prevent you from deleting a book if it is currently borrowed.

## 3. 👤 User Registration
1.  Navigate to **Users**.
2.  **Register**:
    *   Go to **Register User**.
    *   Enter Full Name, Email, and Employee ID.
    *   Click "Register User".
3.  **View**: Check the **View Users** tab to confirm registration.

## 4. 🔄 Borrowing & Returning (The Core Flow)
1.  Navigate to **Borrow/Return**.
2.  **Issue a Book**:
    *   In **Borrow Book** tab, select a User and a Book.
    *   Set the number of days (e.g., 7).
    *   Click "Borrow Book".
    *   ✅ *Verify*: Book availability decreases in the Inventory.
3.  **Return a Book**:
    *   Switch to **Return Book** tab.
    *   Select the User who has the book.
    *   The system will show their **Active Loans**.
    *   Click "Return" next to the book title.
    *   ✅ *Verify*: If overdue, a fine is automatically generated.

## 5. 💰 Managing Fines
1.  Navigate to **Fines**.
2.  Select a User.
3.  View basic information about any **Pending** or **Paid** fines.
4.  If they have pending fines, click the **Pay** button to settle the account.
