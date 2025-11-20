# Importamos librerias
import oracledb
import os
from dotenv import load_dotenv
# Cargamos variables de entorno
load_dotenv()
# Definimos valores gracias a las variables de entorno
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")
# Creamos una conexion reutilizable


def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

# Funcion para crear el esquema de la base de datos


def create_schema(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print(f"Tabla creada \n {query}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err} \n {query}")


tables = [
    ("CREATE TABLE CLIENTE("
     "id_cliente INTEGER PRIMARY KEY,"
     "nombre VARCHAR2(100) NOT NULL,"
     "apellido VARCHAR2(100),"
     "telefono VARCHAR2(20),"
     "email VARCHAR2(100),"
     "fecha_registro DATE DEFAULT SYSDATE"
     ")"),
    ("CREATE TABLE PEDIDO("
     "id_pedido INTEGER PRIMARY KEY,"
     "id_cliente INTEGER NOT NULL,"
     "fecha_pedido DATE DEFAULT SYSDATE,"
     "total NUMBER(10,2),"
     "estado VARCHAR2(20),"
     "CONSTRAINT fk_pedido_cliente"
     "FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)"
     ")"),
    ("CREATE TABLE PEDIDO_PARA_LLEVAR("
     "id_pedido INTEGER PRIMARY KEY,"
     "hora_retiro VARCHAR2(10),"
     "empaquetado VARCHAR2(3) CHECK (empaquetado IN ('SI','NO')),"
     "CONSTRAINT fk_pl_pedido"
     "FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)"
     ")"),
    ("CREATE TABLE PEDIDO_EN_LOCAL("
     "id_pedido INTEGER PRIMARY KEY,"
     "numero_mesa INTEGER NOT NULL,"
     "camarero VARCHAR2(100),"
     "CONSTRAINT fk_el_pedido"
     "FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)"
     ")"),
    ("CREATE TABLE PEDIDO_DESPACHO("
     "id_pedido INTEGER PRIMARY KEY,"
     "direccion_envio VARCHAR2(200) NOT NULL,"
     "ciudad VARCHAR2(100),"
     "costo_envio NUMBER(10,2),"
     "CONSTRAINT fk_pd_pedido"
     "FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)"
     ")")
]

for query in tables:
    create_schema(query)


# Read - Consulta de datos
def read_clientes():
    sql = (
        "SELECT * FROM CLIENTE"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print("Consulta a la tabla CLIENTE")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos:")

def read_cliente_by_id(id):
    pass
