-- ==============================================================================
-- BASE DE DATOS: ECOMMERCE_TIENDA (PostgreSQL)
-- Ubicacion: backend/database/init.sql
-- Generado con: pg_dump --schema-only sobre la base de datos real del proyecto
-- ==============================================================================

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: carrito; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.carrito (
    id integer NOT NULL,
    estado character varying(50) NOT NULL,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fechaactualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    clienteid integer NOT NULL,
    sucursalid integer
);


--
-- Name: carrito_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.carrito_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: carrito_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.carrito_id_seq OWNED BY public.carrito.id;


--
-- Name: carrito_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.carrito_item (
    carritoid integer NOT NULL,
    varianteid integer NOT NULL,
    cantidad integer NOT NULL,
    preciounitario numeric(12,2) NOT NULL,
    fechaagregado timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: categoria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categoria (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    activo boolean DEFAULT true NOT NULL
);


--
-- Name: categoria_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categoria_id_seq OWNED BY public.categoria.id;


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cliente (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100),
    email character varying(150),
    telefono character varying(20),
    fechanac date,
    genero character varying(30),
    activo boolean DEFAULT true NOT NULL,
    fecharegistro timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    usuarioid integer
);


--
-- Name: cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;


--
-- Name: coleccion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.coleccion (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    imagenurl text,
    activo boolean DEFAULT true NOT NULL,
    temporadaid integer NOT NULL
);


--
-- Name: coleccion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.coleccion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: coleccion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.coleccion_id_seq OWNED BY public.coleccion.id;


--
-- Name: color; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.color (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    codigohex character varying(10),
    activo boolean DEFAULT true NOT NULL
);


--
-- Name: color_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.color_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: color_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.color_id_seq OWNED BY public.color.id;


--
-- Name: detalle_venta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.detalle_venta (
    ventaid integer NOT NULL,
    varianteid integer NOT NULL,
    cantidad integer NOT NULL,
    preciounitario numeric(12,2) NOT NULL,
    descuento numeric(12,2) DEFAULT 0,
    subtotal numeric(12,2) NOT NULL
);


--
-- Name: direccioncliente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.direccioncliente (
    id integer NOT NULL,
    direccion character varying(250) NOT NULL,
    referencia character varying(200),
    ciudad character varying(100),
    departamento character varying(100),
    telefono character varying(20),
    esprincipal boolean DEFAULT false NOT NULL,
    activo boolean DEFAULT true NOT NULL,
    clienteid integer NOT NULL
);


--
-- Name: direccioncliente_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.direccioncliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: direccioncliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.direccioncliente_id_seq OWNED BY public.direccioncliente.id;


--
-- Name: evento_cliente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evento_cliente (
    id integer NOT NULL,
    tipoevento character varying(100) NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    metadata jsonb,
    clienteid integer NOT NULL,
    varianteid integer NOT NULL
);


--
-- Name: evento_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.evento_cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: evento_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.evento_cliente_id_seq OWNED BY public.evento_cliente.id;


--
-- Name: inventario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventario (
    id integer NOT NULL,
    stockfisico integer DEFAULT 0 NOT NULL,
    stockreservado integer DEFAULT 0 NOT NULL,
    stockminimo integer DEFAULT 0 NOT NULL,
    fechaactualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    sucursalid integer NOT NULL,
    varianteid integer NOT NULL
);


--
-- Name: inventario_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventario_id_seq OWNED BY public.inventario.id;


--
-- Name: metodo_pago; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.metodo_pago (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    estado boolean DEFAULT true NOT NULL
);


--
-- Name: metodo_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.metodo_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: metodo_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.metodo_pago_id_seq OWNED BY public.metodo_pago.id;


--
-- Name: movimiento_inventario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.movimiento_inventario (
    id integer NOT NULL,
    tipomovimiento character varying(50) NOT NULL,
    cantidad integer NOT NULL,
    motivo character varying(200),
    referencia character varying(100),
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    inventarioid integer NOT NULL,
    usuarioid integer NOT NULL
);


