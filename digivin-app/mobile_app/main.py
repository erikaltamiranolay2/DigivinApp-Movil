from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp  # ✅ usa MDApp, no App

# importa tus pantallas
from screens.login_screen import LoginScreen
from screens.mostrar_productos_screen import MostrarProductosScreen
from screens.carrito_screen import CarritoScreen


class MainApp(MDApp):  # ✅ hereda de MDApp
    def build(self):
        self.title = "Licorería App"  # título de la ventana

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MostrarProductosScreen(name='mostrar_productos'))
        sm.add_widget(CarritoScreen(name='carrito'))

        # 👇 Establecer la pantalla que se muestra al inicio
        sm.current = 'mostrar_productos'

        return sm


if __name__ == '__main__':
    MainApp().run()
