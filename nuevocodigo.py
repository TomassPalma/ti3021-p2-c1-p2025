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

# =====================================================
#                      CLIENTE
# =====================================================
class Cliente:
    def __init__(self, id_cliente: str, nombre: str, telefono=None, correo=None):
        self.__id_cliente = id_cliente  # ahora string
        self.__nombre = nombre
        self.__telefono = telefono
        self.__correo = correo

    @property
    def id_cliente(self): return self.__id_cliente
    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self, valor): self.__nombre = valor

    @property
    def telefono(self): return self.__telefono
    @telefono.setter
    def telefono(self, valor): self.__telefono = valor

    @property
    def correo(self): return self.__correo
    @correo.setter
    def correo(self, valor): self.__correo = valor

    def __str__(self):
        return f"Cliente[{self.__id_cliente}] - {self.__nombre} - {self.__telefono} - {self.__correo}"


class ClienteRepository:
    @staticmethod
    def crear(cliente: Cliente):
        sql = "INSERT INTO CLIENTE (id_cliente, nombre, telefono, correo) VALUES (:id, :nombre, :tel, :cor)"
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, id=cliente.id_cliente, nombre=cliente.nombre,
                                tel=cliente.telefono, cor=cliente.correo)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error creando cliente: {e}")

    @staticmethod
    def actualizar(cliente: Cliente):
        sql = "UPDATE CLIENTE SET nombre=:nom, telefono=:tel, correo=:cor WHERE id_cliente=:id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, nom=cliente.nombre, tel=cliente.telefono,
                                cor=cliente.correo, id=cliente.id_cliente)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error actualizando cliente: {e}")

    @staticmethod
    def eliminar(id_cliente: str):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM CLIENTE WHERE id_cliente=:id", id=id_cliente)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error eliminando cliente: {e}")

    @staticmethod
    def obtener_por_id(id_cliente: str):
        sql = "SELECT id_cliente, nombre, telefono, correo FROM CLIENTE WHERE id_cliente=:id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, id=id_cliente)
                    row = cur.fetchone()
                    if row:
                        return Cliente(*row)
                    return None
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error obteniendo cliente: {e}")

    @staticmethod
    def listar_todos():
        clientes = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id_cliente, nombre, telefono, correo FROM CLIENTE")
                    for row in cur:
                        clientes.append(Cliente(*row))
            return clientes
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error listando clientes: {e}")

# =====================================================
#                      PEDIDOS
# =====================================================
class Pedido(ABC):
    def __init__(self, numeroPedido, cliente: Cliente, fecha=None, totalPagar=0):
        self.numeroPedido = numeroPedido
        self.cliente = cliente
        self.fecha = fecha
        self.totalPagar = totalPagar

    @abstractmethod
    def procesar(self):
        pass

class PedidoEnLocal(Pedido):
    def __init__(self, numeroPedido, cliente, numeroMesa, fecha=None, totalPagar=0):
        super().__init__(numeroPedido, cliente, fecha, totalPagar)
        self.numeroMesa = numeroMesa

    def procesar(self):
        print(f"Pedido en local #{self.numeroPedido} - Mesa {self.numeroMesa}")

class PedidoParaLlevar(Pedido):
    def __init__(self, numeroPedido, cliente, tiempoEstimadoRetiro, fecha=None, totalPagar=0):
        super().__init__(numeroPedido, cliente, fecha, totalPagar)
        self.tiempoEstimadoRetiro = tiempoEstimadoRetiro

    def procesar(self):
        print(f"Pedido para llevar #{self.numeroPedido} - Retiro en {self.tiempoEstimadoRetiro}")

class PedidoDespacho(Pedido):
    def __init__(self, numeroPedido, cliente, direccion, fecha=None, totalPagar=0):
        super().__init__(numeroPedido, cliente, fecha, totalPagar)
        self.direccion = direccion

    def procesar(self):
        print(f"Pedido despacho #{self.numeroPedido} - Dirección {self.direccion}")


