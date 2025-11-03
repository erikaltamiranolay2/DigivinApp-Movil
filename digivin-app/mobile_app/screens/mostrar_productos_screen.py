import os
import json
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
from kivy.network.urlrequest import UrlRequest


class MostrarProductosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        self._crear_barra_superior()
        self.central_box.add_widget(self.top_bar)

        # ===== BUSCADOR =====
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

        # ===== SCROLL DE PRODUCTOS =====
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

        # Cargar productos al inicio
        self.cargar_productos()

    # =======================================================
    # UI helpers
    # =======================================================
    def _crear_barra_superior(self):
        """Crea los botones de la barra superior."""
        self.top_bar.clear_widgets()

        # Botón de volver al login
        btn_login = MDIconButton(
            icon="account-circle",
            pos_hint={"center_y": 0.5},
            icon_size=dp(28),
            on_release=lambda *_: self.ir_a_login(),
        )
        self.top_bar.add_widget(btn_login)

        # Espaciador
        self.top_bar.add_widget(MDBoxLayout())

        # Botón carrito
        btn_carrito = MDIconButton(
            icon="cart",
            pos_hint={"center_y": 0.5},
            icon_size=dp(28),
            on_release=lambda *_: self.ir_a_carrito(),
        )
        self.top_bar.add_widget(btn_carrito)

    # =======================================================
    # Navegación
    # =======================================================
    def ir_a_login(self):
        self.manager.current = "login"

    def ir_a_carrito(self):
        self.manager.current = "carrito"

    # =======================================================
    # Cargar productos desde backend
    # =======================================================
    def cargar_productos(self):
        """Obtiene los productos desde tu API."""
        backend = os.getenv("BACKEND_URL", "http://10.0.2.2:5000")
        url = f"{backend}/api/products"
        self.container.clear_widgets()
        self.container.add_widget(MDLabel(text="⏳ Cargando productos...", halign="center"))

        UrlRequest(
            url,
            on_success=self._on_productos_ok,
            on_error=self._on_productos_error,
            on_failure=self._on_productos_error,
            timeout=10,
        )

    def _on_productos_ok(self, request, result):
        try:
            if isinstance(result, (bytes, bytearray)):
                data = json.loads(result.decode("utf-8"))
            else:
                data = result
            productos = data.get("products") if isinstance(data, dict) else data
        except Exception:
            productos = []

        self._mostrar_productos(productos)

    def _on_productos_error(self, request, error):
        self.container.clear_widgets()
        self.container.add_widget(
            MDLabel(text="⚠️ Error al cargar productos", halign="center")
        )
        print(f"Error al obtener productos: {error}")

    # =======================================================
    # Renderizar productos
    # =======================================================
    def _mostrar_productos(self, productos):
        self.container.clear_widgets()
        if not productos:
            self.container.add_widget(MDLabel(text="No hay productos disponibles"))
            return

        for producto in productos:
            nombre = producto.get("name") or producto.get("nombre", "Sin nombre")
            categoria = producto.get("category", "N/A")
            precio = producto.get("price") or producto.get("precio", 0)
            stock = producto.get("stock", 0)
            image_url = producto.get("image_url")

            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(160),
                padding=10,
                spacing=10,
                ripple_behavior=True,
                elevation=2,
            )

            # Imagen del producto
            img_widget = Image(
                source=image_url if image_url else "assets/no-image.png",
                size_hint=(0.3, 1),
            )

            # Info de producto
            info = MDBoxLayout(orientation="vertical", spacing=5)
            info.add_widget(MDLabel(text=f"[b]{nombre}[/b]", markup=True))
            info.add_widget(MDLabel(text=f"Categoría: {categoria}"))
            info.add_widget(MDLabel(text=f"Precio: ${precio:.2f}"))
            info.add_widget(MDLabel(text=f"Stock: {stock}"))

            # Botones acción
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
                    on_release=lambda x, p=producto: self._agregar_carrito(p),
                )
            )
            btns.add_widget(
                MDRaisedButton(
                    text="Comprar",
                    md_bg_color=(0.2, 0.6, 0.86, 1),
                    on_release=lambda x, p=producto: self._comprar(p),
                )
            )

            info.add_widget(btns)
            card.add_widget(img_widget)
            card.add_widget(info)
            self.container.add_widget(card)

    # =======================================================
    # Acciones
    # =======================================================
    def _agregar_carrito(self, producto):
        toast(f"🛒 {producto.get('name', 'Producto')} agregado al carrito")

    def _comprar(self, producto):
        toast(f"💳 Comprando {producto.get('name', 'producto')}")
        self.manager.current = "carrito"

    # =======================================================
    # Búsqueda local
    # =======================================================
    def filtrar_productos(self, *args):
        """Filtra productos en el backend según texto."""
        query = self.search_input.text.strip()
        if not query:
            self.cargar_productos()
            return

        backend = os.getenv("BACKEND_URL", "http://10.0.2.2:5000")
        url = f"{backend}/api/products?search={query}"
        UrlRequest(
            url,
            on_success=self._on_productos_ok,
            on_error=self._on_productos_error,
            on_failure=self._on_productos_error,
            timeout=10,
        )
