-- ==============================================================================
-- SHOPYN GOLDEN STORE - ARQUITECTURA DE BASE DE DATOS MULTI-TENANT (SAAS)
-- Motor: PostgreSQL 14+ / 16
-- Modelo: Shared Database con Columna Discriminadora (tenant_id) + RLS Ready
-- Total de Tablas: 31 tablas (4 tablas SaaS Plataforma + 27 tablas del ERP)
-- Archivo: backend/database/schema_multitenant_completo.sql
-- ==============================================================================

-- 0. EXTENSIONES REQUERIDAS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================================================
-- BLOQUE 1: INFRAESTRUCTURA SAAS MULTI-TENANT (NIVEL PLATAFORMA / GLOBAL)
-- ==============================================================================

-- 1.1 Catálogo de Planes de Suscripción para las Boutiques
CREATE TABLE IF NOT EXISTS public.plan_suscripcion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,              -- 'Básico', 'Profesional', 'Enterprise'
    descripcion TEXT,
    precio_mensual NUMERIC(10, 2) NOT NULL,          -- Costo mensual en Bs. / USD
    limite_sucursales INTEGER NOT NULL DEFAULT 1,     -- Cantidad máx de sucursales permitidas
    limite_usuarios INTEGER NOT NULL DEFAULT 3,       -- Cantidad máx de empleados/usuarios
    limite_productos INTEGER NOT NULL DEFAULT 100,    -- Límite de catálogo de prendas
    habilitar_vestidor_ia BOOLEAN DEFAULT FALSE,      -- Acceso al vestidor virtual IA
    habilitar_facturacion BOOLEAN DEFAULT FALSE,      -- Módulo fiscal avanzado
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 1.2 Registro de Inquilinos / Boutiques / Empresas (Tenant)
CREATE TABLE IF NOT EXISTS public.tenant (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,                     -- Ej: 'Boutique Chiquitana S.R.L.'
    slug VARCHAR(60) UNIQUE NOT NULL,                 -- Ej: 'chiquitana' (subdominio: chiquitana.goldenstore.com)
    dominio_personalizado VARCHAR(150) UNIQUE,        -- Ej: 'tienda.chiquitana.com'
    nit_ruc VARCHAR(30),                              -- Identificación tributaria
    email_contacto VARCHAR(120) NOT NULL,
    telefono_contacto VARCHAR(30),
    direccion_fiscal TEXT,
    logo_url TEXT,
    plan_id INTEGER REFERENCES public.plan_suscripcion(id) ON UPDATE CASCADE,
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 1.3 Historial y Estado de Suscripciones por Tenant
CREATE TABLE IF NOT EXISTS public.tenant_suscripcion (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    plan_id INTEGER NOT NULL REFERENCES public.plan_suscripcion(id),
    fecha_inicio TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    estado VARCHAR(20) DEFAULT 'ACTIVA',              -- 'ACTIVA', 'GRACIA', 'VENCIDA', 'CANCELADA'
    monto_pagado NUMERIC(10, 2) NOT NULL,
    metodo_pago VARCHAR(50),                          -- 'QR_BANCO', 'TARJETA', 'TRANSFERENCIA'
    comprobante_url TEXT,
    notas TEXT
);

-- 1.4 Configuración y Parámetros Personalizados por Boutique
CREATE TABLE IF NOT EXISTS public.tenant_configuracion (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER UNIQUE NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    moneda_simbolo VARCHAR(10) DEFAULT 'Bs.',
    moneda_iso VARCHAR(5) DEFAULT 'BOB',
    zona_horaria VARCHAR(50) DEFAULT 'America/La_Paz',
    tiempo_expiracion_reserva_horas INTEGER DEFAULT 48, -- Horas para caducar reservas (CU10)
    color_primario_hex VARCHAR(10) DEFAULT '#0d1b2a',
    color_secundario_hex VARCHAR(10) DEFAULT '#d4af37',
    
    -- Pasarelas de Cobro por Boutique (CU16):
    paypal_client_id TEXT,
    paypal_client_secret TEXT,
    qr_banco_cuenta VARCHAR(60),
    qr_banco_alias VARCHAR(60),
    
    -- Integración de Notificaciones (CU19):
    whatsapp_notificaciones VARCHAR(30),
    email_notificaciones VARCHAR(120)
);

-- ==============================================================================
-- BLOQUE 2: SEGURIDAD, ROLES, SUCURSALES Y USUARIOS (TENANT-AWARE)
-- ==============================================================================

-- 2.1 Roles del Sistema (Pueden ser globales del sistema)
CREATE TABLE IF NOT EXISTS public.rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,               -- 'ADMIN', 'CLIENTE', 'ENCARGADO_SUCURSAL', 'CAJERO'
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- 2.2 Sucursales Físicas (Pertenece a cada Tenant)
CREATE TABLE IF NOT EXISTS public.sucursal (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(120) NOT NULL,
    ciudad VARCHAR(80),
    direccion VARCHAR(255),
    telefono VARCHAR(30),
    latitud NUMERIC(10, 7),
    longitud NUMERIC(10, 7),
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2.3 Cuentas de Usuario (Personal y Administradores por Tenant)
CREATE TABLE IF NOT EXISTS public.usuario (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(120) NOT NULL,
    passwordhash VARCHAR(255) NOT NULL,
    telefono VARCHAR(30),
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sucursalid INTEGER REFERENCES public.sucursal(id) ON DELETE SET NULL,
    rolid INTEGER REFERENCES public.rol(id) ON DELETE RESTRICT,
    verificado BOOLEAN DEFAULT FALSE,
    codigoverificacion VARCHAR(20),
    codigoexpiracion TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT uq_usuario_tenant_email UNIQUE (tenant_id, email)
);

-- 2.4 Clientes Registrados de la Tienda (Por Tenant)
CREATE TABLE IF NOT EXISTS public.cliente (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(120),
    telefono VARCHAR(30),
    fechanac DATE,
    genero VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecharegistro TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    usuarioid INTEGER REFERENCES public.usuario(id) ON DELETE SET NULL,
    CONSTRAINT uq_cliente_tenant_email UNIQUE (tenant_id, email)
);

-- ==============================================================================
-- BLOQUE 3: CATÁLOGO, ATRIBUTOS Y PRENDAS (TENANT-AWARE)
-- ==============================================================================

-- 3.1 Atributos Base Estándar (Globales para uniformidad de colores y tallas)
CREATE TABLE IF NOT EXISTS public.color (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    codigohex VARCHAR(10),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS public.talla (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,                      -- 'XS', 'S', 'M', 'L', 'XL', 'XXL'
    grupoedad VARCHAR(30),                            -- 'Adulto', 'Juvenil', 'Niños'
    orden INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE
);

-- 3.2 Clasificación de Prendas (Propias de cada Boutique)
CREATE TABLE IF NOT EXISTS public.categoria (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_categoria_tenant_nombre UNIQUE (tenant_id, nombre)
);

CREATE TABLE IF NOT EXISTS public.temporada (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fechainicio DATE,
    fechafin DATE,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS public.coleccion (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagenurl TEXT,
    activo BOOLEAN DEFAULT TRUE,
    temporadaid INTEGER REFERENCES public.temporada(id) ON DELETE SET NULL
);

-- 3.3 Catálogo de Prendas y Poleras (Propio de cada Boutique)
CREATE TABLE IF NOT EXISTS public.producto (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    marca VARCHAR(80),
    genero VARCHAR(30),                               -- 'Caballeros', 'Damas', 'Unisex'
    grupoedad VARCHAR(30),
    preciobase NUMERIC(10, 2) NOT NULL,
    imagenprincipal TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fechaactualizacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    categoriaid INTEGER REFERENCES public.categoria(id) ON DELETE SET NULL
);

-- 3.4 Variantes por Talla y Color de cada Prenda
CREATE TABLE IF NOT EXISTS public.variante_producto (
    id SERIAL PRIMARY KEY,
    productoid INTEGER NOT NULL REFERENCES public.producto(id) ON DELETE CASCADE,
    colorid INTEGER REFERENCES public.color(id) ON DELETE RESTRICT,
    tallaid INTEGER REFERENCES public.talla(id) ON DELETE RESTRICT,
    sku VARCHAR(60),
    codigobarra VARCHAR(80),
    imagenurl TEXT,
    precioventa NUMERIC(10, 2),
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3.5 Proveedores de Cada Tienda
CREATE TABLE IF NOT EXISTS public.proveedor (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    razonsocial VARCHAR(150),
    nit VARCHAR(30),
    contacto VARCHAR(100),
    telefono VARCHAR(30),
    email VARCHAR(120),
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.producto_proveedor (
    idproducto INTEGER NOT NULL REFERENCES public.producto(id) ON DELETE CASCADE,
    idproveedor INTEGER NOT NULL REFERENCES public.proveedor(id) ON DELETE CASCADE,
    costocompra NUMERIC(10, 2),
    cantidad INTEGER DEFAULT 0,
    PRIMARY KEY (idproducto, idproveedor)
);

-- ==============================================================================
-- BLOQUE 4: GESTIÓN DE STOCK E INVENTARIOS (TENANT-AWARE)
-- ==============================================================================

-- 4.1 Stock Centralizado por Sucursal y Variante
CREATE TABLE IF NOT EXISTS public.inventario (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    sucursalid INTEGER NOT NULL REFERENCES public.sucursal(id) ON DELETE CASCADE,
    varianteid INTEGER NOT NULL REFERENCES public.variante_producto(id) ON DELETE CASCADE,
    stockfisico INTEGER NOT NULL DEFAULT 0,
    stockreservado INTEGER NOT NULL DEFAULT 0,
    stockminimo INTEGER NOT NULL DEFAULT 5,
    fechaactualizacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_inventario_sucursal_variante UNIQUE (sucursalid, varianteid)
);

-- 4.2 Tabla de compatibilidad para CU08-CU11
CREATE TABLE IF NOT EXISTS public.inventario_sucursal (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    sucursalid INTEGER NOT NULL REFERENCES public.sucursal(id) ON DELETE CASCADE,
    varianteid INTEGER NOT NULL REFERENCES public.variante_producto(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL DEFAULT 0,
    stockreservado INTEGER DEFAULT 0,
    stockminimo INTEGER DEFAULT 5,
    fechaactualizacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4.3 Movimientos de Entrada, Salida y Ajuste (Kardex)
CREATE TABLE IF NOT EXISTS public.movimiento_inventario (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    inventarioid INTEGER NOT NULL REFERENCES public.inventario(id) ON DELETE CASCADE,
    usuarioid INTEGER NOT NULL REFERENCES public.usuario(id) ON DELETE RESTRICT,
    tipomovimiento VARCHAR(30) NOT NULL,             -- 'ENTRADA', 'SALIDA', 'AJUSTE', 'VENTA', 'RESERVA'
    cantidad INTEGER NOT NULL,
    motivo VARCHAR(255),
    referencia VARCHAR(100),
    fecha TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- BLOQUE 5: E-COMMERCE, CARRITO Y RESERVAS (TENANT-AWARE)
-- ==============================================================================

-- 5.1 Carrito de Compras Omnicanal
CREATE TABLE IF NOT EXISTS public.carrito (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    clienteid INTEGER NOT NULL REFERENCES public.usuario(id) ON DELETE CASCADE,
    sucursalid INTEGER REFERENCES public.sucursal(id) ON DELETE SET NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',     -- 'ACTIVO', 'PROCESADO', 'ABANDONADO'
    fechacreacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fechaactualizacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.carrito_item (
    id SERIAL PRIMARY KEY,
    carritoid INTEGER NOT NULL REFERENCES public.carrito(id) ON DELETE CASCADE,
    varianteid INTEGER NOT NULL REFERENCES public.variante_producto(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL DEFAULT 1,
    preciounitario NUMERIC(10, 2) NOT NULL,
    fechaagregado TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5.2 Reservas de Prendas en Tienda Física (CU10 - 48h)
CREATE TABLE IF NOT EXISTS public.reserva (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    codigoreserva VARCHAR(50) NOT NULL,
    clienteid INTEGER NOT NULL REFERENCES public.usuario(id) ON DELETE CASCADE,
    sucursalid INTEGER NOT NULL REFERENCES public.sucursal(id) ON DELETE RESTRICT,
    fechareserva TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',  -- 'PENDIENTE', 'CONFIRMADA', 'COMPLETADA', 'EXPIRADA', 'CANCELADA'
    observaciones TEXT,
    CONSTRAINT uq_reserva_tenant_codigo UNIQUE (tenant_id, codigoreserva)
);

CREATE TABLE IF NOT EXISTS public.reserva_detalle (
    id SERIAL PRIMARY KEY,
    reservaid INTEGER NOT NULL REFERENCES public.reserva(id) ON DELETE CASCADE,
    varianteid INTEGER NOT NULL REFERENCES public.variante_producto(id) ON DELETE RESTRICT,
    cantidad INTEGER NOT NULL DEFAULT 1
);

-- ==============================================================================
-- BLOQUE 6: VENTAS, PAGOS, COMPROBANTES Y AUDITORÍA (TENANT-AWARE)
-- ==============================================================================

-- 6.1 Métodos de Pago Disponibles (Catálogo Estándar)
CREATE TABLE IF NOT EXISTS public.metodo_pago (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,               -- 'EFECTIVO', 'TARJETA_DEBITO', 'TARJETA_CREDITO', 'PAGO_QR', 'PAYPAL'
    estado BOOLEAN DEFAULT TRUE
);

-- 6.2 Comprobantes / Recibos de Venta
CREATE TABLE IF NOT EXISTS public.recibo (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    nro_recibo VARCHAR(50),
    estado VARCHAR(30) NOT NULL DEFAULT 'EMITIDO',
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 6.3 Registro de Ventas (Presenciales y Digitales - CU14 & CU15)
CREATE TABLE IF NOT EXISTS public.venta (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    codigoventa VARCHAR(50) NOT NULL,
    tipoventa VARCHAR(30) NOT NULL,                   -- 'PRESENCIAL', 'DIGITAL_ECOMMERCE', 'DESDE_RESERVA'
    estado VARCHAR(30) NOT NULL DEFAULT 'PAGADA',     -- 'PENDIENTE', 'PAGADA', 'ANULADA'
    subtotal NUMERIC(10, 2) NOT NULL,
    descuento NUMERIC(10, 2) DEFAULT 0.00,
    total NUMERIC(10, 2) NOT NULL,
    fecha TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sucursalid INTEGER NOT NULL REFERENCES public.sucursal(id) ON DELETE RESTRICT,
    clienteid INTEGER REFERENCES public.cliente(id) ON DELETE SET NULL,
    usuarioid INTEGER NOT NULL REFERENCES public.usuario(id) ON DELETE RESTRICT,
    CONSTRAINT uq_venta_tenant_codigo UNIQUE (tenant_id, codigoventa)
);

CREATE TABLE IF NOT EXISTS public.detalle_venta (
    id SERIAL PRIMARY KEY,
    ventaid INTEGER NOT NULL REFERENCES public.venta(id) ON DELETE CASCADE,
    varianteid INTEGER NOT NULL REFERENCES public.variante_producto(id) ON DELETE RESTRICT,
    cantidad INTEGER NOT NULL DEFAULT 1,
    preciounitario NUMERIC(10, 2) NOT NULL,
    descuento NUMERIC(10, 2) DEFAULT 0.00,
    subtotal NUMERIC(10, 2) NOT NULL
);

-- 6.4 Transacciones de Pago (CU16)
CREATE TABLE IF NOT EXISTS public.pago (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    ventaid INTEGER NOT NULL REFERENCES public.venta(id) ON DELETE CASCADE,
    metodoid INTEGER NOT NULL REFERENCES public.metodo_pago(id) ON DELETE RESTRICT,
    reciboid INTEGER REFERENCES public.recibo(id) ON DELETE SET NULL,
    monto NUMERIC(10, 2) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'APROBADO',    -- 'APROBADO', 'PENDIENTE', 'RECHAZADO'
    referencia VARCHAR(100),                           -- Código de autorización o nro de transacción
    fecha TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6.5 Notificaciones del Sistema (CU19)
CREATE TABLE IF NOT EXISTS public.notificacion (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES public.usuario(id) ON DELETE CASCADE,
    titulo VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(50),                                  -- 'VENTA', 'RESERVA', 'STOCK_BAJO', 'SISTEMA'
    leido BOOLEAN DEFAULT FALSE,
    enlace VARCHAR(255),
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6.6 Bitácora y Auditoría de Acciones (CU20)
CREATE TABLE IF NOT EXISTS public.bitacora (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenant(id) ON DELETE CASCADE,
    usuarioid INTEGER REFERENCES public.usuario(id) ON DELETE SET NULL,
    accion VARCHAR(50) NOT NULL,                      -- 'LOGIN', 'CREAR', 'ACTUALIZAR', 'ELIMINAR'
    modulo VARCHAR(80) NOT NULL,                      -- 'VENTAS', 'INVENTARIO', 'USUARIOS', 'PRENDAS'
    detalle TEXT,
    ip VARCHAR(50),
    fechahora TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    datosprevios TEXT,
    datosnuevos TEXT
);

-- ==============================================================================
-- BLOQUE 7: ÍNDICES COMPUESTOS B-TREE PARA MÁXIMA VELOCIDAD MULTI-TENANT
-- ==============================================================================

CREATE INDEX IF NOT EXISTS idx_tenant_slug ON public.tenant(slug);
CREATE INDEX IF NOT EXISTS idx_tenant_dominio ON public.tenant(dominio_personalizado);
CREATE INDEX IF NOT EXISTS idx_usuario_tenant ON public.usuario(tenant_id, activo);
CREATE INDEX IF NOT EXISTS idx_cliente_tenant ON public.cliente(tenant_id, activo);
CREATE INDEX IF NOT EXISTS idx_producto_tenant_cat ON public.producto(tenant_id, categoriaid, activo);
CREATE INDEX IF NOT EXISTS idx_inventario_tenant_suc ON public.inventario(tenant_id, sucursalid);
CREATE INDEX IF NOT EXISTS idx_venta_tenant_fecha ON public.venta(tenant_id, fecha);
CREATE INDEX IF NOT EXISTS idx_reserva_tenant_estado ON public.reserva(tenant_id, estado);
CREATE INDEX IF NOT EXISTS idx_bitacora_tenant_fecha ON public.bitacora(tenant_id, fechahora);

-- ==============================================================================
-- BLOQUE 8: SEGURIDAD POSTGRESQL ROW LEVEL SECURITY (RLS READY)
-- ==============================================================================

-- Para activar el aislamiento nativo en PostgreSQL a nivel motor, ejecuta:
/*
ALTER TABLE public.sucursal ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usuario ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.producto ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.inventario ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.venta ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reserva ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_producto ON public.producto
    FOR ALL
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::integer)
    WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::integer);
*/

-- ==============================================================================
-- BLOQUE 9: DATOS SEMILLA (SEED DATA DEMOSTRATIVO CON 2 TENANTS REALES)
-- ==============================================================================

-- 9.1 Planes de la plataforma SaaS
INSERT INTO public.plan_suscripcion (id, nombre, descripcion, precio_mensual, limite_sucursales, limite_usuarios, limite_productos, habilitar_vestidor_ia)
VALUES 
(1, 'Básico Emprendedor', 'Para boutiques individuales que inician', 120.00, 1, 3, 50, FALSE),
(2, 'Profesional Retail', 'Para tiendas consolidadas con múltiples sucursales', 280.00, 3, 10, 500, TRUE),
(3, 'Enterprise Boutique', 'Para franquicias con sucursales ilimitadas y soporte prioritario', 600.00, 10, 50, 5000, TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.2 Tenants de Ejemplo
INSERT INTO public.tenant (id, uuid, nombre, slug, dominio_personalizado, nit_ruc, email_contacto, telefono_contacto, plan_id, activo)
VALUES 
(1, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Shopyn Golden Store Equipetrol', 'goldenstore', 'equipetrol.goldenstore.com', '1029384029', 'contacto@goldenstore.com', '70001122', 2, TRUE),
(2, 'b1ffcd88-8b1a-3de7-aa5c-5aa8ac270b22', 'Boutique Santa Cruz Chic', 'santacruzchic', 'santacruzchic.com', '2039485012', 'ventas@santacruzchic.com', '71112233', 1, TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.3 Configuración para cada Tenant
INSERT INTO public.tenant_configuracion (tenant_id, moneda_simbolo, tiempo_expiracion_reserva_horas, color_primario_hex, color_secundario_hex)
VALUES 
(1, 'Bs.', 48, '#0d1b2a', '#d4af37'),
(2, 'Bs.', 24, '#1a365d', '#319795')
ON CONFLICT (tenant_id) DO NOTHING;

-- 9.4 Roles Estándar
INSERT INTO public.rol (id, nombre, descripcion, activo)
VALUES 
(1, 'ADMIN', 'Administrador General de la Boutique', TRUE),
(2, 'CLIENTE', 'Cliente Final de la Tienda Online y Móvil', TRUE),
(3, 'ENCARGADO_SUCURSAL', 'Gestor de inventario y atención de reservas en tienda', TRUE),
(4, 'CAJERO', 'Operador de caja para ventas presenciales POS', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.5 Métodos de Pago Estándar
INSERT INTO public.metodo_pago (id, nombre, estado)
VALUES 
(1, 'EFECTIVO', TRUE),
(2, 'TARJETA_DEBITO', TRUE),
(3, 'TARJETA_CREDITO', TRUE),
(4, 'PAGO_QR', TRUE),
(5, 'PAYPAL', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.6 Colores y Tallas Estándar (Globales)
INSERT INTO public.color (id, nombre, codigohex, activo)
VALUES 
(1, 'Blanco Puro', '#FFFFFF', TRUE),
(2, 'Negro Ébano', '#000000', TRUE),
(3, 'Verde Oriente', '#007A3D', TRUE),
(4, 'Beige Chiquitano', '#D4B996', TRUE),
(5, 'Rojo Borgoña', '#800020', TRUE)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.talla (id, nombre, grupoedad, orden, activo)
VALUES 
(1, 'S', 'Adulto', 1, TRUE),
(2, 'M', 'Adulto', 2, TRUE),
(3, 'L', 'Adulto', 3, TRUE),
(4, 'XL', 'Adulto', 4, TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.7 Sucursales por Tenant
INSERT INTO public.sucursal (id, tenant_id, nombre, ciudad, direccion, telefono, activo)
VALUES 
(1, 1, 'Boutique Central Equipetrol', 'Santa Cruz', 'Av. San Martín esq. Calle 7', '70000001', TRUE),
(2, 1, 'Sucursal Mall Ventura', 'Santa Cruz', '4to Anillo, Nivel 2 Local 215', '70000002', TRUE),
(3, 2, 'Showroom Urbano Casco Viejo', 'Santa Cruz', 'Calle René Moreno #340', '71112233', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.8 Usuarios Administradores de cada Tenant (Clave hash: Admin123.)
INSERT INTO public.usuario (id, tenant_id, nombre, apellido, email, passwordhash, rolid, sucursalid, verificado, activo)
VALUES 
(1, 1, 'Admin', 'Golden Store', 'admin@goldenstore.com', '$2b$12$uLlXd1QDOKe8ZYVWuKv5VeUpEZ5EHTD/MOiFG4dKtLDZM/W4zo9K2', 1, 1, TRUE, TRUE),
(2, 2, 'Gerente', 'Santa Cruz Chic', 'admin@santacruzchic.com', '$2b$12$uLlXd1QDOKe8ZYVWuKv5VeUpEZ5EHTD/MOiFG4dKtLDZM/W4zo9K2', 1, 3, TRUE, TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.9 Categorías Aisladas por Tenant
INSERT INTO public.categoria (id, tenant_id, nombre, descripcion, activo)
VALUES 
(1, 1, 'Poleras Artesanales Chiquitanas', 'Poleras bordadas con hilo regional', TRUE),
(2, 1, 'Streetwear Oversize', 'Colección moderna urbana', TRUE),
(3, 2, 'Vestidos y Moda Femenina', 'Prendas de alta costura cruceña', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.10 Productos de Muestra Aislados por Tenant
INSERT INTO public.producto (id, tenant_id, nombre, marca, genero, preciobase, imagenprincipal, categoriaid, activo)
VALUES 
(1, 1, 'Polera Rústica con Bordado Tradicional', 'Boutique Collection', 'Unisex', 140.00, 'https://i.postimg.cc/bNrrzDw1/333.png', 1, TRUE),
(2, 2, 'Vestido Floreado Primavera Tropical', 'Santa Cruz Chic', 'Damas', 220.00, 'https://i.postimg.cc/VLvvYrk0/344.png', 3, TRUE)
ON CONFLICT (id) DO NOTHING;

-- 9.11 Sincronización final de secuencias SERIAL
SELECT setval('public.plan_suscripcion_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.plan_suscripcion));
SELECT setval('public.tenant_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.tenant));
SELECT setval('public.rol_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.rol));
SELECT setval('public.sucursal_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.sucursal));
SELECT setval('public.usuario_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.usuario));
SELECT setval('public.categoria_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.categoria));
SELECT setval('public.producto_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.producto));
SELECT setval('public.color_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.color));
SELECT setval('public.talla_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.talla));
SELECT setval('public.metodo_pago_id_seq', (SELECT COALESCE(MAX(id), 1) FROM public.metodo_pago));

-- ==============================================================================
-- FIN DEL SCRIPT DE BASE DE DATOS MULTI-TENANT
-- ==============================================================================
