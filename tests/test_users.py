def test_create_user(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Jane Librarian",
            "email": "jane@library.com",
            "employee_id": "LIB002"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "jane@library.com"
    assert data["role"] == "Librarian"

def test_read_users(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert len(response.json()) >= 0
