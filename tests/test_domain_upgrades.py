import pytest
from fastapi.testclient import TestClient
from tickets.main import app

client = TestClient(app)


def test_tied_categories_require_human_review():
    r = client.post("/classify", json={"text": "invoice outage"}).json()
    assert r["needs_review"] is True
    assert r["tied_labels"] == ["billing", "outage"]
    assert r["matched_keywords"]["billing"] == ["invoice"]
    assert r["review_reason"] == "tied categories"


def test_unknown_and_clear_matches_have_distinct_review_status():
    assert client.post("/classify", json={"text": "hello"}).json()["needs_review"] is True
    r = client.post("/classify", json={"text": "login SSO"}).json()
    assert r["needs_review"] is False and r["matched_keywords"]["access"] == ["login", "sso"]


def test_oversized_text_is_rejected():
    assert client.post("/classify", json={"text": "x" * 10001}).status_code == 422
