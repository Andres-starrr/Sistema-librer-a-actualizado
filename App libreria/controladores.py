from tkinter import messagebox
from db import conectar_db
from Validaciones import validar_autor, validar_categoria, validar_libro, validar_cliente

# AUTORES
def guardar_autor(nombre, apellido, fecha_nacimiento, nacionalidad, biografia):
    if not validar_autor(nombre, apellido, fecha_nacimiento, nacionalidad, biografia):
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarAutor', [
            nombre, apellido, fecha_nacimiento or None, nacionalidad, biografia.strip()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Autor guardado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar autor:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_autor(id_autor, nombre, apellido, fecha_nacimiento, nacionalidad, biografia):
    if not id_autor:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarAutor', [
            int(id_autor), nombre, apellido, fecha_nacimiento or None, nacionalidad, biografia.strip()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Autor actualizado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_autor(id_autor):
    if not id_autor:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarAutor', [int(id_autor)])
        conexion.commit()
        messagebox.showinfo("Éxito", "Autor eliminado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# CATEGORÍAS
def guardar_categoria(nombre, descripcion):
    if not validar_categoria(nombre, descripcion):
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarCategoria', [nombre.strip(), descripcion.strip()])
        conexion.commit()
        messagebox.showinfo("Éxito", "Categoría guardada")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_categoria(id_categoria, nombre, descripcion):
    if not id_categoria:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarCategoria', [int(id_categoria), nombre.strip(), descripcion.strip()])
        conexion.commit()
        messagebox.showinfo("Éxito", "Categoría actualizada")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_categoria(id_categoria):
    if not id_categoria:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarCategoria', [int(id_categoria)])
        conexion.commit()
        messagebox.showinfo("Éxito", "Categoría eliminada")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# LIBROS
def guardar_libro(titulo, isbn, id_autor, id_categoria, precio, stock, fecha_publicacion):
    if not validar_libro(titulo, isbn, id_autor, id_categoria, precio, stock, fecha_publicacion):
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarLibro', [
            titulo, isbn, int(id_autor), int(id_categoria),
            float(precio), int(stock), fecha_publicacion or None
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro guardado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar libro:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_libro(id_libro, titulo, isbn, id_autor, id_categoria, precio, stock, fecha_publicacion):
    if not id_libro:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarLibro', [
            int(id_libro), titulo, isbn, int(id_autor), int(id_categoria),
            float(precio), int(stock), fecha_publicacion or None
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro actualizado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_libro(id_libro):
    if not id_libro:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarLibro', [int(id_libro)])
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro eliminado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# CLIENTES
def guardar_cliente(nombre, apellido, email, telefono, direccion):
    if not validar_cliente(nombre, apellido, email, telefono, direccion):
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarCliente', [
            nombre, apellido, email, telefono or None, direccion or None
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente guardado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar cliente:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_cliente(id_cliente, nombre, apellido, email, telefono, direccion):
    if not id_cliente:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarCliente', [
            int(id_cliente), nombre, apellido, email, telefono or None, direccion or None
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente actualizado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_cliente(id_cliente):
    if not id_cliente:
        messagebox.showwarning("Advertencia", "ID es requerido")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarCliente', [int(id_cliente)])
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente eliminado")
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# VENTAS
def guardar_venta(id_cliente, id_libro, cantidad, precio_unitario, fecha_venta):
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('RegistrarVenta', [
            int(id_cliente), int(id_libro), int(cantidad),
            float(precio_unitario), fecha_venta
        ])
        conexion.commit()
        for result in cursor.stored_results():
            msg = result.fetchone()[0]
            messagebox.showinfo("Éxito", msg)
    except Exception as e:
        if "Stock insuficiente" in str(e) or "1644" in str(e):
            messagebox.showerror("Error", "Stock insuficiente")
        else:
            messagebox.showerror("Error", f"Error en venta:\n{e}")
    finally:
        cursor.close()

        conexion.close()
