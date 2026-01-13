def test_create_section(client):
    response = client.post(
        "/api/v1/sections/",
        json={"name": "Fiction", "description": "Story books"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Fiction"
    assert "id" in data

def test_read_sections(client):
    # Ensure previous test data persists if session scope is correct or recreate
    # Here using fresh function scope session, so need to recreate if not using session fixture for data
    # But for isolation better to create fresh
    client.post("/api/v1/sections/", json={"name": "Non-Fiction"})
    
    response = client.get("/api/v1/sections/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
