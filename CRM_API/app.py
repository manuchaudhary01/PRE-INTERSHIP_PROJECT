from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
import requests

app = Flask(__name__)
Swagger(app)  # Swagger UI available at /apidocs

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:5432/CRM_DATA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Customer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

# Inventory API URL
INVENTORY_API_URL = "http://localhost:5001/welcome-package"

@app.route("/customers", methods=["POST"])
@swag_from({
    'tags': ['Customers'],
    'description': 'Add a new customer and send a welcome package request to Inventory API.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                },
                'required': ['name', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Customer added and welcome package requested'
        },
        202: {
            'description': 'Customer added, but inventory request failed'
        },
        400: {
            'description': 'Invalid request, name and email are required'
        }
    }
})
def add_customer():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    new_customer = Customer(name=data["name"], email=data["email"])
    db.session.add(new_customer)
    db.session.commit()

    try:
        response = requests.post(INVENTORY_API_URL, json={"customer_name": new_customer.name})
        if response.status_code != 201:
            raise Exception(f"Inventory error: {response.text}")
    except Exception as e:
        return jsonify({
            "message": "Customer added, but inventory request failed",
            "error": str(e),
            "customer": new_customer.to_dict()
        }), 202

    return jsonify({
        "message": "Customer added and welcome package requested",
        "customer": new_customer.to_dict()
    }), 201

@app.route("/customers", methods=["GET"])
@swag_from({
    'tags': ['Customers'],
    'description': 'Retrieve a list of all customers.',
    'responses': {
        200: {
            'description': 'List of customers',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_customers():
    all_customers = Customer.query.all()
    return jsonify([cust.to_dict() for cust in all_customers]), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000)
