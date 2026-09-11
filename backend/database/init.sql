-- ==============================================================================
-- BASE DE DATOS: ECOMMERCE_TIENDA (PostgreSQL)
-- Ubicación: backend/database/init.sql
-- ==============================================================================

-- 1. TABLA: rol
CREATE TABLE IF NOT EXISTS rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- 2. TABLA: usuario
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    passwordhash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    verificado BOOLEAN DEFAULT TRUE,
    codigoverificacion VARCHAR(255),
    codigoexpiracion TIMESTAMP,
    fechacreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sucursalid INT,
    rolid INT REFERENCES rol(id) ON DELETE SET NULL
);

-- ==============================================================================
-- DATOS INICIALES (SEMILLA)
-- ==============================================================================
INSERT INTO rol (nombre, descripcion, activo) VALUES
('ADMIN', 'Administrador total del sistema', true),
('CLIENTE', 'Cliente comprador de la tienda', true)
ON CONFLICT (nombre) DO NOTHING;
