from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

app = Flask(__name__)

# Swagger Configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Inventory-API",
        "description": "API for managing welcome packages",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
}
Swagger(app, template=swagger_template)

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:5432/INVENTORY_DATA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Package model
class Package(db.Model):
    __tablename__ = 'packages'
    package_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "package_id": self.package_id,
            "customer_name": self.customer_name,
            "status": self.status
        }

@app.route("/welcome-package", methods=["POST"])
@swag_from({
    'tags': ['Packages'],
    'description': 'Create a welcome package for a customer.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_name': {'type': 'string'}
                },
                'required': ['customer_name']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Package created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'package_id': {'type': 'integer'},
                    'customer_name': {'type': 'string'},
                    'status': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Customer name is required'
        }
    }
})
def create_package():
    data = request.get_json()
    if not data or "customer_name" not in data:
        return jsonify({"error": "Customer name is required"}), 400

    new_package = Package(customer_name=data["customer_name"], status="dispatched")
    db.session.add(new_package)
    db.session.commit()

    return jsonify(new_package.to_dict()), 201

@app.route("/packages", methods=["GET"])
@swag_from({
    'tags': ['Packages'],
    'description': 'Get list of all packages.',
    'responses': {
        200: {
            'description': 'List of all packages',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'package_id': {'type': 'integer'},
                        'customer_name': {'type': 'string'},
                        'status': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def list_packages():
    all_packages = Package.query.all()
    return jsonify([pkg.to_dict() for pkg in all_packages]), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001)
