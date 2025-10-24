# ...existing code...
from flask import Blueprint, request, jsonify
from backend.services.oracle_client import OracleClient

customers_bp = Blueprint('customers', __name__)
oracle_client = OracleClient()

@customers_bp.route('/', methods=['POST'])
def register_customer():
    data = request.json
    # validación básica
    if not data.get('name') or not data.get('email'):
        return jsonify({"error": "name and email required"}), 400
    try:
        oracle_client.insert_customer(data)  # implementa insert_customer en OracleClient
        return jsonify({"message": "Customer registered successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customers_bp.route('/login', methods=['POST'])
def verify_login():
    data = request.json
    username = data.get('username') or data.get('email')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400
    try:
        user = oracle_client.verify_login(username, password)  # implementa verify_login en OracleClient
        if user:
            return jsonify({"message": "Login successful.", "user": user}), 200
        else:
            return jsonify({"error": "Invalid credentials."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ...existing code...