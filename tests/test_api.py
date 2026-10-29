import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def calculate(client, payload):
    return client.post("/api/calculate", json=payload)


def test_division_rounding_and_recovery(client):
    response = calculate(client, {"number": "100", "divisor": "3", "precision": 2})
    assert response.status_code == 200
    data = response.get_json()
    assert data["original"] == "100"
    assert data["display_result"] == "33.33"
    assert data["reverse_result_from_display"] == "99.99"
    assert data["precision_difference"] == "0.01"
    assert data["recovered_result"] == "100"


@pytest.mark.parametrize("payload", [
    {"number": "10", "divisor": "0"},
    {"number": "NaN", "divisor": "2"},
    {"number": "Infinity", "divisor": "2"},
    {"number": "", "divisor": "2"},
    {"number": "1e101", "divisor": "2"},
    {"number": "10", "divisor": "2", "precision": 11},
    {"number": "10", "divisor": "2", "precision": 1.5},
])
def test_invalid_inputs_return_400(client, payload):
    response = calculate(client, payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_non_json_content_type_is_rejected(client):
    response = client.post("/api/calculate", data="number=10&divisor=2")
    assert response.status_code == 415


def test_non_object_json_is_rejected(client):
    response = client.post("/api/calculate", json=["not", "an", "object"])
    assert response.status_code == 400


def test_zero_precision(client):
    response = calculate(client, {"number": "10", "divisor": "3", "precision": 0})
    assert response.status_code == 200
    assert response.get_json()["display_result"] == "3"
