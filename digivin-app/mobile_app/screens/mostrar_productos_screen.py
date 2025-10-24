# ...existing code...
import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest

class MostrarProductosScreen(Screen):
    def __init__(self, **kwargs):
        super(MostrarProductosScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.scroll_view = ScrollView()
        self.product_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.product_list.bind(minimum_height=self.product_list.setter('height'))
        self.scroll_view.add_widget(self.product_list)
        self.layout.add_widget(self.scroll_view)

        # botón Back creado una sola vez
        back_button = Button(text='Back', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)
        self.load_products()

    def load_products(self):
        backend = os.getenv("BACKEND_URL", "http://10.0.2.2:5000")  # ajustar según entorno
        url = f"{backend}/api/products"
        # UrlRequest hace la llamada async y evita bloquear UI
        UrlRequest(url, on_success=self.on_products_received, on_error=self.on_products_error, on_failure=self.on_products_error, timeout=10)

    def on_products_received(self, request, result):
        # result ya puede ser un objeto python si la respuesta es JSON
        try:
            if isinstance(result, (bytes, bytearray)):
                data = json.loads(result.decode("utf-8"))
            else:
                data = result
            # soportar formato {"ok": True, "products": [...]}
            if isinstance(data, dict) and data.get("ok") and "products" in data:
                products = data["products"]
            elif isinstance(data, list):
                products = data
            else:
                products = []
        except Exception:
            products = []

        self.product_list.clear_widgets()
        if not products:
            self.product_list.add_widget(Label(text="No hay productos", size_hint_y=None, height=40))
            return

        for product in products:
            name = product.get("name") or product.get("nombre", "Sin nombre")
            price = product.get("price") or product.get("precio") or 0
            product_label = Label(text=f"{name} - ${price}", size_hint_y=None, height=40)
            self.product_list.add_widget(product_label)

    def on_products_error(self, request, error):
        self.product_list.clear_widgets()
        self.product_list.add_widget(Label(text="Error al cargar productos", size_hint_y=None, height=40))

    def go_back(self, instance):
        # Ajusta el nombre de la pantalla destino si es diferente
        self.manager.current = 'login'
# ...existing code...