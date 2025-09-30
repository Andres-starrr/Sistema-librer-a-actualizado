import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import re
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.geometry('800x600')
root.title("FORMULARIO SISTEMA LIBRERÍA")
root.iconbitmap("dragon.ico")

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(root)

# Crear los frames que irán dentro de las pestañas
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)

# Añadir las pestañas al Notebook
notebook.add(tab1, text="Autores")
notebook.add(tab2, text="Categorías")
notebook.add(tab3, text="Libros")
notebook.add(tab4, text="Clientes")
notebook.add(tab5, text="Ventas")

# Empaquetar el Notebook
notebook.pack(expand=True, fill="both")

def aplicar_fondo_a_pestaña(pestaña, ruta_imagen, ancho=800, alto=600):
    try:
        # Cargar y redimensionar la imagen
        imagen = Image.open("fondo.ico")
        imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(imagen)

        # Crear un Label que actúe como fondo
        fondo_label = tk.Label(pestaña, image=photo)
        fondo_label.image = photo
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        return fondo_label
    except Exception as e:
        print(f"Error al cargar fondo para {ruta_imagen}: {e}")
        return None

# Aplicar fondos (usa tus propias imágenes)
aplicar_fondo_a_pestaña(tab1, "fondo_autores.jpg")
aplicar_fondo_a_pestaña(tab2, "fondo_categorias.jpg")
aplicar_fondo_a_pestaña(tab3, "fondo_libros.jpg")
aplicar_fondo_a_pestaña(tab4, "fondo_clientes.jpg")
aplicar_fondo_a_pestaña(tab5, "fondo_ventas.jpg")

# CONEXIÓN A LA BASE DE DATOS
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='libreria_db',
            user='root',
            password=''
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print("ERROR DE CONEXIÓN:")
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return None


# FUNCIÓN PARA CONVERTIR RGB A HEX
def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def validar_email(email):
    #Validar el correo electronico
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_id(valor):
    #Validar el ID
    if not valor:
        return False
    try:
        id_num = int(valor)
        return id_num > 0
    except ValueError:
        return False

def validar_numero_positivo(valor, permitir_decimal=False):
    #Validar numeros positivos
    if not valor:
        return False
    try:
        if permitir_decimal:
            num = float(valor)
        else:
            num = int(valor)
        return num >= 0
    except ValueError:
        return False

# FUNCIONES PARA LIMPIAR
def limpiar_autores():
    id_autor.delete(0, tk.END)
    nombre_autor.delete(0, tk.END)
    apellido_autor.delete(0, tk.END)
    fecha_nacimiento.delete(0, tk.END)
    nacionalidad.delete(0, tk.END)
    biografia.delete(1.0, tk.END)
    messagebox.showinfo("Éxito", "La información ha sido limpiada con éxito")

def limpiar_categorias():
    id_categoria.delete(0, tk.END)
    nombre_categoria.delete(0, tk.END)
    descripcion_categoria.delete(1.0, tk.END)
    messagebox.showinfo("Éxito", "La información ha sido limpiada con éxito")

def limpiar_libros():
    id_libro.delete(0, tk.END)
    titulo_libro.delete(0, tk.END)
    isbn.delete(0, tk.END)
    id_autor_libro.delete(0, tk.END)
    id_categoria_libro.delete(0, tk.END)
    precio.delete(0, tk.END)
    stock.delete(0, tk.END)
    fecha_publicacion.delete(0, tk.END)
    messagebox.showinfo("Éxito", "La información ha sido limpiada con éxito")

def limpiar_clientes():
    id_cliente.delete(0, tk.END)
    nombre_cliente.delete(0, tk.END)
    apellido_cliente.delete(0, tk.END)
    email.delete(0, tk.END)
    telefono.delete(0, tk.END)
    direccion.delete(0, tk.END)
    messagebox.showinfo("Éxito", "La información ha sido limpiada con éxito")

def limpiar_ventas():
    id_venta.delete(0, tk.END)
    id_cliente_venta.delete(0, tk.END)
    id_libro_venta.delete(0, tk.END)
    cantidad.delete(0, tk.END)
    precio_unitario.delete(0, tk.END)
    total.delete(0, tk.END)
    fecha_venta.delete(0, tk.END)
    messagebox.showinfo("Éxito", "La información ha sido limpiada con éxito")


