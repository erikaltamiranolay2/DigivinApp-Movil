from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.toast import toast
from database.queries import insertar_cliente


class RegistroClienteScreen(Screen):
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
            on_release=lambda _: setattr(self.manager, "current", "login_cliente_screen"),
        )
        root.add_widget(btn_volver)

        # --- CONTENEDOR CENTRAL ---
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(40), dp(10), dp(40), dp(10)],
            size_hint=(0.9, None),
            height=dp(480),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
        )

        # --- TÍTULO CON ICONO ---
        titulo_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            pos_hint={"center_x": 0.5},
        )

        icon = MDIconButton(
            icon="account-plus",
            icon_size=dp(26),
            theme_icon_color="Custom",
            icon_color=(0, 0, 0, 1),
            md_bg_color=(0, 0, 0, 0),
            padding=0,
        )

        titulo = MDLabel(
            text="Registro de cliente",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            halign="center",
            valign="middle",
            shorten=True,  # 🔹 Evita que salte de línea
            size_hint_x=None,  # 🔹 Permite controlar el ancho manualmente
            width=dp(200),  # 🔹 Ancho suficiente para mantenerlo en una sola línea
        )

        titulo_layout.add_widget(icon)
        titulo_layout.add_widget(titulo)
        layout.add_widget(titulo_layout)

        # --- CAMPOS ---
        self.nombre_input = MDTextField(
            hint_text="Nombre completo",
            mode="rectangle",
            size_hint_x=1,
            font_size=dp(14),
        )
        self.email_input = MDTextField(
            hint_text="Correo electrónico",
            mode="rectangle",
            size_hint_x=1,
            font_size=dp(14),
        )
        self.telefono_input = MDTextField(
            hint_text="Teléfono",
            mode="rectangle",
            size_hint_x=1,
            font_size=dp(14),
        )
        self.pass_input = MDTextField(
            hint_text="Contraseña",
            mode="rectangle",
            password=True,
            size_hint_x=1,
            font_size=dp(14),
        )

        layout.add_widget(self.nombre_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.telefono_input)
        layout.add_widget(self.pass_input)

        # --- BOTÓN REGISTRAR ---
        btn_registrar = MDRaisedButton(
            text="Registrar",
            md_bg_color=(0, 0.5, 1, 1),
            size_hint=(1, None),
            height=dp(50),
            on_release=self.registrar_cliente,
        )
        layout.add_widget(btn_registrar)

        root.add_widget(layout)
        self.add_widget(root)

    def registrar_cliente(self, *args):
        nombre = self.nombre_input.text.strip()
        email = self.email_input.text.strip()
        telefono = self.telefono_input.text.strip()
        password = self.pass_input.text.strip()

        if not nombre or not email or not password:
            toast("❗ Faltan campos obligatorios")
            return

        try:
            insertar_cliente(email, telefono, password, nombre)
            toast("✅ Registro exitoso")
            self.manager.current = "login_cliente_screen"
        except Exception as e:
            toast(f"⚠️ Error: {e}")
