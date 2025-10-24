from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.products import products_bp
from routes.customers import customers_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints for different routes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(customers_bp, url_prefix='/api/customers')

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode for development