# FUNCIONES CRUD - AUTORES
def guardar_autor():
    if not nombre_autor.get().strip():
        messagebox.showwarning("Advertencia", "El campo 'Nombre' es obligatorio.")
        return
    if not apellido_autor.get().strip():
        messagebox.showwarning("Advertencia", "El campo 'Apellido' es obligatorio.")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarAutor', [
            nombre_autor.get(),
            apellido_autor.get(),
            fecha_nacimiento.get() or None,
            nacionalidad.get(),
            biografia.get("1.0", tk.END).strip()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Autor guardado correctamente")
        limpiar_autores()
        cargar_tabla_autores()

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar autor:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_autor():
    if not id_autor.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID del autor a actualizar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarAutor', [
            int(id_autor.get()),
            nombre_autor.get(),
            apellido_autor.get(),
            fecha_nacimiento.get() or None,
            nacionalidad.get(),
            biografia.get("1.0", tk.END).strip()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Autor actualizado correctamente")
        limpiar_autores()
        cargar_tabla_autores()

    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar autor:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_autor():
    if not id_autor.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID del autor a eliminar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarAutor', [int(id_autor.get())])
        conexion.commit()
        messagebox.showinfo("Éxito", "Autor eliminado correctamente")
        limpiar_autores()
        cargar_tabla_autores()

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar autor:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# FUNCIONES CRUD - CATEGORÍAS
def guardar_categoria():
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarCategoria', [
            nombre_categoria.get(),
            descripcion_categoria.get("1.0", tk.END).strip()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Categoría guardada correctamente")
        limpiar_categorias()
        cargar_tabla_categorias()

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar categoría:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_categoria():
    if not id_categoria.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID de la categoría a actualizar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarCategoria', [
            int(id_categoria.get()),
            nombre_categoria.get(),
            descripcion_categoria.get("1.0", tk.END).strip()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
        limpiar_categorias()
        cargar_tabla_categorias()

    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar categoría:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_categoria():
    if not id_categoria.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID de la categoría a eliminar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarCategoria', [int(id_categoria.get())])
        conexion.commit()
        messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
        limpiar_categorias()
        cargar_tabla_categorias()

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar categoría:\n{e}")
    finally:
        cursor.close()
        conexion.close()


# FUNCIONES CRUD - LIBROS
def guardar_libro():
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarLibro', [
            titulo_libro.get(),
            isbn.get(),
            int(id_autor_libro.get()),
            int(id_categoria_libro.get()),
            float(precio.get()),
            int(stock.get()),
            fecha_publicacion.get() or None
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro guardado correctamente")
        limpiar_libros()
        cargar_tabla_libros()

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar libro:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_libro():
    if not id_libro.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID del libro a actualizar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarLibro', [
            int(id_libro.get()),
            titulo_libro.get(),
            isbn.get(),
            int(id_autor_libro.get()),
            int(id_categoria_libro.get()),
            float(precio.get()),
            int(stock.get()),
            fecha_publicacion.get() or None
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro actualizado correctamente")
        limpiar_libros()
        cargar_tabla_libros()

    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar libro:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_libro():
    if not id_libro.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID del libro a eliminar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarLibro', [int(id_libro.get())])
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro eliminado correctamente")
        limpiar_libros()
        cargar_tabla_libros
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar libro:\n{e}")
    finally:
        cursor.close()
        conexion.close()


# FUNCIONES CRUD - CLIENTES
def guardar_cliente():
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('InsertarCliente', [
            nombre_cliente.get(),
            apellido_cliente.get(),
            email.get(),
            telefono.get(),
            direccion.get()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente guardado correctamente")
        limpiar_clientes()
        cargar_tabla_clientes()

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar cliente:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_cliente():
    if not id_cliente.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID del cliente a actualizar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('ActualizarCliente', [
            int(id_cliente.get()),
            nombre_cliente.get(),
            apellido_cliente.get(),
            email.get(),
            telefono.get(),
            direccion.get()
        ])
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        limpiar_clientes()
        cargar_tabla_clientes()

    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar cliente:\n{e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_cliente():
    if not id_cliente.get():
        messagebox.showwarning("Advertencia", "Debes ingresar el ID del cliente a eliminar")
        return
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('EliminarCliente', [int(id_cliente.get())])
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
        limpiar_clientes()
        cargar_tabla_clientes()

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar cliente:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# FUNCIÓN PARA CREAR BOTONES
def crear_botones(parent_tab, clear_command, save_command=None, update_command=None, delete_command=None):
    button_frame = tk.Frame(parent_tab)
    button_frame.pack(pady=20)

    if save_command:
        btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="blue", fg="white", width=10,
                             command=save_command)
        btn_save.pack(side=tk.LEFT, padx=5)

    if update_command:
        btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="blue", fg="white", width=10,
                               command=update_command)
        btn_update.pack(side=tk.LEFT, padx=5)

    if delete_command:
        btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="blue", fg="white", width=10,
                               command=delete_command)
        btn_delete.pack(side=tk.LEFT, padx=5)

    btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="blue", fg="white", width=10,
                          command=clear_command)
    btn_clear.pack(side=tk.LEFT, padx=5)


