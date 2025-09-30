DELIMITER //
-- Insertar Autor
CREATE PROCEDURE InsertarAutor(
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_fecha_nacimiento DATE,
    IN p_nacionalidad VARCHAR(100),
    IN p_biografia TEXT
)
BEGIN
    INSERT INTO autores (nombre, apellido, fecha_nacimiento, nacionalidad, biografia)
    VALUES (p_nombre, p_apellido, p_fecha_nacimiento, p_nacionalidad, p_biografia);
END//

-- Actualizar Autor
CREATE PROCEDURE ActualizarAutor(
    IN p_id_autor INT,
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_fecha_nacimiento DATE,
    IN p_nacionalidad VARCHAR(100),
    IN p_biografia TEXT
)
BEGIN
    UPDATE autores
    SET nombre = p_nombre,
        apellido = p_apellido,
        fecha_nacimiento = p_fecha_nacimiento,
        nacionalidad = p_nacionalidad,
        biografia = p_biografia
    WHERE id_autor = p_id_autor;
END//

-- Eliminar Autor
CREATE PROCEDURE EliminarAutor(IN p_id_autor INT)
BEGIN
    DELETE FROM autores WHERE id_autor = p_id_autor;
END//

-- ===================================================================
-- CATEGORÍAS
-- ===================================================================

-- Insertar Categoría
CREATE PROCEDURE InsertarCategoria(
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    INSERT INTO categorias (nombre, descripcion)
    VALUES (p_nombre, p_descripcion);
END//

-- Actualizar Categoría
CREATE PROCEDURE ActualizarCategoria(
    IN p_id_categoria INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT
)
BEGIN
    UPDATE categorias
    SET nombre = p_nombre,
        descripcion = p_descripcion
    WHERE id_categoria = p_id_categoria;
END//

-- Eliminar Categoría
CREATE PROCEDURE EliminarCategoria(IN p_id_categoria INT)
BEGIN
    DELETE FROM categorias WHERE id_categoria = p_id_categoria;
END//

-- ===================================================================
-- LIBROS
-- ===================================================================

-- Insertar Libro
CREATE PROCEDURE InsertarLibro(
    IN p_titulo VARCHAR(255),
    IN p_isbn VARCHAR(20),
    IN p_id_autor INT,
    IN p_id_categoria INT,
    IN p_precio DECIMAL(10,2),
    IN p_stock INT,
    IN p_fecha_publicacion DATE
)
BEGIN
    INSERT INTO libros (titulo, isbn, id_autor, id_categoria, precio, stock, fecha_publicacion)
    VALUES (p_titulo, p_isbn, p_id_autor, p_id_categoria, p_precio, p_stock, p_fecha_publicacion);
END//

-- Actualizar Libro
CREATE PROCEDURE ActualizarLibro(
    IN p_id_libro INT,
    IN p_titulo VARCHAR(255),
    IN p_isbn VARCHAR(20),
    IN p_id_autor INT,
    IN p_id_categoria INT,
    IN p_precio DECIMAL(10,2),
    IN p_stock INT,
    IN p_fecha_publicacion DATE
)
BEGIN
    UPDATE libros
    SET titulo = p_titulo,
        isbn = p_isbn,
        id_autor = p_id_autor,
        id_categoria = p_id_categoria,
        precio = p_precio,
        stock = p_stock,
        fecha_publicacion = p_fecha_publicacion
    WHERE id_libro = p_id_libro;
END$$

-- Eliminar Libro
CREATE PROCEDURE EliminarLibro(IN p_id_libro INT)
BEGIN
    DELETE FROM libros WHERE id_libro = p_id_libro;
END//

-- ===================================================================
-- CLIENTES
-- ===================================================================

-- Insertar Cliente
CREATE PROCEDURE InsertarCliente(
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_email VARCHAR(150),
    IN p_telefono VARCHAR(20),
    IN p_direccion VARCHAR(255)
)
BEGIN
    INSERT INTO clientes (nombre, apellido, email, telefono, direccion)
    VALUES (p_nombre, p_apellido, p_email, p_telefono, p_direccion);
END//

-- Actualizar Cliente
CREATE PROCEDURE ActualizarCliente(
    IN p_id_cliente INT,
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_email VARCHAR(150),
    IN p_telefono VARCHAR(20),
    IN p_direccion VARCHAR(255)
)
BEGIN
    UPDATE clientes
    SET nombre = p_nombre,
        apellido = p_apellido,
        email = p_email,
        telefono = p_telefono,
        direccion = p_direccion
    WHERE id_cliente = p_id_cliente;
END//

-- Eliminar Cliente
CREATE PROCEDURE EliminarCliente(IN p_id_cliente INT)
BEGIN
    DELETE FROM clientes WHERE id_cliente = p_id_cliente;
END//

-- ===================================================================
-- VENTAS (con lógica de negocio: cálculo de total y control de stock)
-- ===================================================================

CREATE PROCEDURE RegistrarVenta(
    IN p_id_cliente INT,
    IN p_id_libro INT,
    IN p_cantidad INT,
    IN p_precio_unitario DECIMAL(10,2),
    IN p_fecha_venta DATE
)
BEGIN
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_stock_actual INT;

    -- Calcular total
    SET v_total = p_cantidad * p_precio_unitario;

    -- Verificar stock
    SELECT stock INTO v_stock_actual FROM libros WHERE id_libro = p_id_libro;

    IF v_stock_actual >= p_cantidad THEN
        -- Registrar venta
        INSERT INTO ventas (id_cliente, id_libro, cantidad, precio_unitario, total, fecha_venta)
        VALUES (p_id_cliente, p_id_libro, p_cantidad, p_precio_unitario, v_total, p_fecha_venta);

        -- Reducir stock
        UPDATE libros
        SET stock = stock - p_cantidad
        WHERE id_libro = p_id_libro;

        SELECT 'Venta registrada con éxito' AS mensaje;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente para realizar la venta';
    END IF;
END//

DELIMITER ;