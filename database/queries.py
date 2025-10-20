import cx_Oracle
import hashlib
import bcrypt
from database.conexion import get_connection


# ==============================
# Helper para hash de password
# ==============================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ==============================
# USUARIOS
# ==============================
def insertar_usuario(nombre, rol, usuario, password, permisos=None):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO usuarios (nombre, rol, usuario, password_hash, permisos)
        VALUES (:1, :2, :3, :4, :5)
    """
    cur.execute(sql, (nombre, rol, usuario, hash_password(password), permisos))
    conn.commit()
    cur.close()
    conn.close()


def obtener_usuario(usuario, password):
    """Verifica usuario y password para login"""
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT id, nombre, rol, usuario FROM usuarios WHERE usuario = :1 AND password_hash = :2"
    cur.execute(sql, (usuario, hash_password(password)))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row  # (id, nombre, rol, usuario) o None

def get_user_by_username(username):
    """
    Retorna un diccionario con los datos del usuario a partir del nombre de usuario.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, rol, usuario, password_hash, permisos
        FROM usuarios
        WHERE usuario = :username
    """, {"username": username})

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "rol": row[2],
            "usuario": row[3],
            "password_hash": row[4],
            "permisos": row[5]
        }
    return None


# ==============================
# PRODUCTOS
# ==============================
def insertar_producto(nombre, codigo_barras, categoria, precio, stock=0, proveedor_id=None, url_imagen=None):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO productos (nombre, codigo_barras, categoria, precio, stock, proveedor_id, url_imagen)
        VALUES (:1, :2, :3, :4, :5, :6, :7)
    """
    cur.execute(sql, (nombre, codigo_barras, categoria, precio, stock, proveedor_id, url_imagen))
    conn.commit()
    cur.close()
    conn.close()


def obtener_productos():
    """
    Retorna todos los productos con todos sus campos, incluyendo url_imagen.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, codigo_barras, categoria, precio, impuestos, stock, proveedor_id, url_imagen
        FROM productos
    """)

    filas = cursor.fetchall()
    conn.close()
    return filas


# ==============================
# VENTAS
# ==============================
def registrar_venta(codigo_barras, cantidad, cliente_id=None, usuario_id=None):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Buscar producto
    cur.execute("SELECT id, precio, stock, impuestos FROM productos WHERE codigo_barras = :1", (codigo_barras,))
    producto = cur.fetchone()
    if not producto:
        raise Exception("Producto no encontrado")

    producto_id, precio, stock, impuestos = producto

    if stock < cantidad:
        raise Exception("Stock insuficiente")

    total = (precio * cantidad) * (1 + impuestos / 100)

    # 2. Insertar venta
    cur.execute(
        "INSERT INTO ventas (usuario_id, cliente_id, total) VALUES (:1, :2, :3) RETURNING id INTO :4",
        (usuario_id, cliente_id, total, cur.var(cx_Oracle.NUMBER))
    )
    venta_id = cur.getimplicitresults()[0][0] if cur.getimplicitresults() else None

    # 3. Insertar detalle
    cur.execute(
        """
        INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, impuesto)
        VALUES (:1, :2, :3, :4, :5)
        """,
        (venta_id, producto_id, cantidad, precio, impuestos)
    )

    # 4. Actualizar stock
    cur.execute(
        "UPDATE productos SET stock = stock - :1 WHERE id = :2",
        (cantidad, producto_id)
    )

    # 5. Insertar movimiento en inventario
    cur.execute(
        """
        INSERT INTO inventario (producto_id, tipo_movimiento, cantidad, usuario_id, nota)
        VALUES (:1, 'salida', :2, :3, :4)
        """,
        (producto_id, cantidad, usuario_id, f"Venta ID {venta_id}")
    )

    conn.commit()
    cur.close()
    conn.close()
    return venta_id