# BOTONES VENTAS
def guardar_venta():
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.callproc('RegistrarVenta', [
            int(id_cliente_venta.get()),
            int(id_libro_venta.get()),
            int(cantidad.get()),
            float(precio_unitario.get()),
            fecha_venta.get()
        ])
        conexion.commit()

        for result in cursor.stored_results():
            mensaje = result.fetchone()[0]
            messagebox.showinfo("Éxito", mensaje)

        limpiar_ventas()

    except mysql.connector.Error as e:
        if e.errno == 1644:
            messagebox.showerror("Error", "Stock insuficiente para realizar la venta")
        else:
            messagebox.showerror("Error", f"Error al registrar venta:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{e}")
    finally:
        cursor.close()
        conexion.close()

crear_botones(tab5, limpiar_ventas, guardar_venta)

# Función para cargar autores
def cargar_tabla_autores():
    # Limpiar tabla existente
    for item in tree_autores.get_children():
        tree_autores.delete(item)

    conexion = conectar_db()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_autor, nombre, apellido, fecha_nacimiento, nacionalidad FROM autores")
        autores = cursor.fetchall()
        for autor in autores:
            tree_autores.insert("", "end", values=autor)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar autores:\n{e}")
    finally:
        cursor.close()
        conexion.close()

# Función para cargar categorias
def cargar_tabla_categorias():
    # Limpiar tabla existente
    for item in tree_categorias.get_children():
        tree_categorias.delete(item)

    conexion = conectar_db()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre, descripcion FROM categorias")
        for row in cursor.fetchall():
            tree_categorias.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar autores:\n{e}")
    finally:
        cursor.close()
        conexion.close()

