## Library API Walkthrough
## Values Delivered:

Layered Architecture: Implemented a robust Router -> Service -> Repository -> Model pattern.
No Authorization: As requested, the API is open for easy internal usage and testing.
Core Features: Book management, User management, Borrowing with fine calculation, and Section management.
🚀 How to Run
Activate Virtual Environment:

.\venv\Scripts\activate
Start the Server:

uvicorn app.main:app --reload
Access Documentation: Open http://127.0.0.1:8000/docs to see the interactive Swagger UI.

🧪 Verification Steps
1. Create a Section
POST /api/v1/sections/

{
  "name": "Science Fiction",
  "description": "Sci-Fi Books"
}
2. Create a Book
POST /api/v1/books/

{
  "title": "Dune",
  "author": "Frank Herbert",
  "isbn": "978-0441013593",
  "publication_year": 1965,
  "section_id": 1,
  "quantity": 5
}
3. Create a User (Librarian)
POST /api/v1/users/

{
  "name": "John Doe",
  "email": "john@library.com",
  "employee_id": "LIB001"
}
4. Borrow a Book
POST /api/v1/borrowing/

{
  "book_id": "Use UUID from Step 2",
  "user_id": "Use UUID from Step 3",
  "borrowing_period_days": 14
}
5. Return a Book (Check Fines)
PUT /api/v1/borrowing/{borrowing_id}/return

If returned late (simulated by borrowing with negative days or waiting), a fine will be generated automatically.