import oracledb
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("ORACLE_USER")
PASSWORD = os.getenv("ORACLE_PASSWORD")
DSN = os.getenv("ORACLE_DSN")


def get_connection():
    return oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN)


class DatabaseError(Exception):
    pass


# ======================
#       CLIENTE
# ======================
class Cliente:
    def __init__(self, id_cliente, nombre, telefono=None, correo=None):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__telefono = telefono
        self.__correo = correo

    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        self.__correo = valor

    def __str__(self):
        return f"Cliente[{self.__id_cliente}]: {self.__nombre}, Tel: {self.__telefono}, Correo: {self.__correo}"


class ClienteRepository:
    @staticmethod
    def crear(cliente: Cliente):
        sql = """
        INSERT INTO CLIENTE (id_cliente, nombre, telefono, correo)
        VALUES (:id, :nombre, :telefono, :correo)
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql,
                                id=cliente.id_cliente,
                                nombre=cliente.nombre,
                                telefono=cliente.telefono,
                                correo=cliente.correo)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al crear cliente: {e}")

    @staticmethod
    def actualizar(cliente: Cliente):
        sql = """
        UPDATE CLIENTE
        SET nombre=:nombre, telefono=:telefono, correo=:correo
        WHERE id_cliente=:id
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql,
                                nombre=cliente.nombre,
                                telefono=cliente.telefono,
                                correo=cliente.correo,
                                id=cliente.id_cliente)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al actualizar cliente: {e}")

    @staticmethod
    def eliminar(id_cliente):
        sql = "DELETE FROM CLIENTE WHERE id_cliente = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, id=id_cliente)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al eliminar cliente: {e}")

    @staticmethod
    def obtener_por_id(id_cliente):
        sql = """
        SELECT id_cliente, nombre, telefono, correo
        FROM CLIENTE
        WHERE id_cliente = :id
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, id=id_cliente)
                    row = cur.fetchone()
                    if row:
                        return Cliente(*row)
                    return None
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al obtener cliente: {e}")

    @staticmethod
    def listar_todos():
        sql = "SELECT id_cliente, nombre, telefono, correo FROM CLIENTE"
        try:
            clientes = []
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    for row in cur:
                        clientes.append(Cliente(*row))
            return clientes
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al listar clientes: {e}")


# ======================
#       PEDIDOS
# ======================
class Pedido(ABC):
    def __init__(self, numeroPedido, cliente: Cliente, fecha=None, totalPagar=0.0):
        self.__numeroPedido = numeroPedido
        self.__cliente = cliente
        self.fecha = fecha
        self.__totalPagar = totalPagar

    @property
    def numeroPedido(self):
        return self.__numeroPedido

    @property
    def cliente(self):
        return self.__cliente

    @property
    def totalPagar(self):
        return self.__totalPagar

    @totalPagar.setter
    def totalPagar(self, valor):
        self.__totalPagar = valor

    @abstractmethod
    def procesar(self):
        pass


class PedidoEnLocal(Pedido):
    def __init__(self, numeroPedido, cliente: Cliente, numeroMesa=None, fecha=None, totalPagar=0.0):
        super().__init__(numeroPedido, cliente, fecha, totalPagar)
        self.numeroMesa = numeroMesa

    def procesar(self):
        print(f"Pedido en local #{self.numeroPedido} - Mesa {self.numeroMesa}")


class PedidoParaLlevar(Pedido):
    def __init__(self, numeroPedido, cliente: Cliente, tiempoEstimadoRetiro=None, fecha=None, totalPagar=0.0):
        super().__init__(numeroPedido, cliente, fecha, totalPagar)
        self.tiempoEstimadoRetiro = tiempoEstimadoRetiro

    def procesar(self):
        print(f"Pedido para llevar #{self.numeroPedido} - Retiro en {self.tiempoEstimadoRetiro}")


class PedidoDespacho(Pedido):
    def __init__(self, numeroPedido, cliente: Cliente, direccion=None, fecha=None, totalPagar=0.0):
        super().__init__(numeroPedido, cliente, fecha, totalPagar)
        self.direccion = direccion

    def procesar(self):
        print(f"Pedido despacho #{self.numeroPedido} - Dirección {self.direccion}")


class PedidoRepository:
    @staticmethod
    def crear(pedido: Pedido):

        sql_pedido = """
        INSERT INTO PEDIDO (numeroPedido, id_cliente, fecha, totalPagar)
        VALUES (:num, :id_cliente, SYSDATE, :total)
        """

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_pedido,
                                num=pedido.numeroPedido,
                                id_cliente=pedido.cliente.id_cliente,
                                total=pedido.totalPagar)

                    if isinstance(pedido, PedidoEnLocal):
                        cur.execute("""
                        INSERT INTO PEDIDO_EN_LOCAL (numeroPedido, numeroMesa)
                        VALUES (:num, :mesa)
                        """, num=pedido.numeroPedido, mesa=pedido.numeroMesa)

                    elif isinstance(pedido, PedidoParaLlevar):
                        cur.execute("""
                        INSERT INTO PEDIDO_PARA_LLEVAR (numeroPedido, tiempoEstimadoRetiro)
                        VALUES (:num, :tiempo)
                        """, num=pedido.numeroPedido, tiempo=pedido.tiempoEstimadoRetiro)

                    elif isinstance(pedido, PedidoDespacho):
                        cur.execute("""
                        INSERT INTO PEDIDO_DESPACHO (numeroPedido, direccion)
                        VALUES (:num, :direccion)
                        """, num=pedido.numeroPedido, direccion=pedido.direccion)

                conn.commit()

        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al crear pedido: {e}")

    @staticmethod
    def actualizar(pedido: Pedido):
        sql = """
        UPDATE PEDIDO SET totalPagar=:total WHERE numeroPedido=:num
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, total=pedido.totalPagar, num=pedido.numeroPedido)

                    if isinstance(pedido, PedidoEnLocal):
                        cur.execute("""
                        UPDATE PEDIDO_EN_LOCAL SET numeroMesa=:mesa WHERE numeroPedido=:num
                        """, mesa=pedido.numeroMesa, num=pedido.numeroPedido)

                    elif isinstance(pedido, PedidoParaLlevar):
                        cur.execute("""
                        UPDATE PEDIDO_PARA_LLEVAR SET tiempoEstimadoRetiro=:tiempo WHERE numeroPedido=:num
                        """, tiempo=pedido.tiempoEstimadoRetiro, num=pedido.numeroPedido)

                    elif isinstance(pedido, PedidoDespacho):
                        cur.execute("""
                        UPDATE PEDIDO_DESPACHO SET direccion=:direccion WHERE numeroPedido=:num
                        """, direccion=pedido.direccion, num=pedido.numeroPedido)

                conn.commit()

        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al actualizar pedido: {e}")

    @staticmethod
    def eliminar(numeroPedido):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM PEDIDO_EN_LOCAL WHERE numeroPedido=:num", num=numeroPedido)
                    cur.execute("DELETE FROM PEDIDO_PARA_LLEVAR WHERE numeroPedido=:num", num=numeroPedido)
                    cur.execute("DELETE FROM PEDIDO_DESPACHO WHERE numeroPedido=:num", num=numeroPedido)
                    cur.execute("DELETE FROM PEDIDO WHERE numeroPedido=:num", num=numeroPedido)

                conn.commit()

        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al eliminar pedido: {e}")

    @staticmethod
    def obtener_por_id(numeroPedido):
        sql = """
        SELECT numeroPedido, id_cliente, fecha, totalPagar
        FROM PEDIDO
        WHERE numeroPedido=:num
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:

                    cur.execute(sql, num=numeroPedido)
                    row = cur.fetchone()

                    if not row:
                        return None

                    numeroPedido, id_cliente, fecha, total = row
                    cliente = ClienteRepository.obtener_por_id(id_cliente)

                    # Detectar tabla hija
                    cur.execute("SELECT numeroMesa FROM PEDIDO_EN_LOCAL WHERE numeroPedido=:num", num=numeroPedido)
                    r_local = cur.fetchone()

                    if r_local:
                        pedido = PedidoEnLocal(numeroPedido, cliente, r_local[0])

                    else:
                        cur.execute("SELECT tiempoEstimadoRetiro FROM PEDIDO_PARA_LLEVAR WHERE numeroPedido=:num",
                                    num=numeroPedido)
                        r_llevar = cur.fetchone()

                        if r_llevar:
                            pedido = PedidoParaLlevar(numeroPedido, cliente, r_llevar[0])

                        else:
                            cur.execute("SELECT direccion FROM PEDIDO_DESPACHO WHERE numeroPedido=:num",
                                        num=numeroPedido)
                            r_des = cur.fetchone()

                            if r_des:
                                pedido = PedidoDespacho(numeroPedido, cliente, r_des[0])
                            else:
                                return None

                    pedido.totalPagar = total
                    pedido.fecha = fecha

                    return pedido

        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al obtener pedido: {e}")

    @staticmethod
    def listar_todos():
        sql = "SELECT numeroPedido FROM PEDIDO"
        pedidos = []

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)

                    for (numeroPedido,) in cur:
                        pedido = PedidoRepository.obtener_por_id(numeroPedido)
                        if pedido:
                            pedidos.append(pedido)

            return pedidos

        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error al listar pedidos: {e}")



# ===========================
#   PRUEBA DE FUNCIONAMIENTO
# ===========================
if __name__ == "__main__":
    try:
        cliente1 = Cliente(1, "Ana Torres", "555-9876", "ana@example.com")
        ClienteRepository.crear(cliente1)

        pedido_local = PedidoEnLocal(1001, cliente1, numeroMesa=5, totalPagar=150.75)
        PedidoRepository.crear(pedido_local)

        pedido_llevar = PedidoParaLlevar(1002, cliente1, tiempoEstimadoRetiro="45 min", totalPagar=75.50)
        PedidoRepository.crear(pedido_llevar)

        pedido_despacho = PedidoDespacho(1003, cliente1, direccion="Calle Falsa 123", totalPagar=120.00)
        PedidoRepository.crear(pedido_despacho)

        print("\n--- Clientes ---")
        for c in ClienteRepository.listar_todos():
            print(c)

        print("\n--- Pedidos ---")
        for p in PedidoRepository.listar_todos():
            p.procesar()
            print(f"Total: {p.totalPagar}\n")

        pedido_local.numeroMesa = 10
        pedido_local.totalPagar = 155.00
        PedidoRepository.actualizar(pedido_local)

        PedidoRepository.eliminar(1003)

        print("\n--- Después de actualizar y eliminar ---")
        for p in PedidoRepository.listar_todos():
            p.procesar()
            print(f"Total: {p.totalPagar}\n")

    except DatabaseError as e:
        print(e)
