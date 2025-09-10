from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Assuming seeded data, check if not empty
    assert len(response.json()) > 0

def test_checkout_valid():
    response = client.post("/checkout", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert "total" in data
    assert data["total"] == 999.99  # Price of product 1

def test_checkout_invalid_product():
    response = client.post("/checkout", json={"product_id": 999, "quantity": 1})
    assert response.status_code == 404
    assert "Product not found" in response.json()["detail"]

def test_checkout_missing_fields():
    response = client.post("/checkout", json={"product_id": 1})
    assert response.status_code == 400
    assert "product_id and quantity are required" in response.json()["detail"]

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_simulate_error():
    response = client.get("/error")
    assert response.status_code == 500
    assert "Simulated application error" in response.json()["detail"]

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Check if metrics are present
    content = response.text
    assert "http_requests_total" in content
    assert "http_request_duration_seconds" in content
    assert "http_errors_total" in content
