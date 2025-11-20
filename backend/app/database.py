import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="reservas_ucu"
    )


def close_connection(cursor, conn) -> None:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

