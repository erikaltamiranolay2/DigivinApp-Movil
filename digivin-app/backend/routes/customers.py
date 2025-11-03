# ...existing code...
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://<tu-backend-host>:5000/api")

class LoginClienteScreen(Screen):
    # ...existing code...
    def check_login(self, *args):
        email = self.txt_email.text.strip()
        password = self.txt_password.text.strip()

        if not email or not password:
            toast("❗ Completa correo y contraseña")
            return

        try:
            resp = requests.post(f"{BACKEND_URL}/auth/login", json={"username": email, "password": password}, timeout=10)
            if resp.status_code == 200:
                user = resp.json().get("user") or resp.json()
                set_usuario(user)
                toast(f"Bienvenido, {user.get('nombre_completo', user.get('name',''))} 👋")
                self.manager.current = "productos_screen"
            else:
                toast("Correo o contraseña incorrectos ❌")
        except Exception as e:
            toast(f"⚠️ Error red: {e}")
# ...existing code...