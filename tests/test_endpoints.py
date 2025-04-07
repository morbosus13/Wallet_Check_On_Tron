from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.models import Base
from main import app

from unittest.mock import patch

DB_URL = "sqlite://"
engine = create_engine(
    url=DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

Base.metadata.create_all(engine)


client = TestClient(app)


def test_get_data():
    response = client.get("/api/v1/wallets?page=0&size=1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, list)

@patch("httpx.post")
def test_correct_post_data(mock_post):
    wallet_data = {
        "address": "TN7pgdZfPGtfaYjgcCSyazxtByjBQ8Fr8q",
        "balance": 0,
        "bandwidth": 0,
        "energy": {"energy": 0},
    }
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = wallet_data
    data = {
        "address" : wallet_data["address"]
    }
    response = client.post("/api/v1/balance", json=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data["address"] == wallet_data["address"]
    for key in response_data:
        assert key in wallet_data.keys()

@patch("httpx.post")
def test_incorrect_post_data(mock_post):
    wallet_data = {
        "address": "Incorrect address",
        "balance": 0,
        "bandwidth": 0,
        "energy": {"energy": 0},
    }
    data = {
        "address" : wallet_data["address"]
    }
    mock_post.return_value.status_code = 422
    response = client.post("/api/v1/balance", json=data)
    assert response.status_code == 422