Sistema de Gestión para una Librería
Este proyecto es un sistema básico de gestión para una librería, desarrollado en Python con la biblioteca tkinter para la interfaz de usuario y mysql.connector para la conexión a una base de datos MySQL.

El sistema permite realizar operaciones CRUD (crear, Leer, Actualizar, Eliminar) en las siguientes entidades:

Autores: Gestión de información sobre los autores de los libros.
Categorías: Organización de libros por categorías.
Libros: Registro y control del inventario de libros.
Clientes: Almacenamiento de los datos de los clientes.
Ventas: Registro de transacciones de venta, con lógica de negocio para la gestión de stock.
Contenido del Repositorio
DB libreria.sql: Archivo SQL con el esquema de la base de datos (CREATE TABLE).
Store Pro.sql: Archivo SQL con los procedimientos almacenados (CREATE PROCEDURE) utilizados para realizar las operaciones de la aplicación.
Sistema libreria.py: El script principal de Python que ejecuta la interfaz gráfica y se conecta a la base de datos para interactuar con ella.
Requisitos
Para poder ejecutar este proyecto, necesitas tener instalados los siguientes componentes:

Python 3.x: O otra version referente El lenguaje de programación.
MySQL Server: El sistema de gestión de bases de datos. Se debe INICIAR XAMPP PARA ESTABLECER CONEXION
Bibliotecas de Python:
tkinter: Generalmente viene incluido en la instalación de Python.
mysql-connector-python: Para conectar Python con MySQL. Puedes instalarlo usando pip:
pip install mysql-connector-python
Configuración y Uso
Configuración de la Base de Datos:

Asegúrate de que tu servidor MySQL esté en ejecución.
Importa el archivo DB libreria.sql en tu servidor MySQL para crear la base de datos y las tablas necesarias.
Importa el archivo Store Pro.sql para crear todos los procedimientos almacenados.
Verifica que los datos de conexión en el archivo Sistema libreria.py (líneas 21-25) coincidan con la configuración de tu base de datos local (host, user, password, database).
Ejecutar la Aplicación:

Abre una terminal o línea de comandos.
Navega al directorio donde se encuentra el archivo Sistema libreria.py.
Ejecuta el script de Python:
python "Sistema libreria.py"
Ahora puedes empezar a usar la aplicación para gestionar autores, categorías, libros, clientes y ventas de tu librería.

Procedimientos Almacenados Destacados
El sistema utiliza procedimientos almacenados para garantizar la integridad y el control de las operaciones, especialmente en el módulo de ventas. El procedimiento RegistrarVenta incluye la siguiente lógica de negocio:

Calcula el total de la venta automáticamente.
Verifica el stock del libro antes de registrar la venta.
Si hay suficiente stock, registra la venta y disminuye la cantidad del libro en el inventario.
Si el stock es insuficiente, lanza un mensaje de error.

Por ultimo se debe descargar la imagen para el fondo e icono en formato ico, las imagenes del repositorio se deben guardar en la misma carpeta donde se encuentra el codigo de PYTHON
