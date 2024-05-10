from decouple import config
import psycopg2
from psycopg2 import DatabaseError

def get_connection():
    try:
        return psycopg2.connect(
            host=config('PG_HOST'),
            user=config('PG_USER'),
            password=config('PG_PASSWORD'),
            database=config('PG_DATABASE')
        )
    except DatabaseError as ex:
        print("Error durante la conexión: {}".format(ex))
        return None

try:
    connection = get_connection()

    if connection is not None:
        print("Conexión exitosa.")
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        row = cursor.fetchone()
        print("Versión del servidor de PostgreSQL: {}".format(row))
        cursor.execute("SELECT * FROM jugadores")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
except DatabaseError as ex:
    print("Error durante la conexión: {}".format(ex))
finally:
    if connection is not None:
        connection.close()  # Se cerró la conexión a la BD.
        print("La conexión ha finalizado.")