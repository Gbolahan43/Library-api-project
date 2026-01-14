# Library API Project

## 📖 Executive Overview

**Library-Api** is a RESTful backend service designed to manage a comprehensive library system. It enables librarians to efficiently manage book inventory, track book borrowing, manage user accounts, calculate overdue fines, and organize books by sections. The API provides a robust foundation for a complete library management system.

## 🛠️ Technology Stack

*   **Framework:** FastAPI
*   **Language:** Python
*   **Database:** PostgreSQL (Production), SQLite (Development)
*   **ORM:** SQLAlchemy
*   **Schema Validation:** Pydantic
*   **Migrations:** Alembic

## 📂 Project Architecture

The project follows a layered architecture to separate concerns and improve maintainability:

```text
app/
├── api/v1/endpoints/    # Layer 1: HTTP handlers
│   ├── books.py
│   ├── borrowing.py
│   ├── users.py
│   ├── fines.py
│   └── sections.py
│
├── services/            # Layer 2: Business rules
│   ├── book_service.py
│   ├── borrowing_service.py  ← Fine calculation here
│   ├── user_service.py
│   └── fine_service.py
│
├── repositories/        # Layer 3: Database queries
│   ├── base.py          ← Generic CRUD
│   ├── book_repository.py
│   └── borrowing_repository.py
│
├── models/              # SQLAlchemy ORM
├── schemas/             # Pydantic validation
└── core/                # Config, database, exceptions

frontend/                # Streamlit UI
├── main.py              # App entry point
├── api_client.py        # Backend connector
└── tabs/                # Feature modules
```

## ✨ Core Functionalities

### 📚 Book Management
*   **Add/Update/Delete Books:** Complete lifecycle management for book records.
*   **Search & Filter:** Retrieve books by ID, section (Sciences, Arts, Social Studies, etc.), or availability.
*   **Inventory Tracking:** Monitor total and available quantities.

### 🗂️ Sections Management
*   **Organization:** Create and manage library sections (e.g., Fiction, Bio-graphy).
*   **Assignment:** Link books to specific sections for better organization.

### 🔄 Borrowing & Returns
*   **Check-out:** Record borrowing transactions with customizable due dates (default 14 days).
*   **Check-in:** Process returns and automatically calculate overdue status.
*   **History:** accurate logs of borrowing history for users and books.

### 👥 User Management (Librarians)
*   **Librarian Accounts:** Register and manage librarian profiles.
*   **Activity Tracking:** Link actions (borrowing, fines) to specific users.

### 💰 Fine Management
*   **Automatic Calculation:** Fines calculated automatically for overdue items (Default: 50 currency units/day).
*   **Tracking:** Status management for fines (Pending, Paid, Waived).

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   PostgreSQL (optional if using SQLite)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd Library-api-project
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Unix/MacOS
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: To run the frontend, ensure you also install streamlit:*
    ```bash
    pip install streamlit pandas requests
    ```

### Configuration

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=sqlite:///./library.db
# For PostgreSQL use: postgresql://user:password@localhost:5432/library_db
JWT_SECRET_KEY=your-secret-key-here
FINE_RATE_PER_DAY=50
DEFAULT_BORROWING_PERIOD=14
API_VERSION=v1
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Running the Application

You need to run both the backend (API) and the frontend (UI).

**1. Start the Backend Server:**

```bash
uvicorn app.main:app --reload
```
*API Docs available at: `http://127.0.0.1:8000/docs`*

**2. Start the Frontend Interface (New Terminal):**

```bash
cd frontend
streamlit run main.py
```
*UI accessible at: `http://localhost:8501`*

## 📡 API Endpoints Overview

| Category | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Books** | POST | `/api/v1/books` | Add a new book |
| | GET | `/api/v1/books` | List all books |
| | GET | `/api/v1/books/available` | List available books |
| **Borrowing** | POST | `/api/v1/borrowing` | Borrow a book |
| | PUT | `/api/v1/borrowing/{id}/return` | Return a book |
| **Users** | POST | `/api/v1/users` | Create librarian account |
| | GET | `/api/v1/users/{id}` | Get user details |
| **Fines** | GET | `/api/v1/fines` | List fines |
| | PUT | `/api/v1/fines/{id}/pay` | Pay a fine |

*(See `library-api-spec.md` for full specification)*

## 🧪 Testing

Run tests using `pytest` (ensure you have it installed):

```bash
pytest
```

## 📄 License

[MIT License](LICENSE) (or appropriate license)
