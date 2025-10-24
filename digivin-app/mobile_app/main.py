from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Import screens
from screens.login_screen import LoginScreen
from screens.mostrar_productos_screen import MostrarProductosScreen
from screens.carrito_screen import CarritoScreen

# Load the KV file
Builder.load_file('kv/app.kv')

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MostrarProductosScreen(name='mostrar_productos'))
        sm.add_widget(CarritoScreen(name='carrito'))
        return sm

if __name__ == '__main__':
    MainApp().run()