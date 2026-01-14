# 📚 Library System Frontend

A user-friendly, web-based interface for the Library API, built with [Streamlit](https://streamlit.io/). This frontend allows librarians to manage books, users, sections, loans, and fines without interacting directly with raw API endpoints.

## 🛠️ Features

The application is divided into several modules (tabs):

*   **🏠 Home:** Dashboard overview and navigation guide.
*   **📖 Books:**
    *   **Inventory:** View all books with real-time availability and quantity.
    *   **Add Book:** Register new books into the system, assigning them to sections.
    *   **Delete Book:** Remove books from inventory (safeguarded against deleting borrowed books).
*   **🗂️ Sections:**
    *   **Manage:** Create and delete library sections (e.g., Fiction, Science, History).
    *   **View:** List all available sections.
*   **👤 Users:**
    *   **Directory:** View registered library members/staff.
    *   **Registration:** Add new users to the system.
*   **🔄 Borrowing & Returns:**
    *   **Issue Book:** Checkout process with dynamic user/book selection and customizable duration.
    *   **Return Book:** streamlined return process showing active loans for selected users.
*   **💰 Fines:**
    *   **Track:** View overdue fines.
    *   **Pay:** Process fine payments with immediate status updates.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   The Backend API must be running (normally at `http://127.0.0.1:8000`).

### Installation

1.  Navigate to the project root directory.
2.  Ensure your virtual environment is active.
3.  Install the required frontend dependencies:
    ```bash
    pip install streamlit pandas requests
    ```

### Configuration

The frontend communicates with the backend via the `APIClient`.
By default, it connects to: `http://127.0.0.1:8000/api/v1`

If your backend is running on a different port or host, update `frontend/api_client.py`:
```python
API_BASE_URL = "http://your-backend-url:port/api/v1"
```

### Running the Application

To start the frontend interface:

```bash
cd frontend
streamlit run main.py
```

This will automatically open the application in your default web browser (typically at `http://localhost:8501`).

## 📂 Project Structure

```text
frontend/
├── main.py          # Entry point (Navigation & Layout)
├── api_client.py    # API wrapper for HTTP requests
└── tabs/            # Feature modules
    ├── books.py     # Book inventory & management
    ├── borrowing.py # Loan processing
    ├── fines.py     # Fine tracking & payment
    ├── sections.py  # Section management
    └── users.py     # User registration & list
```

## ⚠️ Troubleshooting

*   **Connection Error:** Ensure the Backend API is running (`uvicorn app.main:app --reload`) before starting the frontend.
*   **API Errors:** Check the backend console logs for detailed error messages if an action fails (e.g., 500 Internal Server Error).
