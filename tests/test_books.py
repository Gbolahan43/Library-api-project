def test_create_book(client):
    # Create section first
    s_resp = client.post("/api/v1/sections/", json={"name": "SciFi"})
    section_id = s_resp.json()["id"]

    response = client.post(
        "/api/v1/books/",
        json={
            "title": "Dune",
            "author": "Frank Herbert",
            "isbn": "978-0441013593",
            "publication_year": 1965,
            "section_id": section_id,
            "quantity": 5
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Dune"
    assert data["available_quantity"] == 5

def test_read_books(client):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