class PedidoRepository:
    @staticmethod
    def crear(pedido: Pedido):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO PEDIDO (numeroPedido, id_cliente, fecha, totalPagar) VALUES (:num, :idc, SYSDATE, :tot)",
                        num=pedido.numeroPedido, idc=pedido.cliente.id_cliente, tot=pedido.totalPagar
                    )

                    if isinstance(pedido, PedidoEnLocal):
                        cur.execute("INSERT INTO PEDIDO_EN_LOCAL (numeroPedido, numeroMesa) VALUES (:n,:m)",
                                    n=pedido.numeroPedido, m=pedido.numeroMesa)

                    elif isinstance(pedido, PedidoParaLlevar):
                        cur.execute("INSERT INTO PEDIDO_PARA_LLEVAR (numeroPedido, tiempoEstimadoRetiro) VALUES (:n,:t)",
                                    n=pedido.numeroPedido, t=pedido.tiempoEstimadoRetiro)

                    elif isinstance(pedido, PedidoDespacho):
                        cur.execute("INSERT INTO PEDIDO_DESPACHO (numeroPedido, direccion) VALUES (:n,:d)",
                                    n=pedido.numeroPedido, d=pedido.direccion)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error creando pedido: {e}")

    @staticmethod
    def actualizar(pedido: Pedido):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE PEDIDO SET totalPagar=:t WHERE numeroPedido=:n",
                                t=pedido.totalPagar, n=pedido.numeroPedido)

                    if isinstance(pedido, PedidoEnLocal):
                        cur.execute("UPDATE PEDIDO_EN_LOCAL SET numeroMesa=:m WHERE numeroPedido=:n",
                                    m=pedido.numeroMesa, n=pedido.numeroPedido)

                    elif isinstance(pedido, PedidoParaLlevar):
                        cur.execute("UPDATE PEDIDO_PARA_LLEVAR SET tiempoEstimadoRetiro=:t WHERE numeroPedido=:n",
                                    t=pedido.tiempoEstimadoRetiro, n=pedido.numeroPedido)

                    elif isinstance(pedido, PedidoDespacho):
                        cur.execute("UPDATE PEDIDO_DESPACHO SET direccion=:d WHERE numeroPedido=:n",
                                    d=pedido.direccion, n=pedido.numeroPedido)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error actualizando pedido: {e}")

    @staticmethod
    def eliminar(n):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM PEDIDO_EN_LOCAL WHERE numeroPedido=:n", n=n)
                    cur.execute("DELETE FROM PEDIDO_PARA_LLEVAR WHERE numeroPedido=:n", n=n)
                    cur.execute("DELETE FROM PEDIDO_DESPACHO WHERE numeroPedido=:n", n=n)
                    cur.execute("DELETE FROM PEDIDO WHERE numeroPedido=:n", n=n)
                conn.commit()
        except oracledb.DatabaseError as e:
            raise DatabaseError(f"Error eliminando pedido: {e}")


# =====================================================
#                     MENÚ CRUD
# =====================================================

def menu():
    while True:
        print("""
================ MENU CRUD ================
1. Crear cliente
2. Actualizar cliente
3. Eliminar cliente
4. Listar clientes
5. Crear pedido
6. Actualizar pedido
7. Eliminar pedido
8. Listar pedidos
0. Salir
===========================================
        """)

        opc = input("Seleccione opción: ")

        if opc == "1":
            idc = input("ID cliente (puede tener guion): ")
            nom = input("Nombre: ")
            tel = input("Teléfono: ")
            cor = input("Correo: ")
            ClienteRepository.crear(Cliente(idc, nom, tel, cor))
            print("Cliente creado")

        elif opc == "2":
            idc = input("ID cliente a actualizar: ")
            nom = input("Nuevo nombre: ")
            tel = input("Nuevo teléfono: ")
            cor = input("Nuevo correo: ")
            ClienteRepository.actualizar(Cliente(idc, nom, tel, cor))
            print("Cliente actualizado")

        elif opc == "3":
            idc = input("ID cliente a eliminar: ")
            ClienteRepository.eliminar(idc)
            print("Cliente eliminado")

        elif opc == "4":
            clientes = ClienteRepository.listar_todos()
            for c in clientes:
                print(c)

        elif opc == "5":
            num = input("Número pedido: ")
            idc = input("ID cliente: ")
            cli = ClienteRepository.obtener_por_id(idc)
            if not cli:
                print("Cliente no existe")
                continue

            print("Tipo de pedido:")
            print("1. En local")
            print("2. Para llevar")
            print("3. Despacho")
            tp = input("Seleccione: ")

            tot = float(input("Total a pagar: "))

            if tp == "1":
                mesa = int(input("Número de mesa: "))
                PedidoRepository.crear(PedidoEnLocal(num, cli, mesa, totalPagar=tot))

            elif tp == "2":
                tie = input("Tiempo estimado: ")
                PedidoRepository.crear(PedidoParaLlevar(num, cli, tie, totalPagar=tot))

            elif tp == "3":
                dire = input("Dirección: ")
                PedidoRepository.crear(PedidoDespacho(num, cli, dire, totalPagar=tot))

            print("Pedido creado")

        elif opc == "6":
            num = input("Número de pedido a actualizar: ")
            pedido = PedidoRepository.obtener_por_id(num)
            if not pedido:
                print("No existe ese pedido")
                continue

            nuevo_total = float(input("Nuevo total: "))
            pedido.totalPagar = nuevo_total

            if isinstance(pedido, PedidoEnLocal):
                mesa = int(input("Nueva mesa: "))
                pedido.numeroMesa = mesa

            elif isinstance(pedido, PedidoParaLlevar):
                tie = input("Nuevo tiempo: ")
                pedido.tiempoEstimadoRetiro = tie

            else:
                dire = input("Nueva dirección: ")
                pedido.direccion = dire

            PedidoRepository.actualizar(pedido)
            print("Pedido actualizado")

        elif opc == "7":
            num = input("Número pedido a eliminar: ")
            PedidoRepository.eliminar(num)
            print("Pedido eliminado")

        elif opc == "8":
            pedidos = PedidoRepository.listar_todos()
            for p in pedidos:
                p.procesar()
                print(f"Total: {p.totalPagar}")

        elif opc == "0":
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
