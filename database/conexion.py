import cx_Oracle
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
lib_dir = os.getenv("LIB_DIR")
config_dir = os.getenv("CONFIG_DIR")
print(lib_dir)

# Inicializar el cliente Oracle SOLO UNA VEZ
try:
    cx_Oracle.init_oracle_client(lib_dir=lib_dir, config_dir=config_dir)
except cx_Oracle.ProgrammingError:
    print("✅ La base de datos ya había sido inicializada")
    pass

def get_connection():
    """
    Retorna una conexión activa a la base de datos Oracle.
    """
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    dsn = os.getenv("DSN")

    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    return conn