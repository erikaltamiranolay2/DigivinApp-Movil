from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from database.queries import verificar_login
from globales import set_usuario


class LoginClienteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        # --- BOTÓN DE VOLVER ---
        btn_volver = MDIconButton(
            icon="arrow-left",
            icon_size=dp(28),
            theme_icon_color="Custom",
            icon_color=(0, 0, 0, 1),
            pos_hint={"x": 0.02, "top": 0.98},
            on_release=lambda _: self.ir_a_productos(),
        )
        root.add_widget(btn_volver)

        # --- CONTENEDOR CENTRAL ---
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(40), dp(10), dp(40), dp(10)],
            size_hint=(0.9, None),
            height=dp(420),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
        )

        # --- TÍTULO CON ICONO ---
        titulo_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint=(None, None),
            size=(dp(230), dp(50)),
            pos_hint={"center_x": 0.5},
        )

        icon = MDIconButton(
            icon="account",
            icon_size=dp(26),
            theme_icon_color="Custom",
            icon_color=(0, 0, 0, 1),
            md_bg_color=(0, 0, 0, 0),
            padding=0,
        )

        titulo = MDLabel(
            text="Iniciar sesión",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(None, 1),
            width=dp(150),
        )

        titulo_layout.add_widget(icon)
        titulo_layout.add_widget(titulo)
        layout.add_widget(titulo_layout)

        # --- CAMPOS ---
        self.txt_email = MDTextField(
            hint_text="Correo electrónico",
            mode="rectangle",
            size_hint_x=1,
            font_size=dp(14),
        )
        self.txt_password = MDTextField(
            hint_text="Contraseña",
            mode="rectangle",
            password=True,
            size_hint_x=1,
            font_size=dp(14),
        )
        layout.add_widget(self.txt_email)
        layout.add_widget(self.txt_password)

        # --- BOTÓN INGRESAR ---
        login_button = MDRaisedButton(
            text="Ingresar",
            md_bg_color=(0, 0.5, 1, 1),
            size_hint=(1, None),
            height=dp(50),
        )
        login_button.bind(on_release=self.check_login)
        layout.add_widget(login_button)

        # --- BOTÓN REGISTRARSE ---
        btn_registrar = MDFlatButton(
            text="Registrarse",
            text_color=(0, 0.5, 1, 1),
            size_hint=(1, None),
            height=dp(40),
            on_release=lambda _: setattr(self.manager, "current", "registro_cliente_screen"),
        )
        layout.add_widget(btn_registrar)

        root.add_widget(layout)
        self.add_widget(root)

    def ir_a_productos(self):
        self.manager.current = "productos_screen"

    def check_login(self, *args):
        email = self.txt_email.text.strip()
        password = self.txt_password.text.strip()

        cliente = verificar_login(email, password)
        if cliente:
            set_usuario(cliente)
            toast(f"Bienvenido, {cliente['nombre_completo']} 👋")
            self.manager.current = "productos_screen"
        else:
            toast("Correo o contraseña incorrectos ❌")