--
-- Name: movimiento_inventario_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.movimiento_inventario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: movimiento_inventario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.movimiento_inventario_id_seq OWNED BY public.movimiento_inventario.id;


--
-- Name: pago; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pago (
    id integer NOT NULL,
    monto numeric(12,2) NOT NULL,
    estado character varying(50) NOT NULL,
    referencia character varying(150),
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ventaid integer NOT NULL,
    reciboid integer,
    metodoid integer NOT NULL
);


--
-- Name: pago_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pago_id_seq OWNED BY public.pago.id;


--
-- Name: producto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.producto (
    id integer NOT NULL,
    nombre character varying(150) NOT NULL,
    descripcion text,
    marca character varying(100),
    genero character varying(50),
    grupoedad character varying(50),
    preciobase numeric(12,2) NOT NULL,
    imagenprincipal text,
    activo boolean DEFAULT true NOT NULL,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fechaactualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    categoriaid integer NOT NULL
);


--
-- Name: producto_coleccion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.producto_coleccion (
    idproducto integer NOT NULL,
    idcoleccion integer NOT NULL,
    cantidad integer
);


--
-- Name: producto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.producto_id_seq OWNED BY public.producto.id;


--
-- Name: producto_proveedor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.producto_proveedor (
    idproducto integer NOT NULL,
    idproveedor integer NOT NULL,
    costocompra numeric(12,2),
    cantidad integer
);


--
-- Name: proveedor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.proveedor (
    id integer NOT NULL,
    nombre character varying(150) NOT NULL,
    razonsocial character varying(200),
    nit character varying(50),
    contacto character varying(150),
    telefono character varying(20),
    email character varying(150),
    direccion character varying(250),
    activo boolean DEFAULT true NOT NULL,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: proveedor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.proveedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: proveedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.proveedor_id_seq OWNED BY public.proveedor.id;


--
-- Name: prueba_virtual; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prueba_virtual (
    id integer NOT NULL,
    imagenresultadourl text,
    dispositivo character varying(100),
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    clienteid integer NOT NULL,
    varianteid integer NOT NULL
);


--
-- Name: prueba_virtual_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prueba_virtual_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prueba_virtual_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prueba_virtual_id_seq OWNED BY public.prueba_virtual.id;


--
-- Name: recibo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recibo (
    id integer NOT NULL,
    estado character varying(50) NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: recibo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.recibo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: recibo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.recibo_id_seq OWNED BY public.recibo.id;


--
-- Name: reserva; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reserva (
    id integer NOT NULL,
    codigoreserva character varying(100) NOT NULL,
    fechareserva timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado character varying(50) NOT NULL,
    observaciones text,
    sucursalid integer NOT NULL,
    clienteid integer NOT NULL
);


--
-- Name: reserva_detalle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reserva_detalle (
    varianteid integer NOT NULL,
    reservaid integer NOT NULL,
    cantidad integer NOT NULL
);


--
-- Name: reserva_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reserva_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reserva_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reserva_id_seq OWNED BY public.reserva.id;


--
-- Name: rol; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rol (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    activo boolean DEFAULT true NOT NULL
);


--
-- Name: rol_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rol_id_seq OWNED BY public.rol.id;


--
-- Name: sucursal; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sucursal (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    ciudad character varying(100),
    direccion character varying(200),
    telefono character varying(20),
    latitud numeric(10,7),
    longitud numeric(10,7),
    activo boolean DEFAULT true NOT NULL,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: sucursal_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sucursal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sucursal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sucursal_id_seq OWNED BY public.sucursal.id;


--
-- Name: talla; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.talla (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    grupoedad character varying(50),
    orden integer,
    activo boolean DEFAULT true NOT NULL
);


--
-- Name: talla_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.talla_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: talla_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.talla_id_seq OWNED BY public.talla.id;


--
-- Name: temporada; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.temporada (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    fechainicio date,
    fechafin date,
    activo boolean DEFAULT true NOT NULL
);


--
-- Name: temporada_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.temporada_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: temporada_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.temporada_id_seq OWNED BY public.temporada.id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100),
    email character varying(150) NOT NULL,
    passwordhash character varying(255) NOT NULL,
    telefono character varying(20),
    activo boolean DEFAULT true NOT NULL,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    sucursalid integer,
    rolid integer NOT NULL,
    verificado boolean DEFAULT true,
    codigoverificacion character varying(255),
    codigoexpiracion timestamp without time zone
);


--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- Name: variante_producto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.variante_producto (
    id integer NOT NULL,
    codigobarra character varying(100),
    imagenurl text,
    precioventa numeric(12,2) NOT NULL,
    activo boolean DEFAULT true,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    sku character varying(100),
    productoid integer NOT NULL,
    colorid integer NOT NULL,
    tallaid integer NOT NULL
);


--
-- Name: variante_producto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.variante_producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: variante_producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.variante_producto_id_seq OWNED BY public.variante_producto.id;


--
-- Name: venta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.venta (
    id integer NOT NULL,
    codigoventa character varying(100) NOT NULL,
    tipoventa character varying(50) NOT NULL,
    estado character varying(50) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    descuento numeric(12,2) DEFAULT 0,
    total numeric(12,2) NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    sucursalid integer NOT NULL,
    clienteid integer NOT NULL,
    usuarioid integer NOT NULL
);


--
-- Name: venta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.venta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.venta_id_seq OWNED BY public.venta.id;


--
-- Name: carrito id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito ALTER COLUMN id SET DEFAULT nextval('public.carrito_id_seq'::regclass);


--
-- Name: categoria id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categoria ALTER COLUMN id SET DEFAULT nextval('public.categoria_id_seq'::regclass);


--
-- Name: cliente id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);


