from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestMain:
    def test_root(self):
        """Should return some simple text"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.text == "This is the main page!"

    def test_items(self):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []

    def test_items_paginated(self):
        response1 = client.get("/items").json()
        assert response1 == []

        client.post("/items")
        client.post("/items")
        client.post("/items")
        client.post("/items")
        client.post("/items")

        items: list[str] = client.get("/items?page=1&size=2").json()
        assert len(items) == 2
        assert items[0] == "NEW ITEM!"

        items: list[str] = client.get("/items?page=2&size=3").json()
        assert len(items) == 2
        assert items[0] == "NEW ITEM!"
