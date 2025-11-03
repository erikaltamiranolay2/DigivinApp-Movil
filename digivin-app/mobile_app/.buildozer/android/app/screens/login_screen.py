from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import requests
import os

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.verify_login)

        self.layout.add_widget(Label(text='Login', font_size=24))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)

        self.add_widget(self.layout)

    def verify_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        api_url = os.getenv('API_URL') + '/login'

        response = requests.post(api_url, json={'username': username, 'password': password})

        if response.status_code == 200:
            self.show_popup('Success', 'Login successful!')
            # Navigate to the next screen or perform other actions
        else:
            self.show_popup('Error', 'Login failed. Please try again.')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()