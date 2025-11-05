from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error

app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="reservas_ucu"
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/facultades")
def get_facultades():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM facultad;")
        facultades = cursor.fetchall()
        return facultades
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()