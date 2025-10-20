# screens/mostrar_productos_screen.py
import os
from io import BytesIO
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.toast import toast
import oci

from database.queries import obtener_productos
from globales import agregar_al_carrito, get_usuario


class MostrarProductosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- Configuración OCI ---
        config = oci.config.from_file()
        self.object_storage = oci.object_storage.ObjectStorageClient(config)
        self.namespace = "axlqs6otp3rh"
        self.bucket_name = "licoreria-productos"

        # --- Layout principal ---
        self.central_box = MDBoxLayout(
            orientation="vertical",
            padding=[dp(15), dp(25), dp(15), dp(10)],
            spacing=15,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )

        # ===== BARRA SUPERIOR =====
        self.top_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=[0, 0, 0, 0],
        )

        self.actualizar_barra_superior()
        self.central_box.add_widget(self.top_bar)

        # ===== Layout buscador =====
        search_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=10,
            padding=[0, dp(10), 0, dp(10)],
        )

        self.search_input = MDTextField(
            hint_text="Buscar producto...",
            size_hint_x=0.7,
            multiline=False,
        )

        search_btn = MDRaisedButton(
            text="Buscar",
            size_hint_x=0.3,
            md_bg_color=(0.2, 0.6, 0.86, 1),
            on_release=self.filtrar_productos,
        )

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        self.central_box.add_widget(search_layout)

        # ===== Scroll de productos =====
        scroll = MDScrollView()
        self.container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10,
        )
        self.container.bind(minimum_height=self.container.setter("height"))
        scroll.add_widget(self.container)
        self.central_box.add_widget(scroll)

        wrapper = MDBoxLayout(orientation="vertical")
        wrapper.add_widget(self.central_box)
        self.add_widget(wrapper)

        self.cargar_productos()

    # -------------------
    # Métodos auxiliares
    # -------------------

    def on_pre_enter(self, *args):
        """Actualiza la barra superior según el estado de login"""
        self.actualizar_barra_superior()

    def actualizar_barra_superior(self):
        """Actualiza los botones de la barra superior según si hay sesión"""
        self.top_bar.clear_widgets()
        usuario = get_usuario()

        if usuario:
            # Si hay usuario logueado → botón negro de pedidos 🧾
            btn_pedidos = MDIconButton(
                icon="clipboard-list",
                pos_hint={"center_y": 0.5},
                icon_size=dp(28),
                theme_icon_color="Custom",
                on_release=lambda *_: self.ir_a_pedidos(),
            )
            self.top_bar.add_widget(btn_pedidos)
        else:
            # Si no hay sesión → botón de login 👤
            btn_login = MDIconButton(
                icon="account-circle",
                pos_hint={"center_y": 0.5},
                icon_size=dp(28),
                on_release=lambda *_: self.ir_a_login(),
            )
            self.top_bar.add_widget(btn_login)

        # Espaciador
        spacer = MDBoxLayout()
        self.top_bar.add_widget(spacer)

        # Botón carrito 🛒 (siempre visible)
        btn_carrito = MDIconButton(
            icon="cart",
            pos_hint={"center_y": 0.5},
            icon_size=dp(28),
            on_release=lambda *_: self.ir_a_carrito(),
        )
        self.top_bar.add_widget(btn_carrito)

    def ir_a_carrito(self):
        self.manager.current = "carrito_screen"

    def ir_a_login(self):
        self.manager.current = "login_cliente_screen"

    def ir_a_pedidos(self):
        usuario = get_usuario()
        if usuario:
            toast(f"🧾 Mostrando pedidos de {usuario['nombre_completo']}")
        else:
            toast("⚠️ Debes iniciar sesión para ver tus pedidos")

    def obtener_imagen_desde_bucket(self, object_name):
        try:
            response = self.object_storage.get_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                object_name=object_name,
            )
            data = response.data.content
            return BytesIO(data)
        except Exception as e:
            print(f"⚠️ Error obteniendo imagen '{object_name}' del bucket: {e}")
            return None

    def cargar_productos(self):
        self.container.clear_widgets()
        productos = obtener_productos()

        for p in productos:
            id_, nombre, codigo_barras, categoria, precio, _, stock, proveedor_id, url_imagen = p

            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(160),
                padding=10,
                spacing=10,
                ripple_behavior=True,
                elevation=1,
            )

            # Imagen
            if url_imagen:
                buf = self.obtener_imagen_desde_bucket(url_imagen)
                if buf:
                    try:
                        ci = CoreImage(buf, ext=os.path.splitext(url_imagen)[1][1:])
                        img_widget = Image(texture=ci.texture, size_hint=(0.3, 1))
                    except Exception:
                        img_widget = Image(source="assets/no-image.png", size_hint=(0.3, 1))
                else:
                    img_widget = Image(source="assets/no-image.png", size_hint=(0.3, 1))
            else:
                img_widget = Image(source="assets/no-image.png", size_hint=(0.3, 1))

            # Información
            info = MDBoxLayout(orientation="vertical", spacing=5)
            info.add_widget(MDLabel(text=f"[b]{nombre}[/b]", markup=True))
            info.add_widget(MDLabel(text=f"Categoría: {categoria or 'N/A'}"))
            info.add_widget(MDLabel(text=f"Precio: ${precio:.2f}"))
            info.add_widget(MDLabel(text=f"Stock: {stock}"))

            # Botones
            btns = MDBoxLayout(
                orientation="horizontal",
                spacing=10,
                size_hint_y=None,
                height=dp(40),
            )
            btns.add_widget(
                MDRaisedButton(
                    text="Agregar",
                    md_bg_color=(0.2, 0.6, 0.86, 1),
                    on_release=lambda x, prod=p: self.agregar_carrito(prod),
                )
            )
            btns.add_widget(
                MDRaisedButton(
                    text="Comprar",
                    md_bg_color=(0.2, 0.6, 0.86, 1),
                    on_release=lambda x, prod=p: self.comprar_producto(prod),
                )
            )

            info.add_widget(btns)
            card.add_widget(img_widget)
            card.add_widget(info)
            self.container.add_widget(card)

    def agregar_carrito(self, producto):
        agregar_al_carrito(producto, 1)
        print(f"📦 Agregado al carrito: {producto[1]}")

    def comprar_producto(self, producto):
        agregar_al_carrito(producto, 1)
        self.manager.current = "carrito_screen"

    def filtrar_productos(self, *args):
        query = self.search_input.text.strip().lower()
        if not query:
            self.cargar_productos()
            return
        productos = [p for p in obtener_productos() if query in p[1].lower()]
        self.container.clear_widgets()
        for p in productos:
            self.agregar_carrito(p)
