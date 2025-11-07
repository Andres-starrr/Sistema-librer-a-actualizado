import mysql.connector
from tkinter import messagebox

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="libreria_db"
        )
        return conexion
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return None
