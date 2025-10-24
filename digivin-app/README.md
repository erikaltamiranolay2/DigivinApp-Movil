# Digivin App

## Overview
Digivin App is a mobile application designed to facilitate the management of products and customer interactions through a user-friendly interface. The app communicates with a backend server that handles authentication, product management, and customer operations via a RESTful API.

## Project Structure
The project is organized into two main directories: `mobile_app` and `backend`.

### Mobile App
- **main.py**: Entry point of the mobile application, initializes the Kivy app.
- **buildozer.spec**: Configuration file for building the mobile app using Buildozer.
- **screens/**: Contains the UI screens for the app.
  - **login_screen.py**: Handles user login functionality.
  - **mostrar_productos_screen.py**: Displays a list of products fetched from the backend.
  - **carrito_screen.py**: Manages the shopping cart functionality.
- **services/**: Contains classes for interacting with the backend API.
  - **api_client.py**: Responsible for making HTTP requests to the backend.
- **kv/**: Contains Kivy language files for UI layout.
  - **app.kv**: Defines the app's UI layout.
- **requirements.txt**: Lists the required Python packages for the mobile app.
- **.env.sample**: Template for environment variables needed for the mobile app.

### Backend
- **app.py**: Entry point of the backend application, initializes the Flask app and sets up API routes.
- **requirements.txt**: Lists the required Python packages for the backend.
- **routes/**: Contains the API route definitions.
  - **auth.py**: Defines authentication routes, including login.
  - **products.py**: Manages product-related routes.
  - **customers.py**: Handles customer-related operations.
- **services/**: Contains classes for database interactions.
  - **oracle_client.py**: Manages connections to the Oracle database.
- **models/**: Contains data schemas for validating requests and responses.
  - **schemas.py**: Defines the data schemas.
- **.env.sample**: Template for environment variables needed for the backend.
- **README.md**: Documentation for the backend application.

## Setup Instructions

### Mobile App
1. Navigate to the `mobile_app` directory.
2. Install the required packages listed in `requirements.txt` using:
   ```
   pip install -r requirements.txt
   ```
3. Build the app using Buildozer:
   ```
   buildozer -v android debug
   ```

### Backend
1. Navigate to the `backend` directory.
2. Install the required packages listed in `requirements.txt` using:
   ```
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```
   python app.py
   ```

## API Documentation
For detailed information on the API endpoints, request and response formats, refer to the `docs/api.md` file.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.