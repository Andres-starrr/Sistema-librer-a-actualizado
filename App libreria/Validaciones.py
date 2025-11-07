from tkinter import messagebox
import re

# VALIDACIONES

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        messagebox.showwarning("Validación", "El correo electrónico no tiene un formato válido.")
        return False
    return True

def validar_numero_positivo(valor, permitir_decimal=False):
    try:
        if permitir_decimal:
            num = float(valor)
        else:
            num = int(valor)
        if num < 0:
            messagebox.showwarning("Validación", "El valor debe ser un número positivo.")
            return False
        return True
    except:
        messagebox.showwarning("Validación", "Debes ingresar un número válido.")
        return False

def validar_id(valor):
    try:
        num = int(valor)
        if num <= 0:
            messagebox.showwarning("Validación", "El ID debe ser mayor a cero.")
            return False
        return True
    except:
        messagebox.showwarning("Validación", "El ID debe ser numérico.")
        return False

def solo_letras(valor, campo):
    if not valor.replace(" ", "").isalpha():
        messagebox.showwarning("Validación", f"El campo '{campo}' solo debe contener letras.")
        return False
    return True

# MODULO AUTORES

def validar_autor(nombre, apellido, fecha, nacionalidad, biografia):
    if len(nombre.strip()) < 2 or not solo_letras(nombre, "Nombre Autor"):
        return False
    if len(apellido.strip()) < 2 or not solo_letras(apellido, "Apellido Autor"):
        return False
    if nacionalidad.strip() == "" or not solo_letras(nacionalidad, "Nacionalidad"):
        return False
    if biografia.strip() != "" and len(biografia.strip()) < 10:
        messagebox.showwarning("Validación", "Biografía debe tener mínimo 10 caracteres si no está vacía.")
        return False
    return True

# MODULO CATEGORIAS

def validar_categoria(nombre, descripcion):
    if len(nombre.strip()) < 3 or not solo_letras(nombre, "Nombre Categoría"):
        return False
    if descripcion.strip() != "" and len(descripcion.strip()) < 10:
        messagebox.showwarning("Validación", "La descripción debe tener mínimo 10 caracteres si no está vacía.")
        return False
    return True

# MODULO LIBROS

def validar_libro(titulo, isbn, idAutor, idCategoria, precio, stock, fechaPub):
    if len(titulo.strip()) < 3:
        messagebox.showwarning("Validación", "El título debe tener mínimo 3 caracteres.")
        return False
    if not (len(isbn) == 10 or len(isbn) == 13) or not isbn.isdigit():
        messagebox.showwarning("Validación", "ISBN debe ser de 10 o 13 dígitos numéricos.")
        return False
    if not validar_id(idAutor):
        return False
    if not validar_id(idCategoria):
        return False
    if not validar_numero_positivo(precio, permitir_decimal=True):
        return False
    if not validar_numero_positivo(stock):
        return False
    if fechaPub.strip() == "":
        messagebox.showwarning("Validación", "La fecha de publicación es obligatoria.")
        return False
    return True

# MODULO CLIENTES

def validar_cliente(nombre, apellido, email, telefono, direccion):
    if len(nombre.strip()) < 2 or not solo_letras(nombre, "Nombre Cliente"):
        return False
    if len(apellido.strip()) < 2 or not solo_letras(apellido, "Apellido Cliente"):
        return False
    if not validar_email(email):
        return False
    if not telefono.isdigit() or len(telefono) < 7 or len(telefono) > 10:
        messagebox.showwarning("Validación", "Teléfono debe ser numérico y tener entre 7 y 10 dígitos.")
        return False
    if len(direccion.strip()) < 5:
        messagebox.showwarning("Validación", "La dirección debe tener mínimo 5 caracteres.")
        return False
    return True
