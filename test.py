from fastapi.testclient import TestClient
from hello import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "This is the main page!"


def test_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []
