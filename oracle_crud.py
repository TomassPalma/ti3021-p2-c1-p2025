import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")


def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)


def create_schema(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
    except oracledb.DatabaseError as e:
        print("Error creando tabla:", e)


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
     "CONSTRAINT fk_pedido_cliente "
     "FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)"
     ")"),

    ("CREATE TABLE PEDIDO_PARA_LLEVAR("
     "id_pedido INTEGER PRIMARY KEY,"
     "hora_retiro VARCHAR2(10),"
     "empaquetado VARCHAR2(3) CHECK (empaquetado IN ('SI','NO')),"
     "CONSTRAINT fk_pl_pedido "
     "FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)"
     ")"),

    ("CREATE TABLE PEDIDO_EN_LOCAL("
     "id_pedido INTEGER PRIMARY KEY,"
     "numero_mesa INTEGER NOT NULL,"
     "camarero VARCHAR2(100),"
     "CONSTRAINT fk_el_pedido "
     "FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)"
     ")"),

    ("CREATE TABLE PEDIDO_DESPACHO("
     "id_pedido INTEGER PRIMARY KEY,"
     "direccion_envio VARCHAR2(200) NOT NULL,"
     "ciudad VARCHAR2(100),"
     "costo_envio NUMBER(10,2),"
     "CONSTRAINT fk_pd_pedido "
     "FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido)"
     ")")
]

for t in tables:
    create_schema(t)


# -------------------------
# CRUD CLIENTES
# -------------------------

def create_cliente(id_cliente, nombre, apellido, telefono, email):
    sql = ("INSERT INTO CLIENTE "
           "(id_cliente, nombre, apellido, telefono, email) ")