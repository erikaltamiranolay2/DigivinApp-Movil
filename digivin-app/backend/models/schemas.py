from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class Customer(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterCustomerRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    password: str

class RegisterCustomerResponse(BaseModel):
    id: int
    name: str
    email: str

class ProductsResponse(BaseModel):
    products: List[Product]