def registrar_venta_carrito(carrito, usuario_id=None, cliente_id=None, tipo_venta="venta_fisica"):
    """
    Registra una venta con múltiples productos desde el carrito.
    - carrito: dict {id_producto: {"data": tuple, "cantidad": int}}
    - usuario_id: usuario que realiza la venta
    - cliente_id: cliente (si aplica)
    - tipo_venta: "venta_online" o "venta_fisica"
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        total = 0

        # Calcular total
        for producto_id, item in carrito.items():
            prod = item["data"]
            cantidad = item["cantidad"]
            precio = prod[4]         # índice 4 = precio
            impuestos = prod[5]      # índice 5 = impuestos
            total += (precio * cantidad) * (1 + (impuestos or 0) / 100)

        # Status según tipo
        status_entrega = 1 if tipo_venta == "venta_online" else 3

        # Insertar cabecera de venta
        cur.execute(
            """
            INSERT INTO ventas (usuario_id, cliente_id, total, status_entrega, tipo_venta)
            VALUES (:1, :2, :3, :4, :5)
            RETURNING id INTO :6
            """,
            (usuario_id, cliente_id, total, status_entrega, tipo_venta, cur.var(cx_Oracle.NUMBER))
        )
        venta_id = cur.getimplicitresults()[0][0]

        # Insertar detalles de cada producto
        for producto_id, item in carrito.items():
            prod = item["data"]
            cantidad = item["cantidad"]
            precio = prod[4]
            impuestos = prod[5]

            # Insertar detalle
            cur.execute(
                """
                INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, impuesto)
                VALUES (:1, :2, :3, :4, :5)
                """,
                (venta_id, producto_id, cantidad, precio, impuestos)
            )

            # Actualizar stock
            cur.execute(
                "UPDATE productos SET stock = stock - :1 WHERE id = :2",
                (cantidad, producto_id)
            )

            # Movimiento inventario
            cur.execute(
                """
                INSERT INTO inventario (producto_id, tipo_movimiento, cantidad, usuario_id, nota)
                VALUES (:1, 'salida', :2, :3, :4)
                """,
                (producto_id, cantidad, usuario_id, f"Venta ID {venta_id}")
            )

        conn.commit()
        return venta_id

    except Exception as e:
        conn.rollback()
        print(f"⚠️ Error registrando venta desde carrito: {e}")
        return None

    finally:
        cur.close()
        conn.close()

# ==============================
# CLIENTES
# ==============================

# 🔹 Insertar nuevo cliente
def insertar_cliente(email, telefono, password, nombre_completo):
    conn = get_connection()
    cur = conn.cursor()
    password_hash = hash_password(password)

    password_hash = hash_password(password)  # ← aquí encriptamos antes de guardar

    cur.execute("""
            INSERT INTO clientes (nombre_completo, email, telefono, password_hash)
            VALUES (:1, :2, :3, :4)
        """, (nombre_completo, email, telefono, password_hash))

    conn.commit()
    cur.close()
    conn.close()


# 🔹 Buscar cliente por email
def obtener_cliente_por_email(email):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT id, email, telefono, password_hash, nombre_completo FROM clientes WHERE email = :email"
    cur.execute(sql, {"email": email})
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "email": row[1],
            "telefono": row[2],
            "password_hash": row[3],
            "nombre_completo": row[4],
        }
    return None


def hash_password(password: str) -> str:
    """Devuelve el hash seguro de una contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verifica que la contraseña ingresada coincida con el hash almacenado"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

# 🔹 Verificar login
def verificar_login(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nombre_completo, email, telefono, password_hash
        FROM clientes
        WHERE email = :email
    """, {"email": email})

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        cliente = {
            "id": row[0],
            "nombre_completo": row[1],
            "email": row[2],
            "telefono": row[3],
            "password_hash": row[4],
        }
        # ✅ verificamos contraseña
        if verify_password(password, cliente["password_hash"]):
            return cliente
    return None
