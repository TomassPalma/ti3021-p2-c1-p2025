import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

with oracledb.connect(user=username, password=password, dsn=dsn) as connection:
    with connection.cursor() as cursor:
        sql = "select sysdate from dual"
        resultado = cursor.execute(sql)
        for row in cursor.execute(sql):
            print("Fila",row,"\nCantidad de columnas",len(row))
            for column in row:
                print(column)