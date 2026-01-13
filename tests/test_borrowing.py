def test_borrow_book(client):
    # Setup Data
    s = client.post("/api/v1/sections/", json={"name": "History"}).json()
    b = client.post("/api/v1/books/", json={
        "title": "Sapiens", "author": "Yuval Noah Harari", "isbn": "12345", 
        "publication_year": 2011, "section_id": s["id"], "quantity": 1
    }).json()
    u = client.post("/api/v1/users/", json={
        "name": "Borrower", "email": "borrower@test.com", "employee_id": "B001"
    }).json()

    # Borrow
    response = client.post(
        "/api/v1/borrowing/",
        json={
            "book_id": b["id"],
            "user_id": u["id"],
            "borrowing_period_days": 7
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "Active"
    
    # Check availability decreased
    b_updated = client.get(f"/api/v1/books/{b['id']}").json()
    assert b_updated["available_quantity"] == 0

def test_return_book(client):
    # Setup (same as above for isolation)
    s = client.post("/api/v1/sections/", json={"name": "Math"}).json()
    b = client.post("/api/v1/books/", json={
        "title": "Calculus", "author": "Stewart", "isbn": "67890", 
        "publication_year": 2015, "section_id": s["id"], "quantity": 1
    }).json()
    u = client.post("/api/v1/users/", json={
        "name": "Math Student", "email": "math@test.com", "employee_id": "B002"
    }).json()
    
    borrow_resp = client.post(
        "/api/v1/borrowing/",
        json={"book_id": b["id"], "user_id": u["id"], "borrowing_period_days": 7}
    )
    borrowing_id = borrow_resp.json()["id"]

    # Return
    response = client.put(f"/api/v1/borrowing/{borrowing_id}/return")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Returned"

    # Check availability restored
    b_updated = client.get(f"/api/v1/books/{b['id']}").json()
    assert b_updated["available_quantity"] == 1
