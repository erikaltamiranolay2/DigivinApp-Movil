from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
import requests

class CarritoScreen(Screen):
    def __init__(self, **kwargs):
        super(CarritoScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        self.cart_items = []  # List to hold cart items
        self.list_view = ListView(item_strings=self.cart_items)
        
        self.layout.add_widget(Label(text='Carrito de Compras'))
        self.layout.add_widget(self.list_view)
        
        self.checkout_button = Button(text='Finalizar Compra')
        self.checkout_button.bind(on_press=self.finalizar_compra)
        self.layout.add_widget(self.checkout_button)
        
        self.add_widget(self.layout)

    def agregar_producto(self, producto):
        self.cart_items.append(producto)
        self.list_view.item_strings = self.cart_items

    def finalizar_compra(self, instance):
        # Implementar la lógica para finalizar la compra
        response = requests.post('http://<backend-url>/checkout', json={'items': self.cart_items})
        if response.status_code == 200:
            print("Compra finalizada con éxito")
        else:
            print("Error al finalizar la compra")