from fastapi.testclient import TestClient
from tickets.main import app

client = TestClient(app)


def test_labels():
    assert client.post("/classify", json={"text": 'Cannot login with SSO'}).json()["label"] == "access"
    assert client.post("/classify", json={"text": 'The API is down with 500s'}).json()["label"] == "outage"


def test_empty_is_refused():
    assert client.post("/classify", json={"text": "  "}).status_code == 422
