from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.lang import Builder
import requests

# Puedes definir el diseño de cada ítem en la lista aquí
Builder.load_string('''
<RVLabel>:
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y: None
    height: '40dp'
    text_size: self.size
    valign: 'middle'
    halign: 'center'
''')

class RVLabel(RecycleDataViewBehavior, Label):
    """Etiqueta reutilizable para cada elemento del carrito."""
    pass


class CarritoRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(CarritoRecycleView, self).__init__(**kwargs)
        self.viewclass = 'RVLabel'
        self.data = []


class CarritoScreen(Screen):
    def __init__(self, **kwargs):
        super(CarritoScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título
        self.layout.add_widget(Label(text='🛒 Carrito de Compras', font_size='20sp', size_hint_y=None, height=40))

        # RecycleView que mostrará los productos
        self.rv = CarritoRecycleView()
        self.layout.add_widget(self.rv)

        # Botón para finalizar compra
        self.checkout_button = Button(text='Finalizar Compra', size_hint_y=None, height=50)
        self.checkout_button.bind(on_press=self.finalizar_compra)
        self.layout.add_widget(self.checkout_button)

        self.add_widget(self.layout)

        self.cart_items = []  # Lista de productos del carrito

    def agregar_producto(self, producto):
        """Agrega un producto al carrito y actualiza la vista."""
        self.cart_items.append(producto)
        self.rv.data = [{'text': str(p)} for p in self.cart_items]

    def finalizar_compra(self, instance):
        """Ejemplo básico de llamada al backend."""
        try:
            response = requests.post('http://<backend-url>/checkout', json={'items': self.cart_items})
            if response.status_code == 200:
                print("✅ Compra finalizada con éxito")
            else:
                print(f"❌ Error al finalizar la compra: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error de conexión: {e}")
