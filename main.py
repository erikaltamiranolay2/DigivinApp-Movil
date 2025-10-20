from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# Importar tus pantallas personalizadas
from screens.mostrar_productos_screen import MostrarProductosScreen
from screens.carrito_screen import CarritoScreen
from screens.login_cliente_screen import LoginClienteScreen
from screens.registro_cliente_screen import RegistroClienteScreen
from screens.pago_screen import PagoScreen

# Globales
from globales import get_usuario

KV = """
ScreenManager:
    id: screen_manager

    MostrarProductosScreen:
        name: "productos_screen"

    CarritoScreen:
        name: "carrito_screen"

    LoginClienteScreen:
        name: "login_cliente_screen"

    PagoScreen:
        name: "pago_screen"
"""

class MainApp(MDApp):
    def build(self):
        self.title = "Licorería App"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        self.sm = Builder.load_string(KV)

        # Crear manualmente las pantallas
        self.sm.add_widget(MostrarProductosScreen(name="productos_screen"))
        self.sm.add_widget(CarritoScreen(name="carrito_screen"))
        self.sm.add_widget(LoginClienteScreen(name="login_cliente_screen"))
        self.sm.add_widget(RegistroClienteScreen(name="registro_cliente_screen"))
        self.sm.add_widget(PagoScreen(name="pago_screen"))

        # Pantalla inicial
        return self.sm

    def ir_a_carrito(self):
        """Abre la pantalla del carrito"""
        self.sm.current = "carrito_screen"

    def ir_a_pago(self):
        """Si hay usuario logueado → va a pago, si no → login"""
        usuario = get_usuario()
        if usuario:
            self.sm.current = "pago_screen"
        else:
            self.sm.current = "login_cliente_screen"

    def ir_a_productos(self):
        """Regresa a la pantalla principal"""
        self.sm.current = "productos_screen"


if __name__ == "__main__":
    MainApp().run()