#Funcion para cargar libros
def cargar_tabla_libros():
    for item in tree_libros.get_children():
        tree_libros.delete(item)
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_libro, titulo, isbn, id_autor, id_categoria, precio, stock, fecha_publicacion 
            FROM libros
        """)
        for row in cursor.fetchall():
            tree_libros.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar libros:\n{e}")
    finally:
        cursor.close()
        conexion.close()

#Funcion para cargar clientes
def cargar_tabla_clientes():
    for item in tree_clientes.get_children():
        tree_clientes.delete(item)
    conexion = conectar_db()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_cliente, nombre, apellido, email, telefono, direccion FROM clientes")
        for row in cursor.fetchall():
            tree_clientes.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar clientes:\n{e}")
    finally:
        cursor.close()
        conexion.close()


# INTERFAZ: PESTAÑA 1 - AUTORES
titulo1 = tk.Label(tab1, text="GESTIÓN DE AUTORES", font=("Arial", 16, "bold"), fg=rgb_to_hex(0, 0, 255))
titulo1.pack(pady=30)

form_frame1 = tk.Frame(tab1)
form_frame1.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame1, text="ID Autor:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_autor = tk.Entry(form_frame1, width=25, font=("Arial", 12), relief="solid", bd=1)
id_autor.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame1, text="Nombre:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
nombre_autor = tk.Entry(form_frame1, width=25, font=("Arial", 12), relief="solid", bd=1)
nombre_autor.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame1, text="Apellido:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
apellido_autor = tk.Entry(form_frame1, width=25, font=("Arial", 12), relief="solid", bd=1)
apellido_autor.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame1, text="Fecha Nacimiento:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
fecha_nacimiento = tk.Entry(form_frame1, width=25, font=("Arial", 12), relief="solid", bd=1)
fecha_nacimiento.grid(row=4, column=1, sticky="w", pady=10)

tk.Label(form_frame1, text="Nacionalidad:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
nacionalidad = tk.Entry(form_frame1, width=25, font=("Arial", 12), relief="solid", bd=1)
nacionalidad.grid(row=5, column=1, sticky="w", pady=10)

tk.Label(form_frame1, text="Biografía:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
biografia = tk.Text(form_frame1, width=25, height=3, font=("Arial", 10), relief="solid", bd=1)
biografia.grid(row=6, column=1, sticky="w", pady=10)

crear_botones(tab1, limpiar_autores, guardar_autor, actualizar_autor, eliminar_autor)

# Tabla para mostrar autores
frame_tabla1 = tk.Frame(tab1)
frame_tabla1.pack(fill="both", expand=True, padx=20, pady=10)

columns1 = ("ID", "Nombre", "Apellido", "Fecha Nac.", "Nacionalidad")
tree_autores = ttk.Treeview(frame_tabla1, columns=columns1, show="headings")

# Configurar encabezados
for col in columns1:
    tree_autores.heading(col, text=col)
    tree_autores.column(col, width=120)

tree_autores.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar1 = ttk.Scrollbar(frame_tabla1, orient="vertical", command=tree_autores.yview)
tree_autores.configure(yscroll=scrollbar1.set)
scrollbar1.pack(side="right", fill="y")

# Cargar datos al iniciar
cargar_tabla_autores()

# INTERFAZ: PESTAÑA 2 - CATEGORÍAS
titulo2 = tk.Label(tab2, text="GESTIÓN DE CATEGORÍAS", font=("Arial", 16, "bold"), fg=rgb_to_hex(0, 0, 255))
titulo2.pack(pady=30)

form_frame2 = tk.Frame(tab2)
form_frame2.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame2, text="ID Categoría:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_categoria = tk.Entry(form_frame2, width=25, font=("Arial", 12), relief="solid", bd=1)
id_categoria.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame2, text="Nombre:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
nombre_categoria = tk.Entry(form_frame2, width=25, font=("Arial", 12), relief="solid", bd=1)
nombre_categoria.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame2, text="Descripción:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
descripcion_categoria = tk.Text(form_frame2, width=25, height=4, font=("Arial", 10), relief="solid", bd=1)
descripcion_categoria.grid(row=3, column=1, sticky="w", pady=10)

crear_botones(tab2, limpiar_categorias, guardar_categoria, actualizar_categoria, eliminar_categoria)

frame_tabla2 = tk.Frame(tab2)
frame_tabla2.pack(fill="both", expand=True, padx=20, pady=10)

columns2 = ("ID", "Nombre", "Descripción")
tree_categorias = ttk.Treeview(frame_tabla2, columns=columns2, show="headings")
for col in columns2:
    tree_categorias.heading(col, text=col)
    tree_categorias.column(col, width=150)
tree_categorias.pack(side="left", fill="both", expand=True)

scrollbar2 = ttk.Scrollbar(frame_tabla2, orient="vertical", command=tree_categorias.yview)
tree_categorias.configure(yscroll=scrollbar2.set)
scrollbar2.pack(side="right", fill="y")

cargar_tabla_categorias()

# INTERFAZ: PESTAÑA 3 - LIBROS
titulo3 = tk.Label(tab3, text="GESTIÓN DE LIBROS", font=("Arial", 16, "bold"), fg=rgb_to_hex(0, 0, 255))
titulo3.pack(pady=30)

form_frame3 = tk.Frame(tab3)
form_frame3.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame3, text="ID Libro:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_libro = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
id_libro.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="Título:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
titulo_libro = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
titulo_libro.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="ISBN:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
isbn = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
isbn.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="ID Autor:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
id_autor_libro = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
id_autor_libro.grid(row=4, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="ID Categoría:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
id_categoria_libro = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
id_categoria_libro.grid(row=5, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="Precio:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
precio = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
precio.grid(row=6, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="Stock:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
stock = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
stock.grid(row=7, column=1, sticky="w", pady=10)

tk.Label(form_frame3, text="Fecha Publicación:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=10)
fecha_publicacion = tk.Entry(form_frame3, width=25, font=("Arial", 12), relief="solid", bd=1)
fecha_publicacion.grid(row=8, column=1, sticky="w", pady=10)

crear_botones(tab3, limpiar_libros, guardar_libro, actualizar_libro, eliminar_libro)

# Tabla Libros
frame_tabla3 = tk.Frame(tab3)
frame_tabla3.pack(fill="both", expand=True, padx=20, pady=10)

columns3 = ("ID", "Título", "ISBN", "ID Autor", "ID Categoría", "Precio", "Stock", "Fecha Pub.")
tree_libros = ttk.Treeview(frame_tabla3, columns=columns3, show="headings")
for col in columns3:
    tree_libros.heading(col, text=col)
    tree_libros.column(col, width=100)
tree_libros.column("Título", width=180)
tree_libros.pack(side="left", fill="both", expand=True)

scrollbar3 = ttk.Scrollbar(frame_tabla3, orient="vertical", command=tree_libros.yview)
tree_libros.configure(yscroll=scrollbar3.set)
scrollbar3.pack(side="right", fill="y")

cargar_tabla_libros()

# INTERFAZ: PESTAÑA 4 - CLIENTES
titulo4 = tk.Label(tab4, text="GESTIÓN DE CLIENTES", font=("Arial", 16, "bold"), fg=rgb_to_hex(0, 0, 255))
titulo4.pack(pady=30)

form_frame4 = tk.Frame(tab4)
form_frame4.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame4, text="ID Cliente:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_cliente = tk.Entry(form_frame4, width=25, font=("Arial", 12), relief="solid", bd=1)
id_cliente.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame4, text="Nombre:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
nombre_cliente = tk.Entry(form_frame4, width=25, font=("Arial", 12), relief="solid", bd=1)
nombre_cliente.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame4, text="Apellido:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
apellido_cliente = tk.Entry(form_frame4, width=25, font=("Arial", 12), relief="solid", bd=1)
apellido_cliente.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame4, text="Email:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
email = tk.Entry(form_frame4, width=25, font=("Arial", 12), relief="solid", bd=1)
email.grid(row=4, column=1, sticky="w", pady=10)

tk.Label(form_frame4, text="Teléfono:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
telefono = tk.Entry(form_frame4, width=25, font=("Arial", 12), relief="solid", bd=1)
telefono.grid(row=5, column=1, sticky="w", pady=10)

tk.Label(form_frame4, text="Dirección:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
direccion = tk.Entry(form_frame4, width=25, font=("Arial", 12), relief="solid", bd=1)
direccion.grid(row=6, column=1, sticky="w", pady=10)

crear_botones(tab4, limpiar_clientes, guardar_cliente, actualizar_cliente, eliminar_cliente)

# Tabla Clientes
frame_tabla4 = tk.Frame(tab4)
frame_tabla4.pack(fill="both", expand=True, padx=20, pady=10)

columns4 = ("ID", "Nombre", "Apellido", "Email", "Teléfono", "Dirección")
tree_clientes = ttk.Treeview(frame_tabla4, columns=columns4, show="headings")
for col in columns4:
    tree_clientes.heading(col, text=col)
    tree_clientes.column(col, width=120)
tree_clientes.column("Dirección", width=200)
tree_clientes.pack(side="left", fill="both", expand=True)

scrollbar4 = ttk.Scrollbar(frame_tabla4, orient="vertical", command=tree_clientes.yview)
tree_clientes.configure(yscroll=scrollbar4.set)
scrollbar4.pack(side="right", fill="y")

cargar_tabla_clientes()

# INTERFAZ: PESTAÑA 5 - VENTAS
titulo5 = tk.Label(tab5, text="GESTIÓN DE VENTAS", font=("Arial", 16, "bold"), fg=rgb_to_hex(0, 0, 255))
titulo5.pack(pady=30)

form_frame5 = tk.Frame(tab5)
form_frame5.pack(pady=20, anchor="w", padx=50)

tk.Label(form_frame5, text="ID Venta:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_venta = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
id_venta.grid(row=1, column=1, sticky="w", pady=10)

tk.Label(form_frame5, text="ID Cliente:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
id_cliente_venta = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
id_cliente_venta.grid(row=2, column=1, sticky="w", pady=10)

tk.Label(form_frame5, text="ID Libro:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
id_libro_venta = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
id_libro_venta.grid(row=3, column=1, sticky="w", pady=10)

tk.Label(form_frame5, text="Cantidad:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
cantidad = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
cantidad.grid(row=4, column=1, sticky="w", pady=10)

tk.Label(form_frame5, text="Precio Unitario:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
precio_unitario = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
precio_unitario.grid(row=5, column=1, sticky="w", pady=10)

tk.Label(form_frame5, text="Total:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
total = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
total.grid(row=6, column=1, sticky="w", pady=10)

tk.Label(form_frame5, text="Fecha Venta:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
fecha_venta = tk.Entry(form_frame5, width=25, font=("Arial", 12), relief="solid", bd=1)
fecha_venta.grid(row=7, column=1, sticky="w", pady=10)

# EJECUTAR LA APLICACIÓN
root.mainloop()
