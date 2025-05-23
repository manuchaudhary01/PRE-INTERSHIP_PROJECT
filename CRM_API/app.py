from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

customers = []
INVENTORY_API_URL = "http://localhost:5001/welcome-package"

@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    customer = {
        "id": len(customers) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    customers.append(customer)

    # Sending request to Inventory API
    try:
        response = requests.post(INVENTORY_API_URL, json={"customer_name": customer["name"]})
        if response.status_code != 201:
            raise Exception(f"Inventory error: {response.text}")
    except Exception as e:
        return jsonify({"message": "Customer added, but inventory request failed", "error": str(e)}), 202

    return jsonify({"message": "Customer added and welcome package requested", "customer": customer}), 201

@app.route("/customers", methods=["GET"])
def list_customers():
    return jsonify(customers)

if __name__ == "__main__":
    app.run(port=5000)