--
-- Name: coleccion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coleccion ALTER COLUMN id SET DEFAULT nextval('public.coleccion_id_seq'::regclass);


--
-- Name: color id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.color ALTER COLUMN id SET DEFAULT nextval('public.color_id_seq'::regclass);


--
-- Name: direccioncliente id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccioncliente ALTER COLUMN id SET DEFAULT nextval('public.direccioncliente_id_seq'::regclass);


--
-- Name: evento_cliente id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evento_cliente ALTER COLUMN id SET DEFAULT nextval('public.evento_cliente_id_seq'::regclass);


--
-- Name: inventario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario ALTER COLUMN id SET DEFAULT nextval('public.inventario_id_seq'::regclass);


--
-- Name: metodo_pago id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metodo_pago ALTER COLUMN id SET DEFAULT nextval('public.metodo_pago_id_seq'::regclass);


--
-- Name: movimiento_inventario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario ALTER COLUMN id SET DEFAULT nextval('public.movimiento_inventario_id_seq'::regclass);


--
-- Name: pago id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago ALTER COLUMN id SET DEFAULT nextval('public.pago_id_seq'::regclass);


--
-- Name: producto id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto ALTER COLUMN id SET DEFAULT nextval('public.producto_id_seq'::regclass);


--
-- Name: proveedor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proveedor ALTER COLUMN id SET DEFAULT nextval('public.proveedor_id_seq'::regclass);


--
-- Name: prueba_virtual id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prueba_virtual ALTER COLUMN id SET DEFAULT nextval('public.prueba_virtual_id_seq'::regclass);


--
-- Name: recibo id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recibo ALTER COLUMN id SET DEFAULT nextval('public.recibo_id_seq'::regclass);


--
-- Name: reserva id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva ALTER COLUMN id SET DEFAULT nextval('public.reserva_id_seq'::regclass);


--
-- Name: rol id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rol ALTER COLUMN id SET DEFAULT nextval('public.rol_id_seq'::regclass);


--
-- Name: sucursal id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sucursal ALTER COLUMN id SET DEFAULT nextval('public.sucursal_id_seq'::regclass);


--
-- Name: talla id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.talla ALTER COLUMN id SET DEFAULT nextval('public.talla_id_seq'::regclass);


--
-- Name: temporada id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.temporada ALTER COLUMN id SET DEFAULT nextval('public.temporada_id_seq'::regclass);


