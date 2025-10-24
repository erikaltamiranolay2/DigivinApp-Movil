# API Documentation

## Overview
This document provides an overview of the API endpoints available for the Digivin App backend. The API is built using Flask and allows the mobile application to perform various operations such as user authentication, product retrieval, and customer registration.

## Base URL
The base URL for the API is:
```
http://<your-server-address>:<port>
```

## Endpoints

### Authentication

#### Login
- **Endpoint:** `/api/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  - **200 OK**
    ```json
    {
      "token": "string",
      "message": "Login successful"
    }
    ```
  - **401 Unauthorized**
    ```json
    {
      "message": "Invalid credentials"
    }
    ```

### Products

#### Get Products
- **Endpoint:** `/api/products`
- **Method:** `GET`
- **Response:**
  - **200 OK**
    ```json
    [
      {
        "id": "integer",
        "name": "string",
        "price": "float",
        "description": "string"
      }
    ]
    ```

### Customers

#### Register Customer
- **Endpoint:** `/api/customers`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "name": "string",
    "email": "string",
    "phone": "string"
  }
  ```
- **Response:**
  - **201 Created**
    ```json
    {
      "message": "Customer registered successfully"
    }
    ```
  - **400 Bad Request**
    ```json
    {
      "message": "Invalid input data"
    }
    ```

## Error Handling
All error responses will have a standard format:
```json
{
  "message": "error description"
}
```

## Notes
- Ensure to include the authentication token in the headers for protected routes.
- The API is designed to be stateless; each request must contain all the information needed to process it.