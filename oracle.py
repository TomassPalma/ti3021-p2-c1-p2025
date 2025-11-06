import oracledb
import os
from dotenv import load_dotenv

load_dotenv(

username = os.dotenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

with oracledb.connect(user=username, password = password, dsn=dsn) as connection:
    with connection.cursor() as cursor:
        for r in cursor.execute(sql):
            print(r)