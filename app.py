from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock database array storing inventory items with IDs[cite: 4, 6]
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "quantity": 10,
        "price": 3.50,
    }
]

@app.route("/inventory", methods=["GET"])
def get_inventory():
  return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
  item = next((item for item in inventory if item["id"] == item_id), None)
  if item is None:
    return jsonify({"error": "Item not found"}), 404
  return jsonify(item), 200

# POST /inventory -> Add a new item
@app.route("/inventory", methods=["POST"])
def add_item():
  data = request.get_json()
  if not data or "product_name" not in data:
    return jsonify({"error": "Invalid input, product_name required"}), 400

  new_item = {
      "id": len(inventory) + 1 if not inventory else inventory[-1]["id"] + 1,
      "product_name": data.get("product_name"),
      "brands": data.get("brands", "Unknown"),
      "quantity": data.get("quantity", 0),
      "price": data.get("price", 0.0),
  }
  inventory.append(new_item)
  return jsonify(new_item), 201

# PATCH /inventory/<id> -> Update an item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
  item = next((item for item in inventory if item["id"] == item_id), None)
  if item is None:
    return jsonify({"error": "Item not found"}), 404

  data = request.get_json()
  if "quantity" in data:
    item["quantity"] = data["quantity"]
  if "price" in data:
    item["price"] = data["price"]
  if "product_name" in data:
    item["product_name"] = data["product_name"]

  return jsonify(item), 200

# DELETE /inventory/<id> -> Remove an item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
  global inventory
  item = next((item for item in inventory if item["id"] == item_id), None)
  if item is None:
    return jsonify({"error": "Item not found"}), 404

  inventory = [i for i in inventory if i["id"] != item_id]
  return "", 204

# External API Integration: Fetch product details from OpenFoodFacts API[cite: 1, 4, 7]
@app.route("/inventory/external/<barcode>", methods=["GET"])
def fetch_external_product(barcode):
  url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    if data.get("status") == 1:
      prod = data.get("product", {})
      return (
          jsonify({
              "product_name": prod.get("product_name", "Unknown"),
              "brands": prod.get("brands", "Unknown"),
              "ingredients_text": prod.get("ingredients_text", ""),
          }),
          200,
      )
  return jsonify({"error": "Product not found on OpenFoodFacts"}), 404

if __name__ == "__main__":
  app.run(debug=True)