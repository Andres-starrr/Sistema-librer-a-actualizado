📚 Sistema de Gestión para una Librería
Este proyecto es un sistema de gestión integral para una librería, desarrollado en Python con una interfaz gráfica intuitiva y conexión a una base de datos relacional. Permite administrar autores, categorías, libros, clientes y ventas de forma eficiente y segura.

Interfaz del sistema
(Ejemplo visual: asegúrate de incluir una captura de pantalla en tu repositorio)

🔧 Funcionalidades
El sistema implementa operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las siguientes entidades:

Autores: Gestión de información personal y biográfica.
Categorías: Organización temática de los libros.
Libros: Registro detallado con ISBN, precio, stock y relación con autor/categoría.
Clientes: Almacenamiento de datos de contacto y dirección.
Ventas: Registro de transacciones con lógica de negocio integrada:
Cálculo automático del total.
Verificación de stock disponible.
Actualización automática del inventario tras cada venta.
Mensaje de error si el stock es insuficiente.
🗃️ Contenido del Repositorio
DB libreria.sql: Esquema de la base de datos (tablas y relaciones).
Store Pro.sql: Procedimientos almacenados para operaciones seguras y eficientes.
Sistema libreria.py: Script principal con la interfaz gráfica (Tkinter) y lógica de la aplicación.
dragon.ico: Ícono personalizado para la ventana de la aplicación.
fondo_libros.jpg (u otras imágenes de fondo): Imágenes para la interfaz visual.
📌 Importante: Todas las imágenes (dragon.ico, fondo_libros.jpg, etc.) deben guardarse en la misma carpeta que Sistema libreria.py. 

⚙️ Requisitos
Para ejecutar este proyecto, necesitas:

Python 3.x (con tkinter incluido).
Servidor MySQL (recomendado: XAMPP para entornos locales).
Bibliotecas de Python:
bash


1
2
pip install mysql-connector-python
pip install Pillow  # Solo si usas imágenes en el formulario de autores
🚀 Configuración y Uso
1. Configurar la base de datos
Inicia XAMPP y asegúrate de que el módulo MySQL esté activo.
Importa DB libreria.sql en phpMyAdmin (o tu cliente MySQL) para crear la base de datos libreria_db.
Importa Store Pro.sql para crear los procedimientos almacenados.
2. Verificar conexión
Abre Sistema libreria.py y confirma que los parámetros de conexión coincidan con tu entorno (por defecto: localhost, usuario root, sin contraseña):

python


1
2
3
4
5
6
conexion = mysql.connector.connect(
    host='localhost',
    database='libreria_db',
    user='root',
    password=''
)
3. Ejecutar la aplicación
En tu terminal, navega a la carpeta del proyecto y ejecuta:

bash


1
python "Sistema libreria.py"
💡 Características Técnicas Destacadas
Interfaz multi-pestañas con diseño limpio y funcional.
Validaciones en tiempo real:
Formato de correo electrónico.
IDs numéricos positivos.
Precios y cantidades válidas.
Seguridad y rendimiento mediante el uso de procedimientos almacenados.
Gestión de imágenes (opcional): Soporte para fotos de autores.
Fondos personalizados por pestaña para una experiencia visual atractiva.

Por ultimo se debe descargar la imagen para el fondo e icono en formato ico, las imagenes del repositorio se deben guardar en la misma carpeta donde se encuentra el codigo de PYTHON
