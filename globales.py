# globales.py

# ==============================
# 🛒 CARRITO GLOBAL
# ==============================
# Estructura: {producto_id: {"data": producto_tuple, "cantidad": n}}
CARRITO = {}

# ==============================
# 👤 USUARIO ACTUAL
# ==============================
USUARIO_ACTUAL = None  # Contendrá un diccionario con datos del usuario logueado

def agregar_al_carrito(producto, cantidad=1):
    producto_id = producto[0]  # id del producto
    if producto_id in CARRITO:
        CARRITO[producto_id]["cantidad"] += cantidad
    else:
        CARRITO[producto_id] = {"data": producto, "cantidad": cantidad}

def eliminar_del_carrito(producto_id):
    if producto_id in CARRITO:
        del CARRITO[producto_id]

def vaciar_carrito():
    CARRITO.clear()

def actualizar_cantidad(producto_id, nueva_cantidad):
    """Actualiza la cantidad absoluta de un producto en el carrito"""
    if producto_id in CARRITO:
        if nueva_cantidad <= 0:
            eliminar_del_carrito(producto_id)
        else:
            CARRITO[producto_id]["cantidad"] = nueva_cantidad

def incrementar_cantidad(producto_id):
    """Aumenta en +1 la cantidad"""
    if producto_id in CARRITO:
        CARRITO[producto_id]["cantidad"] += 1

def decrementar_cantidad(producto_id):
    """Disminuye en -1 la cantidad (si llega a 0 lo elimina)"""
    if producto_id in CARRITO:
        CARRITO[producto_id]["cantidad"] -= 1
        if CARRITO[producto_id]["cantidad"] <= 0:
            eliminar_del_carrito(producto_id)

def calcular_total():
    total = 0
    for item in CARRITO.values():
        producto = item["data"]
        cantidad = item["cantidad"]
        precio = producto[4]  # Precio ya incluye IVA
        total += precio * cantidad
    return total


# ==============================
# 📦 ORDENES (para pantalla de órdenes entrantes)
# ==============================
ORDENES = []  # Lista global de órdenes (sincronizadas o nuevas)

def agregar_orden(orden):
    """
    Agrega una nueva orden localmente.
    Estructura esperada:
    {
        "id": int,
        "cliente": str,
        "total": float,
        "status_entrega": int,  # 1=Hecha, 2=En reparto, 3=Entregado
        "fecha": str
    }
    """
    ORDENES.append(orden)

def actualizar_estado_orden(orden_id, nuevo_estado):
    """
    Actualiza el estado de entrega (1, 2 o 3) de una orden existente.
    """
    for orden in ORDENES:
        if orden["id"] == orden_id:
            orden["status_entrega"] = nuevo_estado
            break

def obtener_ordenes():
    """Devuelve todas las órdenes registradas localmente."""
    return ORDENES

def set_usuario(usuario: dict):
    """Guarda el usuario logueado globalmente"""
    global USUARIO_ACTUAL
    USUARIO_ACTUAL = usuario

def get_usuario():
    """Devuelve el usuario actual logueado o None"""
    return USUARIO_ACTUAL

def cerrar_sesion():
    """Limpia la sesión actual"""
    global USUARIO_ACTUAL
    USUARIO_ACTUAL = None