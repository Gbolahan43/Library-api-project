## Library API & Frontend Walkthrough
## Values Delivered:

- **Layered Architecture**: Implemented a robust Router -> Service -> Repository -> Model pattern.
- **No Authorization**: As requested, the API is open for easy internal usage and testing.
- **Core Features**: Book management, User management, Borrowing with fine calculation, and Section management.
- **Automated Tests**: Full test suite included using `pytest`.
- **Frontend**: A user-friendly Streamlit interface for managing the library.

## 🚀 How to Run

1.  **Activate Virtual Environment**:
    ```bash
    .\libraryenv\Scripts\activate
    ```

2.  **Start the Backend Server**:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    *Access API Docs:* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3.  **Start the Frontend App**:
    Open a new terminal, activate the environment, and run:
    ```bash
    streamlit run frontend/main.py
    ```
    *Access App:* Usually http://localhost:8501

## 🧪 Verification Steps

### Automated Tests
Run the full test suite to verify all functionality automatically:
```bash
pytest tests/
```

### Manual Verification (Frontend)
1.  **Register a User**: usage the **Users** tab.
2.  **Add a Book**: use the **Books** tab.
3.  **Borrow**: Go to **Borrow/Return**, select the user and book.
4.  **Confirm**: Check **Books** tab to see quantity decrease.
5.  **Return**: Go to **Borrow/Return** -> Return Book tab.