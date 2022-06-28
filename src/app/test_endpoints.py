from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_index():
    response = client.get("/")

    print(response.text)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
