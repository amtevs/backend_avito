import pytest
from fastapi.testclient import TestClient

import routers.users as users
from main import app

client = TestClient(app)

PAYLOAD = {
    "seller_id": 1,
    "is_verified_seller": False,
    "item_id": 101,
    "name": "Стул",
    "description": "Деревянный стул",
    "category": 5,
    "images_qty": 1,
}


def test_violation_found():
    response = client.post(
        "/predict",
        json={**PAYLOAD, "images_qty": 0},
    )
    assert response.status_code == 200
    assert response.json() is True


def test_no_violation_found():
    response = client.post("/predict", json=PAYLOAD)
    assert response.status_code == 200
    assert response.json() is False


def test_missing_required_field():
    payload = PAYLOAD.copy()
    del payload["seller_id"]
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_wrong_field_type():
    payload = {**PAYLOAD, "seller_id": "не число"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_business_logic_error(monkeypatch):
    def raise_error(**kwargs):
        raise RuntimeError("test error")

    monkeypatch.setattr(users, "predict_violation", raise_error)
    response = client.post("/predict", json=PAYLOAD)
    assert response.status_code == 500