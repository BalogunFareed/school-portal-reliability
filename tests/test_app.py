from app.main import app

def test_homepage_loads():
    client = app.test_client()

    response = client.get("/")
    
    assert response.status_code == 200


def test_valid_student_id_returns_student_details():
    client = app.test_client()

    response = client.post("/", data={"student_id": "STU001"})

    assert response.status_code == 200
    assert b"John Doe" in response.data

def test_unknown_student_id_returns_404():
    client = app.test_client()

    response = client.post("/", data={"student_id": "UNKNOWN123"})

    assert response.status_code == 404
    assert b"Student record not found." in response.data