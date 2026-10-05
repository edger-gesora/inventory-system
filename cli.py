import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def main():
  while True:
    print("\n--- Inventory Management CLI ---")
    print("1. View All Inventory")
    print("2. View Item by ID")
    print("3. Add New Item")
    print("4. Update Item")
    print("5. Delete Item")
    print("6. Fetch Product from OpenFoodFacts API")
    print("7. Exit")

    choice = input("Choose an option (1-7): ")

    if choice == "1":
      res = requests.get(BASE_URL)
      print(res.json())

    elif choice == "2":
      item_id = input("Enter Item ID: ")
      res = requests.get(f"{BASE_URL}/{item_id}")
      print(res.json())

    elif choice == "3":
      name = input("Product Name: ")
      brand = input("Brand: ")
      qty = int(input("Quantity: "))
      price = float(input("Price: "))
      payload = {
          "product_name": name,
          "brands": brand,
          "quantity": qty,
          "price": price,
      }
      res = requests.post(BASE_URL, json=payload)
      print("Added successfully:", res.json())

    elif choice == "4":
      item_id = input("Enter Item ID to update: ")
      qty = input("New Quantity (leave blank to skip): ")
      price = input("New Price (leave blank to skip): ")
      payload = {}
      if qty:
        payload["quantity"] = int(qty)
      if price:
        payload["price"] = float(price)
      res = requests.patch(f"{BASE_URL}/{item_id}", json=payload)
      print("Updated successfully:", res.json())

    elif choice == "5":
      item_id = input("Enter Item ID to delete: ")
      res = requests.delete(f"{BASE_URL}/{item_id}")
      if res.status_code == 204:
        print("Item deleted successfully.")
      else:
        print(res.json())

    elif choice == "6":
      barcode = input("Enter Product Barcode (e.g. 737628064502): ")
      res = requests.get(f"{BASE_URL}/external/{barcode}")
      print(res.json())

    elif choice == "7":
      print("Exiting CLI. Goodbye!")
      break
    else:
      print("Invalid choice, try again.")

if __name__ == "__main__":
  main()