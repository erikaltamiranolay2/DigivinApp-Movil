class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        response = requests.post(f"{self.base_url}/auth/login", json={"username": username, "password": password})
        return response.json()

    def fetch_products(self):
        response = requests.get(f"{self.base_url}/products")
        return response.json()

    def register_customer(self, customer_data):
        response = requests.post(f"{self.base_url}/customers", json=customer_data)
        return response.json()