--
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- Name: variante_producto id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto ALTER COLUMN id SET DEFAULT nextval('public.variante_producto_id_seq'::regclass);


--
-- Name: venta id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta ALTER COLUMN id SET DEFAULT nextval('public.venta_id_seq'::regclass);


--
-- Name: carrito_item carrito_item_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito_item
    ADD CONSTRAINT carrito_item_pkey PRIMARY KEY (carritoid, varianteid);


--
-- Name: carrito carrito_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_pkey PRIMARY KEY (id);


--
-- Name: categoria categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (id);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- Name: coleccion coleccion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coleccion
    ADD CONSTRAINT coleccion_pkey PRIMARY KEY (id);


--
-- Name: color color_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.color
    ADD CONSTRAINT color_pkey PRIMARY KEY (id);


--
-- Name: detalle_venta detalle_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_pkey PRIMARY KEY (ventaid, varianteid);


--
-- Name: direccioncliente direccioncliente_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccioncliente
    ADD CONSTRAINT direccioncliente_pkey PRIMARY KEY (id);


--
-- Name: evento_cliente evento_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evento_cliente
    ADD CONSTRAINT evento_cliente_pkey PRIMARY KEY (id);


--
-- Name: inventario inventario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_pkey PRIMARY KEY (id);


--
-- Name: metodo_pago metodo_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metodo_pago
    ADD CONSTRAINT metodo_pago_pkey PRIMARY KEY (id);


--
-- Name: movimiento_inventario movimiento_inventario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario
    ADD CONSTRAINT movimiento_inventario_pkey PRIMARY KEY (id);


--
-- Name: pago pago_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id);


--
-- Name: producto_coleccion producto_coleccion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_coleccion
    ADD CONSTRAINT producto_coleccion_pkey PRIMARY KEY (idproducto, idcoleccion);


--
-- Name: producto producto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (id);


--
-- Name: producto_proveedor producto_proveedor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_proveedor
    ADD CONSTRAINT producto_proveedor_pkey PRIMARY KEY (idproducto, idproveedor);


--
-- Name: proveedor proveedor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_pkey PRIMARY KEY (id);


--
-- Name: prueba_virtual prueba_virtual_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prueba_virtual
    ADD CONSTRAINT prueba_virtual_pkey PRIMARY KEY (id);


--
-- Name: recibo recibo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recibo
    ADD CONSTRAINT recibo_pkey PRIMARY KEY (id);


--
-- Name: reserva_detalle reserva_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva_detalle
    ADD CONSTRAINT reserva_detalle_pkey PRIMARY KEY (varianteid, reservaid);


--
-- Name: reserva reserva_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id);


--
-- Name: rol rol_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id);


--
-- Name: sucursal sucursal_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sucursal
    ADD CONSTRAINT sucursal_pkey PRIMARY KEY (id);


--
-- Name: talla talla_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.talla
    ADD CONSTRAINT talla_pkey PRIMARY KEY (id);


--
-- Name: temporada temporada_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.temporada
    ADD CONSTRAINT temporada_pkey PRIMARY KEY (id);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: variante_producto variante_producto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_pkey PRIMARY KEY (id);


--
-- Name: venta venta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_pkey PRIMARY KEY (id);


