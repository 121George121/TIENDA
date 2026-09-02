-- ==============================================================================
-- BASE DE DATOS: ECOMMERCE_TIENDA (PostgreSQL)
-- Modelo Relacional de la Tienda Virtual
-- ==============================================================================

-- 1. TABLA: Roles de usuario
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA: Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT REFERENCES roles(id) ON DELETE SET NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABLA: Categorías de Productos
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. TABLA: Productos
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria_id INT REFERENCES categorias(id) ON DELETE CASCADE,
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. TABLA: Pedidos / Órdenes
CREATE TABLE IF NOT EXISTS ordenes (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    total DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'PENDIENTE', -- PENDIENTE, PAGADO, ENVIADO, CANCELADO
    direccion_envio TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. TABLA: Detalle de Pedido (Items)
CREATE TABLE IF NOT EXISTS orden_detalles (
    id SERIAL PRIMARY KEY,
    orden_id INT REFERENCES ordenes(id) ON DELETE CASCADE,
    producto_id INT REFERENCES productos(id) ON DELETE RESTRICT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- ==============================================================================
-- DATOS INICIALES (SEMILLA)
-- ==============================================================================
INSERT INTO roles (nombre, descripcion) VALUES
('ADMIN', 'Administrador total del sistema'),
('CLIENTE', 'Cliente comprador de la tienda')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO categorias (nombre, descripcion) VALUES
('Electrónica', 'Dispositivos tecnológicos, accesorios y gadgets'),
('Ropa y Moda', 'Prendas de vestir masculinas y femeninas'),
('Hogar', 'Artículos para decoración y cocina')
ON CONFLICT DO NOTHING;

INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id, imagen_url) VALUES
('Laptop Gamer Pro', 'Laptop de alto rendimiento 16GB RAM SSD 1TB', 1250.00, 10, 1, 'https://images.unsplash.com/photo-1603302576837-37561b2e2302'),
('Audífonos Bluetooth', 'Audífonos inalámbricos con cancelación de ruido', 85.50, 25, 1, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e'),
('Polera Casual Algodón', 'Polera 100% algodón lavable', 25.00, 50, 2, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518')
ON CONFLICT DO NOTHING;
