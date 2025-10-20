# screens/pago_screen.py
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.floatlayout import FloatLayout
from kivymd.toast import toast
from globales import get_usuario


class PagoScreen(Screen):
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
            on_release=lambda _: self.volver_a_login(),
        )
        root.add_widget(btn_volver)

        # --- CONTENEDOR PRINCIPAL ---
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(40), dp(10), dp(40), dp(10)],
            size_hint=(0.9, None),
            height=dp(420),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # --- TÍTULO ---
        titulo_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            pos_hint={"center_x": 0.5},
        )

        icon = MDIconButton(
            icon="cash",
            icon_size=dp(26),
            theme_icon_color="Custom",
            icon_color=(0, 0.5, 1, 1),
            md_bg_color=(0, 0, 0, 0),
            padding=0,
        )

        self.lbl_usuario = MDLabel(
            text="Bienvenido 👋",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(None, 1),
            width=dp(200),
        )

        titulo_layout.add_widget(icon)
        titulo_layout.add_widget(self.lbl_usuario)
        layout.add_widget(titulo_layout)

        # --- BOTÓN DE PAGO ---
        btn_pagar = MDRaisedButton(
            text="Realizar pago",
            md_bg_color=(0, 0.5, 1, 1),
            size_hint=(1, None),
            height=dp(50),
            on_release=lambda _: toast("Función de pago próximamente 💳"),
        )
        layout.add_widget(btn_pagar)

        root.add_widget(layout)
        self.add_widget(root)

    def on_pre_enter(self, *args):
        usuario = get_usuario()
        self.lbl_usuario.text = (
            f"Bienvenido, {usuario.get('nombre_completo', '')} 👋"
            if usuario else "Bienvenido 👋"
        )

    def volver_a_login(self):
        self.manager.current = "login_cliente_screen"