--
-- Name: carrito carrito_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: carrito_item carrito_item_carritoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito_item
    ADD CONSTRAINT carrito_item_carritoid_fkey FOREIGN KEY (carritoid) REFERENCES public.carrito(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: carrito_item carrito_item_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito_item
    ADD CONSTRAINT carrito_item_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: carrito carrito_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: cliente cliente_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: coleccion coleccion_temporadaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coleccion
    ADD CONSTRAINT coleccion_temporadaid_fkey FOREIGN KEY (temporadaid) REFERENCES public.temporada(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: detalle_venta detalle_venta_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: detalle_venta detalle_venta_ventaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_ventaid_fkey FOREIGN KEY (ventaid) REFERENCES public.venta(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: direccioncliente direccioncliente_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccioncliente
    ADD CONSTRAINT direccioncliente_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: evento_cliente evento_cliente_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evento_cliente
    ADD CONSTRAINT evento_cliente_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: evento_cliente evento_cliente_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evento_cliente
    ADD CONSTRAINT evento_cliente_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: inventario inventario_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: inventario inventario_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: movimiento_inventario movimiento_inventario_inventarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario
    ADD CONSTRAINT movimiento_inventario_inventarioid_fkey FOREIGN KEY (inventarioid) REFERENCES public.inventario(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: movimiento_inventario movimiento_inventario_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario
    ADD CONSTRAINT movimiento_inventario_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: pago pago_metodoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_metodoid_fkey FOREIGN KEY (metodoid) REFERENCES public.metodo_pago(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: pago pago_reciboid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_reciboid_fkey FOREIGN KEY (reciboid) REFERENCES public.recibo(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: pago pago_ventaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_ventaid_fkey FOREIGN KEY (ventaid) REFERENCES public.venta(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: producto producto_categoriaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_categoriaid_fkey FOREIGN KEY (categoriaid) REFERENCES public.categoria(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: producto_coleccion producto_coleccion_idcoleccion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_coleccion
    ADD CONSTRAINT producto_coleccion_idcoleccion_fkey FOREIGN KEY (idcoleccion) REFERENCES public.coleccion(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: producto_coleccion producto_coleccion_idproducto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_coleccion
    ADD CONSTRAINT producto_coleccion_idproducto_fkey FOREIGN KEY (idproducto) REFERENCES public.producto(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: producto_proveedor producto_proveedor_idproducto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_proveedor
    ADD CONSTRAINT producto_proveedor_idproducto_fkey FOREIGN KEY (idproducto) REFERENCES public.producto(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: producto_proveedor producto_proveedor_idproveedor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_proveedor
    ADD CONSTRAINT producto_proveedor_idproveedor_fkey FOREIGN KEY (idproveedor) REFERENCES public.proveedor(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: prueba_virtual prueba_virtual_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prueba_virtual
    ADD CONSTRAINT prueba_virtual_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: prueba_virtual prueba_virtual_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prueba_virtual
    ADD CONSTRAINT prueba_virtual_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: reserva reserva_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: reserva_detalle reserva_detalle_reservaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva_detalle
    ADD CONSTRAINT reserva_detalle_reservaid_fkey FOREIGN KEY (reservaid) REFERENCES public.reserva(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: reserva_detalle reserva_detalle_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva_detalle
    ADD CONSTRAINT reserva_detalle_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: reserva reserva_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: usuario usuario_rolid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_rolid_fkey FOREIGN KEY (rolid) REFERENCES public.rol(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: usuario usuario_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: variante_producto variante_producto_colorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_colorid_fkey FOREIGN KEY (colorid) REFERENCES public.color(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: variante_producto variante_producto_productoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_productoid_fkey FOREIGN KEY (productoid) REFERENCES public.producto(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: variante_producto variante_producto_tallaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_tallaid_fkey FOREIGN KEY (tallaid) REFERENCES public.talla(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: venta venta_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: venta venta_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: venta venta_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--




-- ==============================================================================
-- DATOS INICIALES (SEMILLA)
-- Roles reales usados por la aplicacion (auth_controller.py busca el rol
-- "Cliente" al registrar; cliente_service.py filtra usuarios por este rol).
-- ==============================================================================
INSERT INTO public.rol (id, nombre, descripcion, activo) VALUES
(1, 'Administrador', 'Control total del sistema, seguridad y configuracion gerencial', true),
(2, 'Supervisor', 'Supervision de inventario de prendas, aprobacion de compras y personal', true),
(3, 'Cajero', 'Procesamiento de facturacion, punto de venta (POS) y cobros en tienda', true),
(4, 'Cliente', 'Acceso a catalogo de poleras, carrito de compras y reservas online', true)
ON CONFLICT (id) DO NOTHING;

-- Sincroniza la secuencia tras el seed con id explicito (evita choques de
-- llave primaria en el primer INSERT hecho por la API tras un setup limpio).
SELECT setval('public.rol_id_seq', (SELECT MAX(id) FROM public.rol), true);

