from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_hex():
    response = client.get("/hex", headers={"parent_hex": "8a2a1072b59ffff"})
    assert response.status_code == 200
