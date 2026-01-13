def test_fine_generation(client):
    # Setup Data
    s = client.post("/api/v1/sections/", json={"name": "Art"}).json()
    b = client.post("/api/v1/books/", json={
        "title": "Art History", "author": "Gombrich", "isbn": "112233", 
        "publication_year": 1950, "section_id": s["id"], "quantity": 1
    }).json()
    u = client.post("/api/v1/users/", json={
        "name": "Late Caller", "email": "late@test.com", "employee_id": "LATE001"
    }).json()

    # Borrow with negative period to force overdue upon return?
    # Logic in service uses borrowing_period_days to calc due_date = now + days
    # So if we pass -5 days, due_date is 5 days ago.
    borrow_resp = client.post(
        "/api/v1/borrowing/",
        json={"book_id": b["id"], "user_id": u["id"], "borrowing_period_days": -5}
    )
    borrowing_id = borrow_resp.json()["id"]

    # Return immediate
    response = client.put(f"/api/v1/borrowing/{borrowing_id}/return")
    assert response.status_code == 200
    data = response.json()
    
    # Expect Overdue status and fine generation
    assert data["status"] == "Overdue"
    
    # Check Fine
    fines = client.get(f"/api/v1/fines/?user_id={u['id']}").json()
    assert len(fines) > 0
    assert fines[0]["amount"] > 0
    assert fines[0]["status"] == "Pending"
