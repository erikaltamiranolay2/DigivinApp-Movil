from flask import Blueprint, request, jsonify
from backend.services.oracle_client import OracleClient

auth_bp = Blueprint('auth', __name__)
oracle_client = OracleClient()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = oracle_client.verify_login(username, password)
    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'error': 'Username, password, and email are required'}), 400

    success = oracle_client.insert_cliente(username, password, email)
    if success:
        return jsonify({'message': 'Registration successful'}), 201
    else:
        return jsonify({'error': 'Registration failed'}), 500