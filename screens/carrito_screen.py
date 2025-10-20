# screens/carrito_screen.py
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
import os
from io import BytesIO
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

import oci
from globales import (
    get_usuario,
    CARRITO,
    vaciar_carrito,
    calcular_total,
    incrementar_cantidad,
    decrementar_cantidad,
    actualizar_cantidad,
)


class CarritoScreen(Screen):
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

        # ===== BARRA SUPERIOR (botón volver) =====
        top_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=[0, 0, 0, 0],
        )

        btn_volver = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_y": 0.5},
            theme_icon_color="Custom",
            icon_size=dp(28),
            on_release=lambda *_: self.ir_a_productos(),
        )

        # Espaciador para centrar visualmente
        top_bar.add_widget(btn_volver)
        self.central_box.add_widget(top_bar)

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

        # ===== Label de total =====
        self.total_label = MDLabel(
            text="Total: $0.00",
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=dp(40),
        )
        self.central_box.add_widget(self.total_label)

        # ===== Botones finales =====
        buttons_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=10,
            padding=[0, 10, 0, 0],
        )
        self.vaciar_btn = MDRaisedButton(
            text="Vaciar carrito",
            md_bg_color=(0.9, 0.2, 0.2, 1),
            on_release=lambda *_: self._vaciar_carrito(),
        )
        self.finalizar_btn = MDRaisedButton(
            text="Finalizar compra",
            md_bg_color=(0.2, 0.6, 0.86, 1),
            on_release=lambda *_: self._finalizar_compra(),
        )
        buttons_box.add_widget(self.vaciar_btn)
        buttons_box.add_widget(self.finalizar_btn)
        self.central_box.add_widget(buttons_box)

        # ===== Agregar todo al wrapper =====
        wrapper = MDBoxLayout(orientation="vertical")
        wrapper.add_widget(self.central_box)
        self.add_widget(wrapper)

    # ----------------------------
    # Funcionalidad principal
    # ----------------------------

    def ir_a_productos(self):
        """Regresa a la pantalla de productos"""
        self.manager.current = "productos_screen"

    def obtener_imagen_desde_bucket(self, object_name):
        """Obtiene una imagen desde OCI"""
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

    def on_pre_enter(self):
        self.mostrar_carrito()

    def mostrar_carrito(self):
        self.container.clear_widgets()

        if not CARRITO:
            self.container.add_widget(
                MDLabel(text="🛒 Carrito vacío", halign="center", size_hint_y=None, height=dp(40))
            )
        else:
            for producto_id, item in CARRITO.items():
                producto = item["data"]
                cantidad = item["cantidad"]

                id_, nombre, codigo_barras, categoria, precio, impuestos, stock, proveedor_id, url_imagen = producto

                row = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(120),
                    spacing=10,
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

                # Info + controles
                info = MDBoxLayout(orientation="vertical", spacing=3)
                info.add_widget(MDLabel(text=f"[b]{nombre}[/b]", markup=True))
                info.add_widget(MDLabel(text=f"Precio: ${precio:.2f}"))
                info.add_widget(MDLabel(text=f"Cantidad: {cantidad}"))

                # Controles cantidad
                controls = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(40),
                    spacing=5,
                )
                btn_menos = MDIconButton(
                    icon="minus",
                    on_release=lambda _, pid=producto_id: (decrementar_cantidad(pid), self.mostrar_carrito()),
                )
                cantidad_input = MDTextField(
                    text=str(cantidad),
                    input_filter="int",
                    size_hint_x=None,
                    width=dp(40),
                    halign="center",
                    on_text_validate=lambda x, pid=producto_id: (
                        actualizar_cantidad(pid, int(x.text) if x.text.isdigit() else 1),
                        self.mostrar_carrito(),
                    ),
                )
                btn_mas = MDIconButton(
                    icon="plus",
                    on_release=lambda _, pid=producto_id: (incrementar_cantidad(pid), self.mostrar_carrito()),
                )
                controls.add_widget(btn_menos)
                controls.add_widget(cantidad_input)
                controls.add_widget(btn_mas)

                info.add_widget(controls)

                row.add_widget(img_widget)
                row.add_widget(info)
                self.container.add_widget(row)

        # Actualizar total
        total = calcular_total()
        self.total_label.text = f"Total: ${total:.2f}"

    def _vaciar_carrito(self):
        vaciar_carrito()
        self.mostrar_carrito()

    def _finalizar_compra(self):
        usuario = get_usuario()
        if usuario:
            self.manager.current = "pago_screen"
        else:
            self.manager.current = "login_cliente_screen"
