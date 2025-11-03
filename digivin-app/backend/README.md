# Backend Application Documentation

## Overview

The backend of the Digivin App is built using Flask and serves as the API for the mobile application. It provides endpoints for user authentication, product management, and customer operations. This README outlines the setup instructions, API usage, and other relevant information for developers working on the backend.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd digivin-app/backend
   ```

2. **Create a Virtual Environment**
   It is recommended to use a virtual environment to manage dependencies.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements**
   Install the necessary packages using pip.
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Copy the `.env.sample` file to `.env` and update the values as needed.
   ```bash
   cp .env.sample .env
   ```

5. **Run the Application**
   Start the Flask application.
   ```bash
   python app.py
   ```

## API Endpoints

### Authentication

- **Login**
  - **Endpoint:** `/api/auth/login`
  - **Method:** POST
  - **Request Body:**
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response:**
    - **200 OK:** Returns user information and a token.
    - **401 Unauthorized:** Invalid credentials.

### Products

- **Get Products**
  - **Endpoint:** `/api/products`
  - **Method:** GET
  - **Response:**
    - **200 OK:** Returns a list of products.

### Customers

- **Register Customer**
  - **Endpoint:** `/api/customers`
  - **Method:** POST
  - **Request Body:**
    ```json
    {
      "name": "string",
      "email": "string",
      "phone": "string"
    }
    ```
  - **Response:**
    - **201 Created:** Returns the created customer information.

## Additional Information

- Ensure that the Oracle database is accessible and the connection details are correctly configured in the `.env` file.
- For further details on the API request and response formats, refer to the `docs/api.md` file.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.