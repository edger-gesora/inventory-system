from app import app
import pytest

@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as client:
    yield client

def test_get_inventory(client):
  res = client.get("/inventory")
  assert res.status_code == 200

def test_add_and_get_item(client):
  payload = {
      "product_name": "Test Milk",
      "brands": "TestBrand",
      "quantity": 5,
      "price": 2.0,
  }
  res = client.post("/inventory", json=payload)
  assert res.status_code == 201
  data = res.get_json()
  item_id = data["id"]

  res_single = client.get(f"/inventory/{item_id}")
  assert res_single.status_code == 200
  assert res_single.get_json()["product_name"] == "Test Milk"