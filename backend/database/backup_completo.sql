--
-- PostgreSQL database dump
--


-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.venta DROP CONSTRAINT IF EXISTS venta_usuarioid_fkey;
ALTER TABLE IF EXISTS ONLY public.venta DROP CONSTRAINT IF EXISTS venta_sucursalid_fkey;
ALTER TABLE IF EXISTS ONLY public.venta DROP CONSTRAINT IF EXISTS venta_clienteid_fkey;
ALTER TABLE IF EXISTS ONLY public.variante_producto DROP CONSTRAINT IF EXISTS variante_producto_tallaid_fkey;
ALTER TABLE IF EXISTS ONLY public.variante_producto DROP CONSTRAINT IF EXISTS variante_producto_productoid_fkey;
ALTER TABLE IF EXISTS ONLY public.variante_producto DROP CONSTRAINT IF EXISTS variante_producto_colorid_fkey;
ALTER TABLE IF EXISTS ONLY public.usuario DROP CONSTRAINT IF EXISTS usuario_rolid_fkey;
ALTER TABLE IF EXISTS ONLY public.reserva DROP CONSTRAINT IF EXISTS reserva_sucursalid_fkey;
ALTER TABLE IF EXISTS ONLY public.reserva_detalle DROP CONSTRAINT IF EXISTS reserva_detalle_varianteid_fkey;
ALTER TABLE IF EXISTS ONLY public.reserva_detalle DROP CONSTRAINT IF EXISTS reserva_detalle_reservaid_fkey;
ALTER TABLE IF EXISTS ONLY public.reserva DROP CONSTRAINT IF EXISTS reserva_clienteid_fkey;
ALTER TABLE IF EXISTS ONLY public.producto_proveedor DROP CONSTRAINT IF EXISTS producto_proveedor_idproveedor_fkey;
ALTER TABLE IF EXISTS ONLY public.producto_proveedor DROP CONSTRAINT IF EXISTS producto_proveedor_idproducto_fkey;
ALTER TABLE IF EXISTS ONLY public.producto DROP CONSTRAINT IF EXISTS producto_categoriaid_fkey;
ALTER TABLE IF EXISTS ONLY public.pago DROP CONSTRAINT IF EXISTS pago_ventaid_fkey;
ALTER TABLE IF EXISTS ONLY public.pago DROP CONSTRAINT IF EXISTS pago_reciboid_fkey;
ALTER TABLE IF EXISTS ONLY public.pago DROP CONSTRAINT IF EXISTS pago_metodoid_fkey;
ALTER TABLE IF EXISTS ONLY public.notificacion DROP CONSTRAINT IF EXISTS notificacion_usuario_id_fkey;
ALTER TABLE IF EXISTS ONLY public.movimiento_inventario DROP CONSTRAINT IF EXISTS movimiento_inventario_usuarioid_fkey;
ALTER TABLE IF EXISTS ONLY public.movimiento_inventario DROP CONSTRAINT IF EXISTS movimiento_inventario_inventarioid_fkey;
ALTER TABLE IF EXISTS ONLY public.inventario DROP CONSTRAINT IF EXISTS inventario_varianteid_fkey;
ALTER TABLE IF EXISTS ONLY public.inventario DROP CONSTRAINT IF EXISTS inventario_sucursalid_fkey;
ALTER TABLE IF EXISTS ONLY public.inventario_sucursal DROP CONSTRAINT IF EXISTS inventario_sucursal_varianteid_fkey;
ALTER TABLE IF EXISTS ONLY public.inventario_sucursal DROP CONSTRAINT IF EXISTS inventario_sucursal_sucursalid_fkey;
ALTER TABLE IF EXISTS ONLY public.detalle_venta DROP CONSTRAINT IF EXISTS detalle_venta_ventaid_fkey;
ALTER TABLE IF EXISTS ONLY public.detalle_venta DROP CONSTRAINT IF EXISTS detalle_venta_varianteid_fkey;
ALTER TABLE IF EXISTS ONLY public.coleccion DROP CONSTRAINT IF EXISTS coleccion_temporadaid_fkey;
ALTER TABLE IF EXISTS ONLY public.cliente DROP CONSTRAINT IF EXISTS cliente_usuarioid_fkey;
ALTER TABLE IF EXISTS ONLY public.carrito DROP CONSTRAINT IF EXISTS carrito_sucursalid_fkey;
ALTER TABLE IF EXISTS ONLY public.carrito_item DROP CONSTRAINT IF EXISTS carrito_item_varianteid_fkey;
ALTER TABLE IF EXISTS ONLY public.carrito_item DROP CONSTRAINT IF EXISTS carrito_item_carritoid_fkey;
ALTER TABLE IF EXISTS ONLY public.carrito DROP CONSTRAINT IF EXISTS carrito_clienteid_fkey;
ALTER TABLE IF EXISTS ONLY public.bitacora DROP CONSTRAINT IF EXISTS bitacora_usuarioid_fkey;
DROP INDEX IF EXISTS public.ix_venta_id;
DROP INDEX IF EXISTS public.ix_variante_producto_id;
DROP INDEX IF EXISTS public.ix_temporada_id;
DROP INDEX IF EXISTS public.ix_talla_id;
DROP INDEX IF EXISTS public.ix_sucursal_id;
DROP INDEX IF EXISTS public.ix_reserva_sucursalid;
DROP INDEX IF EXISTS public.ix_reserva_id;
DROP INDEX IF EXISTS public.ix_reserva_codigoreserva;
DROP INDEX IF EXISTS public.ix_reserva_clienteid;
DROP INDEX IF EXISTS public.ix_recibo_id;
DROP INDEX IF EXISTS public.ix_proveedor_id;
DROP INDEX IF EXISTS public.ix_producto_id;
DROP INDEX IF EXISTS public.ix_pago_id;
DROP INDEX IF EXISTS public.ix_notificacion_usuario_id;
DROP INDEX IF EXISTS public.ix_notificacion_id;
DROP INDEX IF EXISTS public.ix_movimiento_inventario_id;
DROP INDEX IF EXISTS public.ix_metodo_pago_id;
DROP INDEX IF EXISTS public.ix_inventario_sucursal_varianteid;
DROP INDEX IF EXISTS public.ix_inventario_sucursal_sucursalid;
DROP INDEX IF EXISTS public.ix_inventario_sucursal_id;
DROP INDEX IF EXISTS public.ix_inventario_id;
DROP INDEX IF EXISTS public.ix_color_id;
DROP INDEX IF EXISTS public.ix_coleccion_id;
DROP INDEX IF EXISTS public.ix_cliente_id;
DROP INDEX IF EXISTS public.ix_categoria_id;
DROP INDEX IF EXISTS public.ix_carrito_sucursalid;
DROP INDEX IF EXISTS public.ix_carrito_id;
DROP INDEX IF EXISTS public.ix_carrito_clienteid;
DROP INDEX IF EXISTS public.ix_bitacora_usuarioid;
DROP INDEX IF EXISTS public.ix_bitacora_modulo_fechahora;
DROP INDEX IF EXISTS public.ix_bitacora_modulo;
DROP INDEX IF EXISTS public.ix_bitacora_id;
DROP INDEX IF EXISTS public.ix_bitacora_fechahora;
DROP INDEX IF EXISTS public.ix_bitacora_accion_fechahora;
DROP INDEX IF EXISTS public.ix_bitacora_accion;
ALTER TABLE IF EXISTS ONLY public.venta DROP CONSTRAINT IF EXISTS venta_pkey;
ALTER TABLE IF EXISTS ONLY public.venta DROP CONSTRAINT IF EXISTS venta_codigoventa_key;
ALTER TABLE IF EXISTS ONLY public.variante_producto DROP CONSTRAINT IF EXISTS variante_producto_pkey;
ALTER TABLE IF EXISTS ONLY public.usuario DROP CONSTRAINT IF EXISTS usuario_pkey;
ALTER TABLE IF EXISTS ONLY public.usuario DROP CONSTRAINT IF EXISTS usuario_email_key;
ALTER TABLE IF EXISTS ONLY public.temporada DROP CONSTRAINT IF EXISTS temporada_pkey;
ALTER TABLE IF EXISTS ONLY public.talla DROP CONSTRAINT IF EXISTS talla_pkey;
ALTER TABLE IF EXISTS ONLY public.sucursal DROP CONSTRAINT IF EXISTS sucursal_pkey;
ALTER TABLE IF EXISTS ONLY public.rol DROP CONSTRAINT IF EXISTS rol_pkey;
ALTER TABLE IF EXISTS ONLY public.rol DROP CONSTRAINT IF EXISTS rol_nombre_key;
ALTER TABLE IF EXISTS ONLY public.reserva DROP CONSTRAINT IF EXISTS reserva_pkey;
ALTER TABLE IF EXISTS ONLY public.reserva_detalle DROP CONSTRAINT IF EXISTS reserva_detalle_pkey;
ALTER TABLE IF EXISTS ONLY public.recibo DROP CONSTRAINT IF EXISTS recibo_pkey;
ALTER TABLE IF EXISTS ONLY public.proveedor DROP CONSTRAINT IF EXISTS proveedor_pkey;
ALTER TABLE IF EXISTS ONLY public.producto_proveedor DROP CONSTRAINT IF EXISTS producto_proveedor_pkey;
ALTER TABLE IF EXISTS ONLY public.producto DROP CONSTRAINT IF EXISTS producto_pkey;
ALTER TABLE IF EXISTS ONLY public.pago DROP CONSTRAINT IF EXISTS pago_pkey;
ALTER TABLE IF EXISTS ONLY public.notificacion DROP CONSTRAINT IF EXISTS notificacion_pkey;
ALTER TABLE IF EXISTS ONLY public.movimiento_inventario DROP CONSTRAINT IF EXISTS movimiento_inventario_pkey;
ALTER TABLE IF EXISTS ONLY public.metodo_pago DROP CONSTRAINT IF EXISTS metodo_pago_pkey;
ALTER TABLE IF EXISTS ONLY public.inventario_sucursal DROP CONSTRAINT IF EXISTS inventario_sucursal_pkey;
ALTER TABLE IF EXISTS ONLY public.inventario DROP CONSTRAINT IF EXISTS inventario_pkey;
ALTER TABLE IF EXISTS ONLY public.detalle_venta DROP CONSTRAINT IF EXISTS detalle_venta_pkey;
ALTER TABLE IF EXISTS ONLY public.color DROP CONSTRAINT IF EXISTS color_pkey;
ALTER TABLE IF EXISTS ONLY public.coleccion DROP CONSTRAINT IF EXISTS coleccion_pkey;
ALTER TABLE IF EXISTS ONLY public.cliente DROP CONSTRAINT IF EXISTS cliente_pkey;
ALTER TABLE IF EXISTS ONLY public.categoria DROP CONSTRAINT IF EXISTS categoria_pkey;
ALTER TABLE IF EXISTS ONLY public.carrito DROP CONSTRAINT IF EXISTS carrito_pkey;
ALTER TABLE IF EXISTS ONLY public.carrito_item DROP CONSTRAINT IF EXISTS carrito_item_pkey;
ALTER TABLE IF EXISTS ONLY public.bitacora DROP CONSTRAINT IF EXISTS bitacora_pkey;
ALTER TABLE IF EXISTS public.venta ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.variante_producto ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.usuario ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.temporada ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.talla ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sucursal ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.rol ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.reserva ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.recibo ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.proveedor ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.producto ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.pago ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.notificacion ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.movimiento_inventario ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.metodo_pago ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.inventario_sucursal ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.inventario ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.color ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.coleccion ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.cliente ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.categoria ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.carrito ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.bitacora ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.venta_id_seq;
DROP TABLE IF EXISTS public.venta;
DROP SEQUENCE IF EXISTS public.variante_producto_id_seq;
DROP TABLE IF EXISTS public.variante_producto;
DROP SEQUENCE IF EXISTS public.usuario_id_seq;
DROP TABLE IF EXISTS public.usuario;
DROP SEQUENCE IF EXISTS public.temporada_id_seq;
DROP TABLE IF EXISTS public.temporada;
DROP SEQUENCE IF EXISTS public.talla_id_seq;
DROP TABLE IF EXISTS public.talla;
DROP SEQUENCE IF EXISTS public.sucursal_id_seq;
DROP TABLE IF EXISTS public.sucursal;
DROP SEQUENCE IF EXISTS public.rol_id_seq;
DROP TABLE IF EXISTS public.rol;
DROP SEQUENCE IF EXISTS public.reserva_id_seq;
DROP TABLE IF EXISTS public.reserva_detalle;
DROP TABLE IF EXISTS public.reserva;
DROP SEQUENCE IF EXISTS public.recibo_id_seq;
DROP TABLE IF EXISTS public.recibo;
DROP SEQUENCE IF EXISTS public.proveedor_id_seq;
DROP TABLE IF EXISTS public.proveedor;
DROP TABLE IF EXISTS public.producto_proveedor;
DROP SEQUENCE IF EXISTS public.producto_id_seq;
DROP TABLE IF EXISTS public.producto;
DROP SEQUENCE IF EXISTS public.pago_id_seq;
DROP TABLE IF EXISTS public.pago;
DROP SEQUENCE IF EXISTS public.notificacion_id_seq;
DROP TABLE IF EXISTS public.notificacion;
DROP SEQUENCE IF EXISTS public.movimiento_inventario_id_seq;
DROP TABLE IF EXISTS public.movimiento_inventario;
DROP SEQUENCE IF EXISTS public.metodo_pago_id_seq;
DROP TABLE IF EXISTS public.metodo_pago;
DROP SEQUENCE IF EXISTS public.inventario_sucursal_id_seq;
DROP TABLE IF EXISTS public.inventario_sucursal;
DROP SEQUENCE IF EXISTS public.inventario_id_seq;
DROP TABLE IF EXISTS public.inventario;
DROP TABLE IF EXISTS public.detalle_venta;
DROP SEQUENCE IF EXISTS public.color_id_seq;
DROP TABLE IF EXISTS public.color;
DROP SEQUENCE IF EXISTS public.coleccion_id_seq;
DROP TABLE IF EXISTS public.coleccion;
DROP SEQUENCE IF EXISTS public.cliente_id_seq;
DROP TABLE IF EXISTS public.cliente;
DROP SEQUENCE IF EXISTS public.categoria_id_seq;
DROP TABLE IF EXISTS public.categoria;
DROP TABLE IF EXISTS public.carrito_item;
DROP SEQUENCE IF EXISTS public.carrito_id_seq;
DROP TABLE IF EXISTS public.carrito;
DROP SEQUENCE IF EXISTS public.bitacora_id_seq;
DROP TABLE IF EXISTS public.bitacora;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bitacora; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bitacora (
    id integer NOT NULL,
    usuarioid integer,
    accion character varying(50) NOT NULL,
    modulo character varying(50) NOT NULL,
    detalle text,
    ip character varying(45),
    fechahora timestamp without time zone NOT NULL,
    datosprevios text,
    datosnuevos text
);


--
-- Name: bitacora_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bitacora_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bitacora_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bitacora_id_seq OWNED BY public.bitacora.id;


--
-- Name: carrito; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.carrito (
    id integer NOT NULL,
    estado character varying(50) NOT NULL,
    fechacreacion timestamp without time zone NOT NULL,
    fechaactualizacion timestamp without time zone,
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
    fechaagregado timestamp without time zone
);


--
-- Name: categoria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categoria (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    activo boolean
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
    activo boolean,
    fecharegistro timestamp without time zone,
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
    activo boolean,
    temporadaid integer
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
    activo boolean
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
    descuento numeric(12,2),
    subtotal numeric(12,2) NOT NULL
);


--
-- Name: inventario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventario (
    id integer NOT NULL,
    stockfisico integer NOT NULL,
    stockreservado integer NOT NULL,
    stockminimo integer NOT NULL,
    fechaactualizacion timestamp without time zone,
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
-- Name: inventario_sucursal; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventario_sucursal (
    id integer NOT NULL,
    varianteid integer NOT NULL,
    sucursalid integer NOT NULL,
    cantidad integer NOT NULL,
    stockminimo integer,
    fechaactualizacion timestamp without time zone,
    stockreservado integer DEFAULT 0
);


--
-- Name: inventario_sucursal_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventario_sucursal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventario_sucursal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventario_sucursal_id_seq OWNED BY public.inventario_sucursal.id;


--
-- Name: metodo_pago; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.metodo_pago (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    estado boolean
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
    fecha timestamp without time zone,
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
-- Name: notificacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notificacion (
    id integer NOT NULL,
    usuario_id integer,
    titulo character varying(150) NOT NULL,
    mensaje text NOT NULL,
    tipo character varying(50),
    leido boolean,
    enlace character varying(255),
    fecha_creacion timestamp without time zone
);


--
-- Name: notificacion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notificacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notificacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notificacion_id_seq OWNED BY public.notificacion.id;


--
-- Name: pago; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pago (
    id integer NOT NULL,
    monto numeric(12,2) NOT NULL,
    estado character varying(50) NOT NULL,
    referencia character varying(150),
    fecha timestamp without time zone,
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
    preciobase numeric(10,2) NOT NULL,
    imagenprincipal text,
    activo boolean,
    fechacreacion timestamp without time zone,
    fechaactualizacion timestamp without time zone,
    categoriaid integer
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
    costocompra numeric(10,2),
    cantidad integer
);


--
-- Name: proveedor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.proveedor (
    id integer NOT NULL,
    nombre character varying(150) NOT NULL,
    razonsocial character varying(150),
    nit character varying(50),
    contacto character varying(100),
    telefono character varying(30),
    email character varying(150),
    direccion character varying(255),
    activo boolean,
    fechacreacion timestamp without time zone
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
-- Name: recibo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recibo (
    id integer NOT NULL,
    estado character varying(50) NOT NULL,
    fecha timestamp without time zone NOT NULL
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
    fechareserva timestamp without time zone NOT NULL,
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
    nombre character varying(50) NOT NULL,
    descripcion text,
    activo boolean DEFAULT true
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
    direccion character varying(255),
    telefono character varying(20),
    latitud numeric(10,8),
    longitud numeric(11,8),
    activo boolean,
    fechacreacion timestamp without time zone
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
    nombre character varying(20) NOT NULL,
    grupoedad character varying(50),
    orden integer,
    activo boolean
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
    activo boolean
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
    activo boolean DEFAULT true,
    fechacreacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    sucursalid integer,
    rolid integer,
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
    productoid integer NOT NULL,
    colorid integer,
    tallaid integer,
    sku character varying(50),
    codigobarra character varying(100),
    imagenurl text,
    precioventa numeric(10,2),
    activo boolean,
    fechacreacion timestamp without time zone
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
    descuento numeric(12,2),
    total numeric(12,2) NOT NULL,
    fecha timestamp without time zone,
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
-- Name: bitacora id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bitacora ALTER COLUMN id SET DEFAULT nextval('public.bitacora_id_seq'::regclass);


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
-- Name: inventario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario ALTER COLUMN id SET DEFAULT nextval('public.inventario_id_seq'::regclass);


--
-- Name: inventario_sucursal id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario_sucursal ALTER COLUMN id SET DEFAULT nextval('public.inventario_sucursal_id_seq'::regclass);


--
-- Name: metodo_pago id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metodo_pago ALTER COLUMN id SET DEFAULT nextval('public.metodo_pago_id_seq'::regclass);


--
-- Name: movimiento_inventario id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario ALTER COLUMN id SET DEFAULT nextval('public.movimiento_inventario_id_seq'::regclass);


--
-- Name: notificacion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notificacion ALTER COLUMN id SET DEFAULT nextval('public.notificacion_id_seq'::regclass);


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
-- Data for Name: bitacora; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (1, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Mateo Suárez Ortiz (mateo.suarez@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-15 07:52:00.960577', NULL, '{''id'': 9, ''nombre'': ''Mateo'', ''email'': ''mateo.suarez@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (2, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Admin Sistema (admin@tienda.com) - Rol ADMIN', '192.168.1.10', '2026-09-15 13:52:00.960577', NULL, '{''id'': 1, ''nombre'': ''Admin'', ''email'': ''admin@tienda.com'', ''rol'': ''ADMIN'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (3, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Andrea Peñaranda Soliz (ventas@ranglanstyle.com) - Rol CLIENTE', '192.168.1.10', '2026-09-15 19:52:00.960577', NULL, '{''id'': 20, ''nombre'': ''Andrea'', ''email'': ''ventas@ranglanstyle.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (4, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Cliente Prueba (cliente@tienda.com) - Rol CLIENTE', '192.168.1.10', '2026-09-16 01:52:00.960577', NULL, '{''id'': 3, ''nombre'': ''Cliente'', ''email'': ''cliente@tienda.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (5, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Valeria Morales Choque (valeria.m@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-16 04:52:00.960577', NULL, '{''id'': 10, ''nombre'': ''Valeria'', ''email'': ''valeria.m@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (6, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Estilista '' (ID: 11) - Precio: Bs 90.00', '192.168.1.10', '2026-09-16 04:52:00.960577', NULL, '{''id'': 11, ''nombre'': ''Polera Estilista '', ''precio'': 90.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (7, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Diogo Mars (diogomars2026@gmail.com) - Rol ADMIN', '192.168.1.10', '2026-09-16 10:52:00.960577', NULL, '{''id'': 2, ''nombre'': ''Diogo'', ''email'': ''diogomars2026@gmail.com'', ''rol'': ''ADMIN'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (8, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Mangas Negras'' (ID: 6) - Precio: Bs 150.00', '192.168.1.10', '2026-09-16 14:52:00.960577', NULL, '{''id'': 6, ''nombre'': ''Polera Mangas Negras'', ''precio'': 150.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (9, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Marcelo Torrico Chávez (pedidos@sublisport.bo) - Rol CLIENTE', '192.168.1.10', '2026-09-16 16:52:00.960577', NULL, '{''id'': 21, ''nombre'': ''Marcelo'', ''email'': ''pedidos@sublisport.bo'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (10, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Jorge Alanoca (jorgealanoca2005@gmail.com) - Rol ADMIN', '192.168.1.10', '2026-09-16 22:52:00.960577', NULL, '{''id'': 4, ''nombre'': ''Jorge'', ''email'': ''jorgealanoca2005@gmail.com'', ''rol'': ''ADMIN'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (11, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Canguro'' (ID: 1) - Precio: Bs 130.00', '192.168.1.10', '2026-09-17 00:52:00.960577', NULL, '{''id'': 1, ''nombre'': ''Canguro'', ''precio'': 130.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (12, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Filipina Estética Manicura'' (ID: 12) - Precio: Bs 90.00', '192.168.1.10', '2026-09-17 02:52:00.960577', NULL, '{''id'': 12, ''nombre'': ''Filipina Estética Manicura'', ''precio'': 90.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (13, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Carlos Banzer (ventas@mitsuba.bo) - Rol CLIENTE', '192.168.1.10', '2026-09-17 07:52:00.960577', NULL, '{''id'': 16, ''nombre'': ''Carlos'', ''email'': ''ventas@mitsuba.bo'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (14, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Rosa Floral Degradé / Polera Rosas Sublimada'' (ID: 7) - Precio: Bs 110.00', '192.168.1.10', '2026-09-17 12:52:00.960577', NULL, '{''id'': 7, ''nombre'': ''Polera Rosa Floral Degradé / Polera Rosas Sublimada'', ''precio'': 110.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (15, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Carlos Mendoza Flores (carlos.mendoza@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-17 19:52:00.960577', NULL, '{''id'': 5, ''nombre'': ''Carlos'', ''email'': ''carlos.mendoza@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (16, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Deportiva'' (ID: 2) - Precio: Bs 100.00', '192.168.1.10', '2026-09-17 22:52:00.960577', NULL, '{''id'': 2, ''nombre'': ''Polera Deportiva'', ''precio'': 100.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (17, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Diego Quispe Arnez (diego.quispe@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-18 01:52:00.960577', NULL, '{''id'': 11, ''nombre'': ''Diego'', ''email'': ''diego.quispe@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (18, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Fernando Justiniano (contacto@textilesoriente.bo) - Rol CLIENTE', '192.168.1.10', '2026-09-18 04:52:00.960577', NULL, '{''id'': 17, ''nombre'': ''Fernando'', ''email'': ''contacto@textilesoriente.bo'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (19, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: '' Polera Estampada '' (ID: 8) - Precio: Bs 150.00', '192.168.1.10', '2026-09-18 10:52:00.960577', NULL, '{''id'': 8, ''nombre'': '' Polera Estampada '', ''precio'': 150.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (20, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Mariana Rojas Gutiérrez (mariana.rojas@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-18 16:52:00.960577', NULL, '{''id'': 6, ''nombre'': ''Mariana'', ''email'': ''mariana.rojas@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (21, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Gradientes'' (ID: 3) - Precio: Bs 100.00', '192.168.1.10', '2026-09-18 20:52:00.960577', NULL, '{''id'': 3, ''nombre'': ''Polera Gradientes'', ''precio'': 100.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (48, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Polera Básica Roja Cuello Redondo (ID: 23)', NULL, '2026-09-22 02:11:58.922247', NULL, '{"id": 23, "nombre": "Polera Básica Roja Cuello Redondo", "precio": 120.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (22, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Camila Romero Aguilar (camila.romero@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-18 22:52:00.960577', NULL, '{''id'': 12, ''nombre'': ''Camila'', ''email'': ''camila.romero@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (23, 14, 'VENTA_POS', 'VENTAS', 'Emision de comprobante de venta POS #ORD-202609220453-994 por Bs 130.00 en Boutique Central Equipetrol', '192.168.1.25', '2026-09-18 23:52:00.960577', NULL, '{''codigoventa'': ''ORD-202609220453-994'', ''total'': 130.0, ''estado'': ''Completada'', ''sucursal'': ''Boutique Central Equipetrol''}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (24, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Negra Corazón Pincelada'' (ID: 13) - Precio: Bs 170.00', '192.168.1.10', '2026-09-19 00:52:00.960577', NULL, '{''id'': 13, ''nombre'': ''Polera Negra Corazón Pincelada'', ''precio'': 170.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (25, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera con diseño de mano '' (ID: 9) - Precio: Bs 115.00', '192.168.1.10', '2026-09-19 08:52:00.960577', NULL, '{''id'': 9, ''nombre'': ''Polera con diseño de mano '', ''precio'': 115.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (26, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Alejandro Vargas Torrico (alejandro.v@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-19 13:52:00.960577', NULL, '{''id'': 7, ''nombre'': ''Alejandro'', ''email'': ''alejandro.v@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (27, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Gradientes'' (ID: 4) - Precio: Bs 100.00', '192.168.1.10', '2026-09-19 18:52:00.960577', NULL, '{''id'': 4, ''nombre'': ''Polera Gradientes'', ''precio'': 100.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (28, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Sebastián Castro Miranda (seb.castro@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-19 19:52:00.960577', NULL, '{''id'': 13, ''nombre'': ''Sebastián'', ''email'': ''seb.castro@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (29, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Básica Bicolor Verde Olivo'' (ID: 14) - Precio: Bs 120.00', '192.168.1.10', '2026-09-19 22:52:00.960577', NULL, '{''id'': 14, ''nombre'': ''Polera Básica Bicolor Verde Olivo'', ''precio'': 120.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (30, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Mariela Vaca (info@pimabolivia.com) - Rol CLIENTE', '192.168.1.10', '2026-09-20 01:52:00.960577', NULL, '{''id'': 18, ''nombre'': ''Mariela'', ''email'': ''info@pimabolivia.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (31, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Negra Estampado Leopardo'' (ID: 10) - Precio: Bs 150.00', '192.168.1.10', '2026-09-20 06:52:00.960577', NULL, '{''id'': 10, ''nombre'': ''Polera Negra Estampado Leopardo'', ''precio'': 150.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (32, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Lucía Fernández Paz (lucia.fpaz@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-20 10:52:00.960577', NULL, '{''id'': 8, ''nombre'': ''Lucía'', ''email'': ''lucia.fpaz@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (33, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Natalia Pinto Soliz (natalia.pinto@example.com) - Rol CLIENTE', '192.168.1.10', '2026-09-20 16:52:00.960577', NULL, '{''id'': 14, ''nombre'': ''Natalia'', ''email'': ''natalia.pinto@example.com'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (34, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Dynamic Stroke V-Neck'' (ID: 5) - Precio: Bs 130.00', '192.168.1.10', '2026-09-20 16:52:00.960577', NULL, '{''id'': 5, ''nombre'': ''Dynamic Stroke V-Neck'', ''precio'': 130.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (35, 1, 'CREAR', 'PRODUCTOS', 'Alta en catalogo de polera: ''Polera Básica Verde Militar'' (ID: 15) - Precio: Bs 115.00', '192.168.1.10', '2026-09-20 20:52:00.960577', NULL, '{''id'': 15, ''nombre'': ''Polera Básica Verde Militar'', ''precio'': 115.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (36, 1, 'CREAR', 'USUARIOS', 'Registro formal de usuario del sistema: Rodrigo Camacho Vargas (contacto@gradientcolor.bo) - Rol CLIENTE', '192.168.1.10', '2026-09-20 22:52:00.960577', NULL, '{''id'': 19, ''nombre'': ''Rodrigo'', ''email'': ''contacto@gradientcolor.bo'', ''rol'': ''CLIENTE'', ''activo'': True}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (37, 1, 'LOGIN', 'AUTENTICACION', 'Inicio de sesion exitoso del administrador Admin en Shopyn Golden Store ERP', '192.168.1.10', '2026-09-22 01:37:00.960577', NULL, '{''rol'': ''ADMIN'', ''plataforma'': ''Web Backoffice ERP'', ''zona_horaria'': ''America/La_Paz (BOT, UTC-4)''}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (39, 1, 'LOGIN', 'AUTENTICACION', 'Inicio de sesión exitoso de Admin (admin@tienda.com)', NULL, '2026-09-22 01:57:23.288487', NULL, '{"rol": "ADMIN"}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (41, 1, 'LOGIN', 'AUTENTICACION', 'Inicio de sesión exitoso de Admin (admin@tienda.com)', NULL, '2026-09-22 01:58:42.34977', NULL, '{"rol": "ADMIN"}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (47, 1, 'LOGIN', 'AUTENTICACION', 'Inicio de sesión exitoso de Admin (admin@tienda.com)', NULL, '2026-09-22 02:10:49.045706', NULL, '{"rol": "ADMIN"}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (38, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Crop Top Negro (ID: 16)', NULL, '2026-09-22 01:56:34.35077', NULL, '{"id": 16, "nombre": "Crop Top Negro", "precio": 80.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (40, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Polera Negra Harley Quinn (ID: 17)', NULL, '2026-09-22 01:57:32.153239', NULL, '{"id": 17, "nombre": "Polera Negra Harley Quinn", "precio": 150.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (42, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Institucional Artesanal (ID: 18)', NULL, '2026-09-22 02:00:20.568094', NULL, '{"id": 18, "nombre": "Institucional Artesanal", "precio": 150.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (43, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Polera Rústica con Bordado Tradicional (ID: 19)', NULL, '2026-09-22 02:02:02.129476', NULL, '{"id": 19, "nombre": "Polera Rústica con Bordado Tradicional", "precio": 140.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (44, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Camisa Patujú Santa Cruz (ID: 20)', NULL, '2026-09-22 02:03:13.010086', NULL, '{"id": 20, "nombre": "Camisa Patujú Santa Cruz", "precio": 180.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (45, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Camisa Típica Blanca Bordado Ángel Chiquitano (ID: 21)', NULL, '2026-09-22 02:06:15.334258', NULL, '{"id": 21, "nombre": "Camisa Típica Blanca Bordado Ángel Chiquitano", "precio": 180.0}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (46, 1, 'CREAR', 'PRODUCTOS', 'Registro de nuevo producto: Polera Típica Beige Cordón Barroco (ID: 22)', NULL, '2026-09-22 02:07:21.187339', NULL, '{"id": 22, "nombre": "Polera Típica Beige Cordón Barroco", "precio": 199.5}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (49, 14, 'LOGIN', 'AUTENTICACION', 'Inicio de sesión exitoso de Natalia (natalia.pinto@example.com)', NULL, '2026-09-22 02:20:15.574812', NULL, '{"rol": "CLIENTE"}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (50, 1, 'VENTA_POS', 'VENTAS', 'Emisión de comprobante de venta presencial POS POS-202609220659-766 por Bs 80.00 (Sucursal: Boutique Las Brisas)', NULL, '2026-09-22 02:59:11.054946', NULL, '{"codigo_venta": "POS-202609220659-766", "total": 80.0, "items": 1, "sucursal_id": 3}');
INSERT INTO public.bitacora (id, usuarioid, accion, modulo, detalle, ip, fechahora, datosprevios, datosnuevos) VALUES (51, 1, 'VENTA_POS', 'VENTAS', 'Emisión de comprobante de venta presencial POS POS-202609220721-776 por Bs 199.50 (Sucursal: Boutique Las Brisas)', NULL, '2026-09-22 03:21:11.119331', NULL, '{"codigo_venta": "POS-202609220721-776", "total": 199.5, "items": 1, "sucursal_id": 3}');


--
-- Data for Name: carrito; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.carrito (id, estado, fechacreacion, fechaactualizacion, clienteid, sucursalid) VALUES (1, 'ACTIVO', '2026-09-12 02:56:27.226084', '2026-09-12 03:13:31.141425', 1, 1);
INSERT INTO public.carrito (id, estado, fechacreacion, fechaactualizacion, clienteid, sucursalid) VALUES (10, 'ACTIVO', '2026-09-22 02:33:09.266572', '2026-09-22 02:33:09.266577', 2, NULL);
INSERT INTO public.carrito (id, estado, fechacreacion, fechaactualizacion, clienteid, sucursalid) VALUES (11, 'ACTIVO', '2026-09-22 03:03:40.602421', '2026-09-22 03:03:40.602425', 14, NULL);


--
-- Data for Name: carrito_item; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (5, 'Poleras Polo', 'con cuello camisero y botones', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (6, 'Poleras Básicas de Cuello Redondo', 'lisas / unicolor', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (7, 'Poleras Deportivas', ' Cuello V /Sublimadas', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (8, ' Poleras Bicolor', 'Ranglan', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (9, ' Poleras con Efecto Degradado', 'Gradient', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (10, 'Polera con  Diseño ', 'Diseños mixto ', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (11, 'Poleras Subliminadas ', 'Comoda/ Malla Fria', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (12, 'Top Negro ', 'Bueno ', true);
INSERT INTO public.categoria (id, nombre, descripcion, activo) VALUES (13, 'Poleras artesanales', 'Tipicas', true);


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (14, 'Cliente', 'Prueba', 'cliente@tienda.com', '70000003', '1995-05-15', 'Masculino', true, '2026-09-22 03:02:52.854251', 3);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (15, 'Carlos', 'Mendoza Flores', 'carlos.mendoza@example.com', '71234567', '1992-03-10', 'Masculino', true, '2026-09-22 03:02:52.854251', 5);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (16, 'Mariana', 'Rojas Gutiérrez', 'mariana.rojas@example.com', '72345678', '1996-08-22', 'Femenino', true, '2026-09-22 03:02:52.854251', 6);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (17, 'Alejandro', 'Vargas Torrico', 'alejandro.v@example.com', '73456789', '1990-11-05', 'Masculino', true, '2026-09-22 03:02:52.854251', 7);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (18, 'Lucía', 'Fernández Paz', 'lucia.fpaz@example.com', '74567890', '1998-01-18', 'Femenino', true, '2026-09-22 03:02:52.854251', 8);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (19, 'Mateo', 'Suárez Ortiz', 'mateo.suarez@example.com', '75678901', '1994-07-30', 'Masculino', true, '2026-09-22 03:02:52.854251', 9);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (20, 'Valeria', 'Morales Choque', 'valeria.m@example.com', '76789012', '1997-12-14', 'Femenino', true, '2026-09-22 03:02:52.854251', 10);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (21, 'Diego', 'Quispe Arnez', 'diego.quispe@example.com', '77890123', '1993-04-25', 'Masculino', true, '2026-09-22 03:02:52.854251', 11);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (22, 'Camila', 'Romero Aguilar', 'camila.romero@example.com', '78901234', '1999-09-09', 'Femenino', true, '2026-09-22 03:02:52.854251', 12);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (23, 'Sebastián', 'Castro Miranda', 'seb.castro@example.com', '79012345', '1991-06-17', 'Masculino', true, '2026-09-22 03:02:52.854251', 13);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (24, 'Natalia', 'Pinto Soliz', 'natalia.pinto@example.com', '70123456', '1995-10-03', 'Femenino', true, '2026-09-22 03:02:52.854251', 14);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (1, 'Admin', 'Sistema', 'admin@tienda.com', '70000001', '1990-01-01', 'Masculino', true, '2026-09-13 19:46:19.936926', 1);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (3, 'Diogo', 'Mars', 'diogomars2026@gmail.com', '70000002', '1998-05-20', 'Masculino', true, '2026-09-19 14:30:53.920086', 2);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (25, 'Carlos', 'Banzer', 'ventas@mitsuba.bo', '33445566', NULL, NULL, true, '2026-09-22 03:02:58.893312', 16);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (26, 'Fernando', 'Justiniano', 'contacto@textilesoriente.bo', '33556677', NULL, NULL, true, '2026-09-22 03:02:58.895744', 17);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (27, 'Mariela', 'Vaca', 'info@pimabolivia.com', '33667788', NULL, NULL, true, '2026-09-22 03:02:58.89764', 18);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (28, 'Rodrigo', 'Camacho Vargas', 'contacto@gradientcolor.bo', '33778899', NULL, NULL, true, '2026-09-22 03:02:58.899336', 19);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (29, 'Andrea', 'Peñaranda Soliz', 'ventas@ranglanstyle.com', '33889900', NULL, NULL, true, '2026-09-22 03:02:58.901005', 20);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (30, 'Marcelo', 'Torrico Chávez', 'pedidos@sublisport.bo', '33990011', NULL, NULL, true, '2026-09-22 03:02:58.902543', 21);
INSERT INTO public.cliente (id, nombre, apellido, email, telefono, fechanac, genero, activo, fecharegistro, usuarioid) VALUES (31, 'Consumidor Final', '', 'consumidor_4668@boutique.com', '', NULL, NULL, true, '2026-09-22 06:59:10.894841', 1);


--
-- Data for Name: coleccion; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: color; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (1, 'Verde Oriente', '#007A3D', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (2, 'Blanco Tajibo', '#FFFFFF', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (3, 'Negro Azabache', '#111827', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (4, 'Azul Marino Camba', '#1E3A8A', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (5, 'Beige Chiquitano', '#D4B996', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (6, 'Terracota Guarayos', '#B45309', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (7, 'Gris Melange Urbano', '#64748B', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (8, 'Amarillo Patujú', '#F59E0B', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (9, 'Verde Olivo Chaco', '#556B2F', true);
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES (10, 'Rojo Borgoña', '#991B1B', true);


--
-- Data for Name: detalle_venta; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.detalle_venta (ventaid, varianteid, cantidad, preciounitario, descuento, subtotal) VALUES (1, 1, 1, 130.00, 0.00, 130.00);
INSERT INTO public.detalle_venta (ventaid, varianteid, cantidad, preciounitario, descuento, subtotal) VALUES (2, 20, 1, 80.00, 0.00, 80.00);
INSERT INTO public.detalle_venta (ventaid, varianteid, cantidad, preciounitario, descuento, subtotal) VALUES (3, 17, 1, 199.50, 0.00, 199.50);


--
-- Data for Name: inventario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (2, 20, 0, 5, '2026-09-22 02:54:05.637027', 2, 1);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (3, 20, 0, 5, '2026-09-22 02:54:05.639256', 3, 1);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (4, 20, 0, 5, '2026-09-22 03:01:50.719846', 1, 2);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (5, 20, 0, 5, '2026-09-22 03:01:50.722189', 2, 2);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (6, 20, 0, 5, '2026-09-22 03:01:50.724379', 3, 2);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (7, 20, 0, 5, '2026-09-22 03:12:03.750415', 1, 3);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (8, 20, 0, 5, '2026-09-22 03:12:03.753097', 2, 3);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (9, 20, 0, 5, '2026-09-22 03:12:03.755151', 3, 3);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (10, 20, 0, 5, '2026-09-22 03:14:35.518332', 1, 4);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (11, 20, 0, 5, '2026-09-22 03:14:35.522916', 2, 4);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (12, 20, 0, 5, '2026-09-22 03:14:35.529091', 3, 4);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (1, 19, 0, 5, '2026-09-22 04:53:56.805657', 1, 1);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (13, 20, 0, 5, '2026-09-22 05:24:29.807647', 1, 5);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (14, 20, 0, 5, '2026-09-22 05:24:29.810398', 2, 5);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (15, 20, 0, 5, '2026-09-22 05:24:29.812018', 3, 5);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (16, 20, 0, 5, '2026-09-22 05:24:29.816865', 1, 6);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (17, 20, 0, 5, '2026-09-22 05:24:29.81883', 2, 6);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (18, 20, 0, 5, '2026-09-22 05:24:29.820427', 3, 6);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (19, 20, 0, 5, '2026-09-22 05:24:29.824148', 1, 7);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (20, 20, 0, 5, '2026-09-22 05:24:29.825805', 2, 7);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (21, 20, 0, 5, '2026-09-22 05:24:29.827586', 3, 7);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (22, 20, 0, 5, '2026-09-22 05:24:29.831748', 1, 8);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (23, 20, 0, 5, '2026-09-22 05:24:29.833189', 2, 8);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (24, 20, 0, 5, '2026-09-22 05:24:29.834753', 3, 8);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (25, 20, 0, 5, '2026-09-22 05:24:29.837549', 1, 9);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (26, 20, 0, 5, '2026-09-22 05:24:29.838844', 2, 9);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (27, 20, 0, 5, '2026-09-22 05:24:29.840424', 3, 9);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (28, 20, 0, 5, '2026-09-22 05:24:29.844352', 1, 10);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (29, 20, 0, 5, '2026-09-22 05:24:29.845711', 2, 10);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (30, 20, 0, 5, '2026-09-22 05:24:29.847458', 3, 10);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (31, 20, 0, 5, '2026-09-22 05:24:29.85104', 1, 11);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (32, 20, 0, 5, '2026-09-22 05:24:29.852367', 2, 11);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (33, 20, 0, 5, '2026-09-22 05:24:29.853603', 3, 11);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (34, 20, 0, 5, '2026-09-22 05:24:29.856638', 1, 12);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (35, 20, 0, 5, '2026-09-22 05:24:29.858569', 2, 12);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (36, 20, 0, 5, '2026-09-22 05:24:29.860584', 3, 12);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (37, 20, 0, 5, '2026-09-22 05:24:29.865067', 1, 13);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (38, 20, 0, 5, '2026-09-22 05:24:29.868414', 2, 13);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (39, 20, 0, 5, '2026-09-22 05:24:29.870715', 3, 13);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (40, 20, 0, 5, '2026-09-22 06:07:45.65228', 1, 14);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (41, 20, 0, 5, '2026-09-22 06:07:45.655819', 2, 14);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (42, 20, 0, 5, '2026-09-22 06:07:45.659261', 3, 14);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (43, 20, 0, 5, '2026-09-22 06:07:45.663571', 1, 15);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (44, 20, 0, 5, '2026-09-22 06:07:45.665279', 2, 15);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (45, 20, 0, 5, '2026-09-22 06:07:45.667039', 3, 15);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (46, 20, 0, 5, '2026-09-22 06:07:45.670693', 1, 16);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (47, 20, 0, 5, '2026-09-22 06:07:45.67287', 2, 16);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (48, 20, 0, 5, '2026-09-22 06:07:45.674754', 3, 16);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (49, 20, 0, 5, '2026-09-22 06:07:45.678667', 1, 17);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (50, 20, 0, 5, '2026-09-22 06:07:45.680362', 2, 17);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (52, 20, 0, 5, '2026-09-22 06:07:45.72536', 1, 18);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (53, 20, 0, 5, '2026-09-22 06:07:45.72682', 2, 18);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (54, 20, 0, 5, '2026-09-22 06:07:45.728328', 3, 18);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (55, 20, 0, 5, '2026-09-22 06:07:45.732775', 1, 19);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (56, 20, 0, 5, '2026-09-22 06:07:45.734291', 2, 19);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (57, 20, 0, 5, '2026-09-22 06:07:45.735615', 3, 19);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (58, 20, 0, 5, '2026-09-22 06:07:45.7384', 1, 20);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (59, 20, 0, 5, '2026-09-22 06:07:45.739818', 2, 20);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (61, 20, 0, 5, '2026-09-22 06:07:45.743721', 1, 21);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (62, 20, 0, 5, '2026-09-22 06:07:45.744765', 2, 21);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (63, 20, 0, 5, '2026-09-22 06:07:45.745764', 3, 21);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (64, 20, 0, 5, '2026-09-22 06:07:45.748476', 1, 22);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (65, 20, 0, 5, '2026-09-22 06:07:45.749882', 2, 22);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (66, 20, 0, 5, '2026-09-22 06:07:45.751344', 3, 22);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (67, 20, 0, 5, '2026-09-22 06:18:50.491706', 1, 23);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (68, 20, 0, 5, '2026-09-22 06:18:50.495883', 2, 23);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (69, 20, 0, 5, '2026-09-22 06:18:50.49941', 3, 23);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (60, 19, 0, 5, '2026-09-22 06:59:10.945893', 3, 20);
INSERT INTO public.inventario (id, stockfisico, stockreservado, stockminimo, fechaactualizacion, sucursalid, varianteid) VALUES (51, 19, 0, 5, '2026-09-22 07:21:11.084904', 3, 17);


--
-- Data for Name: inventario_sucursal; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: metodo_pago; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.metodo_pago (id, nombre, estado) VALUES (1, 'Efectivo', true);
INSERT INTO public.metodo_pago (id, nombre, estado) VALUES (2, 'Tarjeta de Débito / Crédito', true);
INSERT INTO public.metodo_pago (id, nombre, estado) VALUES (3, 'QR / Transferencia Bancaria', true);
INSERT INTO public.metodo_pago (id, nombre, estado) VALUES (4, 'Pago Digital / Online', false);
INSERT INTO public.metodo_pago (id, nombre, estado) VALUES (5, 'PayPal', true);


--
-- Data for Name: movimiento_inventario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.movimiento_inventario (id, tipomovimiento, cantidad, motivo, referencia, fecha, inventarioid, usuarioid) VALUES (1, 'Venta Digital', -1, 'Descuento automático por Venta Digital (ORD-202609220453-994)', 'ORD-202609220453-994', '2026-09-22 04:53:56.8057', 1, 14);
INSERT INTO public.movimiento_inventario (id, tipomovimiento, cantidad, motivo, referencia, fecha, inventarioid, usuarioid) VALUES (2, 'Venta Presencial', -1, 'Descuento automático por Venta Presencial (POS-202609220659-766)', 'POS-202609220659-766', '2026-09-22 06:59:10.945963', 60, 1);
INSERT INTO public.movimiento_inventario (id, tipomovimiento, cantidad, motivo, referencia, fecha, inventarioid, usuarioid) VALUES (3, 'Venta Presencial', -1, 'Descuento automático por Venta Presencial (POS-202609220721-776)', 'POS-202609220721-776', '2026-09-22 07:21:11.084918', 51, 1);


--
-- Data for Name: notificacion; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.pago (id, monto, estado, referencia, fecha, ventaid, reciboid, metodoid) VALUES (1, 130.00, 'Aprobado', 'PAY-ORD-202609220453-994', '2026-09-22 04:53:56.777065', 1, NULL, 4);


--
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (19, 'Polera Rústica con Bordado Tradicional', '', 'Boutique Collection', 'Unisex', 'Juvenil', 140.00, 'https://i.postimg.cc/bNrrzDw1/333.png', true, '2026-09-22 06:02:02.113355', '2026-09-22 06:02:02.113378', 13);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (20, 'Camisa Patujú Santa Cruz', '', 'Boutique Collection', 'Caballeros', 'Adultos', 180.00, 'https://i.postimg.cc/VLvvYrk0/344.png', true, '2026-09-22 06:03:12.999447', '2026-09-22 06:03:12.999454', 13);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (21, 'Camisa Típica Blanca Bordado Ángel Chiquitano', '', 'Artesanos Magdalena', 'Unisex', 'Juvenil', 180.00, 'https://i.postimg.cc/T17PVGCL/355.png', true, '2026-09-22 06:06:15.3216', '2026-09-22 06:06:15.321612', 13);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (22, 'Polera Típica Beige Cordón Barroco', '', 'Boutique Collection', 'Unisex', 'Juvenil', 199.50, 'https://i.postimg.cc/QxCCX9dJ/366.png', true, '2026-09-22 06:07:21.182435', '2026-09-22 06:07:21.182438', 13);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (23, 'Polera Básica Roja Cuello Redondo', '', 'Boutique Collection', 'Caballeros', 'Adultos', 120.00, 'https://i.postimg.cc/zvwjvHfH/ai-generated-t-shirt-mockup-clip-art-free-png.png', true, '2026-09-22 06:11:58.916189', '2026-09-22 06:11:58.916197', 6);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (1, 'Canguro', '100%', 'Boutique Collection', 'Unisex', 'Juvenil', 130.00, 'https://i.postimg.cc/vmvSqjyp/image-(1).png', true, '2026-09-22 02:52:15.727148', '2026-09-22 02:52:15.727157', 5);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (2, 'Polera Deportiva', '', 'Boutique Collection', 'Unisex', 'Adultos', 100.00, 'https://i.postimg.cc/wMY29Q9h/a-blue-gradient-short-sleeved-t-shirt-on-a-transparent-background-setting-png.png', true, '2026-09-22 03:01:47.535215', '2026-09-22 03:01:47.535219', 7);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (3, 'Polera Gradientes', '', 'Boutique Collection', 'Unisex', 'Adultos', 100.00, 'https://i.postimg.cc/rsGJsRpN/blank-t-shirt-mockup-with-orange-gradient-isolated-on-transparent-background-free-png.png', true, '2026-09-22 03:03:22.185059', '2026-09-22 03:03:22.18507', 8);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (4, 'Polera Gradientes', 'Cuello V', 'Boutique Collection', 'Caballeros', 'Adultos', 100.00, 'https://i.postimg.cc/cC7mCtJr/a-green-polo-shirt-with-black-and-white-designs-free-png.png', true, '2026-09-22 03:14:28.016799', '2026-09-22 03:14:28.016847', 8);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (5, 'Dynamic Stroke V-Neck', 'Malla Fria', 'Boutique Collection', 'Unisex', 'Juvenil', 130.00, 'https://i.postimg.cc/C5CN5nK9/unique-abstract-jersey-design-mockup-isolated-on-transparent-background-perfect-for-gaming-teams-spo.png', true, '2026-09-22 03:17:07.067668', '2026-09-22 03:17:07.067675', 7);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (6, 'Polera Mangas Negras', '', 'Boutique Collection', 'Caballeros', 'Juvenil', 150.00, 'https://i.postimg.cc/PJb4JvqB/white-t-shirt-mockup-free-png.png', true, '2026-09-22 03:36:46.264392', '2026-09-22 03:36:46.264399', 6);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (7, 'Polera Rosa Floral Degradé / Polera Rosas Sublimada', 'Tela Malla Fria', 'Boutique Collection', 'Damas', 'Adultos', 110.00, 'https://i.postimg.cc/k5DSV1sK/20.png', true, '2026-09-22 05:05:12.354085', '2026-09-22 05:05:12.354099', 9);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (8, ' Polera Estampada ', '', 'Boutique Collection', 'Damas', 'Adultos', 150.00, 'https://i.postimg.cc/s28h5YHJ/21.png', true, '2026-09-22 05:06:49.132199', '2026-09-22 05:06:49.132207', 6);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (9, 'Polera con diseño de mano ', 'Diseño basico', 'Boutique Collection', 'Damas', 'Adultos', 115.00, 'https://i.postimg.cc/yN5Z0mpg/23.png', true, '2026-09-22 05:13:57.261553', '2026-09-22 05:13:57.261558', 10);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (10, 'Polera Negra Estampado Leopardo', '', 'Boutique Collection', 'Caballeros', 'Adultos', 150.00, 'https://i.postimg.cc/pd7FKfcQ/24.png', true, '2026-09-22 05:15:07.68983', '2026-09-22 05:15:07.689834', 10);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (11, 'Polera Estilista ', '', 'Boutique Collection', 'Damas', 'Adultos', 90.00, 'https://i.postimg.cc/5tjzH7gd/26.png', true, '2026-09-22 05:19:51.55042', '2026-09-22 05:19:51.550423', 11);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (12, 'Filipina Estética Manicura', 'Lana ', 'Boutique Collection', 'Damas', 'Adultos', 90.00, 'https://i.postimg.cc/CKd8ZP7w/28.png', true, '2026-09-22 05:21:21.666998', '2026-09-22 05:21:21.667004', 11);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (13, 'Polera Negra Corazón Pincelada', 'Cencilla y elegante
', 'Boutique Collection', 'Damas', 'Juvenil', 170.00, 'https://i.postimg.cc/HLjMJZzG/29.png', true, '2026-09-22 05:22:38.082773', '2026-09-22 05:22:38.082779', 10);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (14, 'Polera Básica Bicolor Verde Olivo', '', 'Boutique Collection', 'Caballeros', 'Juvenil', 120.00, 'https://i.postimg.cc/br0TrSv0/green-crew-neck-t-shirt-with-short-sleeves-against-a-transparent-background-png.webp', true, '2026-09-22 05:28:28.632536', '2026-09-22 05:28:28.63254', 8);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (15, 'Polera Básica Verde Militar', '', 'Boutique Collection', 'Caballeros', 'Adultos', 115.00, 'https://i.postimg.cc/PJb4JvqL/a-men-s-t-shirt-in-olive-green-highlighting-its-simple-style-and-comfortable-fit-perfect-for-everyda.webp', true, '2026-09-22 05:29:35.017141', '2026-09-22 05:29:35.017146', 6);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (16, 'Crop Top Negro', '', 'Boutique Collection', 'Damas', 'Juvenil', 80.00, 'https://i.postimg.cc/nL4cdq0W/300.png', true, '2026-09-22 05:56:34.343896', '2026-09-22 05:56:34.343902', 12);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (17, 'Polera Negra Harley Quinn', '', 'Boutique Collection', 'Damas', 'Juvenil', 150.00, 'https://i.postimg.cc/vBX8ybR5/311.png', true, '2026-09-22 05:57:32.137982', '2026-09-22 05:57:32.137988', 10);
INSERT INTO public.producto (id, nombre, descripcion, marca, genero, grupoedad, preciobase, imagenprincipal, activo, fechacreacion, fechaactualizacion, categoriaid) VALUES (18, 'Institucional Artesanal', '', 'Boutique Collection', 'Unisex', 'Juvenil', 150.00, 'https://i.postimg.cc/0Q95hr4D/322.png', true, '2026-09-22 06:00:20.533875', '2026-09-22 06:00:20.533885', 13);


--
-- Data for Name: producto_proveedor; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: proveedor; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (1, 'Industrias Textiles Mitsuba S.A.', 'Mitsuba Bolivia Textiles S.A.', '1028374029', 'Lic. Carlos Banzer', '+591 3 3467711', 'ventas@mitsuba.bo', 'Parque Industrial Manzana 14, Santa Cruz', true, '2026-09-13 19:41:24.491893');
INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (2, 'Confecciones Textiles del Oriente S.R.L.', 'Textiles del Oriente Cruceño S.R.L.', '1049281033', 'Ing. Fernando Justiniano', '+591 3 3529944', 'contacto@textilesoriente.bo', 'Av. Virgen de Cotoca Km 4.5, Santa Cruz', true, '2026-09-13 19:41:24.491898');
INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (3, 'Algodonera Pima Bolivia & Co.', 'Algodones Finos Pima S.R.L.', '1083749012', 'Mariela Vaca', '+591 3 3362288', 'info@pimabolivia.com', 'Calle Warnes #240, Santa Cruz de la Sierra', true, '2026-09-13 19:41:24.4919');
INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (4, 'Gradient Color Bolivia', 'Tintes y Acabados Gradient Color S.R.L.', '1029384021', 'Rodrigo Camacho Vargas', '+591 71029384', 'contacto@gradientcolor.bo', 'Parque Industrial Mz. 14, Santa Cruz', true, '2026-09-22 01:02:36.624854');
INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (5, 'Ranglan Style', 'Industrias Textiles Bicolor & Ranglan S.A.', '3049582019', 'Andrea Peñaranda Soliz', '+591 72134590', 'ventas@ranglanstyle.com', 'Av. Blanco Galindo Km 6, Cochabamba', true, '2026-09-22 01:08:27.500018');
INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (6, 'SubliSport', 'Sublimaciones e Insumos Deportivos SubliSport S.R.L.', '4920183025', 'Marcelo Torrico Chávez', '+591 73245601', 'pedidos@sublisport.bo', 'Av. Banzer entre 4to y 5to Anillo, Santa Cruz', true, '2026-09-22 01:09:13.724305');
INSERT INTO public.proveedor (id, nombre, razonsocial, nit, contacto, telefono, email, direccion, activo, fechacreacion) VALUES (7, 'SubliSport', 'Sublimaciones e Insumos Deportivos SubliSport S.R.L.', '4920183025', 'Marcelo Torrico Chávez', '+591 73245601', 'pedidos@sublisport.bo', 'Av. Banzer entre 4to y 5to Anillo, Santa Cruz', true, '2026-09-22 02:07:59.190717');


--
-- Data for Name: recibo; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: reserva; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: reserva_detalle; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rol (id, nombre, descripcion, activo) VALUES (1, 'ADMIN', 'Administrador total del sistema', true);
INSERT INTO public.rol (id, nombre, descripcion, activo) VALUES (2, 'CLIENTE', 'Cliente comprador de la tienda', true);
INSERT INTO public.rol (id, nombre, descripcion, activo) VALUES (3, 'CAJERO ', 'Responsable de caja', true);
INSERT INTO public.rol (id, nombre, descripcion, activo) VALUES (4, 'Supervisor', 'Supervisa todo el sistema ', true);


--
-- Data for Name: sucursal; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.sucursal (id, nombre, ciudad, direccion, telefono, latitud, longitud, activo, fechacreacion) VALUES (1, 'Boutique Central Equipetrol', 'Santa Cruz de la Sierra', 'Av. San Martín esq. Calle 7 (Equipetrol)', '+591 3 3421100', NULL, NULL, true, '2026-09-12 02:34:35.191833');
INSERT INTO public.sucursal (id, nombre, ciudad, direccion, telefono, latitud, longitud, activo, fechacreacion) VALUES (2, 'Boutique Mall Ventura', 'Santa Cruz de la Sierra', '4to Anillo y Av. San Martín, Nivel 1 Local 42', '+591 3 3458890', NULL, NULL, true, '2026-09-12 02:34:35.205013');
INSERT INTO public.sucursal (id, nombre, ciudad, direccion, telefono, latitud, longitud, activo, fechacreacion) VALUES (3, 'Boutique Las Brisas', 'Santa Cruz de la Sierra', 'Av. Cristo Redentor y 4to Anillo, PB Local 15', '+591 3 3482210', NULL, NULL, true, '2026-09-12 02:34:35.20635');


--
-- Data for Name: talla; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.talla (id, nombre, grupoedad, orden, activo) VALUES (1, 'S', 'Adultos', 1, true);
INSERT INTO public.talla (id, nombre, grupoedad, orden, activo) VALUES (2, 'M', 'Adultos', 2, true);
INSERT INTO public.talla (id, nombre, grupoedad, orden, activo) VALUES (3, 'L', 'Adultos', 3, true);
INSERT INTO public.talla (id, nombre, grupoedad, orden, activo) VALUES (4, 'XL', 'Adultos', 4, true);
INSERT INTO public.talla (id, nombre, grupoedad, orden, activo) VALUES (5, 'XXL', 'Adultos', 5, true);


--
-- Data for Name: temporada; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.temporada (id, nombre, descripcion, fechainicio, fechafin, activo) VALUES (1, 'Primavera - Verano Santa Cruz 2026', NULL, '2026-09-01', '2027-03-31', true);
INSERT INTO public.temporada (id, nombre, descripcion, fechainicio, fechafin, activo) VALUES (2, 'Temporada Fexpocruz / Feria 2026', NULL, '2026-09-15', '2026-10-15', true);


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (3, 'Cliente', 'Prueba', 'cliente@tienda.com', '$2b$12$GTGjeU5f4GRITsID/QC1Z.J.a/qgT02YsOokZ/yFS5QO2lCcsO5XK', '70000003', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (4, 'Jorge', 'Alanoca', 'jorgealanoca2005@gmail.com', '$2b$12$uIZb5B.QiE9ielpkVFMWSuQowxoMF6zKTr/asB86.Y5nF9o6vYYqG', '67838705', true, '2026-09-22 03:02:52.854251', NULL, 1, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (5, 'Carlos', 'Mendoza Flores', 'carlos.mendoza@example.com', '$2b$12$stcmm1f43q7NhBCBisHMeetaQeiNouTtRgZLrDE.BWOkqy112bBaK', '71234567', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (6, 'Mariana', 'Rojas Gutiérrez', 'mariana.rojas@example.com', '$2b$12$MZyR/9kLJQSsF6PEqiuUEeitSEXkm4E7W4GKLPus0wTLO6gV/rvci', '72345678', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (7, 'Alejandro', 'Vargas Torrico', 'alejandro.v@example.com', '$2b$12$O5I94I9FuZhTEIHIq5.N0e0lLeSdxFLggpw48LIkH6zaffspJPQLS', '73456789', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (8, 'Lucía', 'Fernández Paz', 'lucia.fpaz@example.com', '$2b$12$B.SfHPevVEzrj10F2DGCBOV5SK83Z.uR7ZxLLtz8V4DmaUgwwZCG2', '74567890', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (9, 'Mateo', 'Suárez Ortiz', 'mateo.suarez@example.com', '$2b$12$yYQdCZRdaCjK9u/9lWzqxuNSJLVajDFhSevoIJWtSJTkdhgVglDJW', '75678901', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (10, 'Valeria', 'Morales Choque', 'valeria.m@example.com', '$2b$12$7gkUYPFzK5OsECch9/AC6.hEZlCESFua1Nhd2cgYL4/U.x1bse68a', '76789012', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (11, 'Diego', 'Quispe Arnez', 'diego.quispe@example.com', '$2b$12$bc3xudkwkfx0CnrpZ7MlUunRTRtFgyFcTeOH9fyctc0ajAEZQCbe6', '77890123', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (12, 'Camila', 'Romero Aguilar', 'camila.romero@example.com', '$2b$12$KKo.vo6kQIcV4FtkiylO2O.7VFqAQXIuku7jdtIz3HAaOue7UeX9u', '78901234', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (13, 'Sebastián', 'Castro Miranda', 'seb.castro@example.com', '$2b$12$jDmbPrYLZDeo.0N32chZ3.v81zulcV8eq0BnoLCPP6b6Me7UP5Kxq', '79012345', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (14, 'Natalia', 'Pinto Soliz', 'natalia.pinto@example.com', '$2b$12$eWcjNcKC/RbLV/AMVN4CTuwsNcBNBQRCKxnMLgbghcfEi1mEgoHaK', '70123456', true, '2026-09-22 03:02:52.854251', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (1, 'Admin', 'Sistema', 'admin@tienda.com', '$2b$12$uLlXd1QDOKe8ZYVWuKv5VeUpEZ5EHTD/MOiFG4dKtLDZM/W4zo9K2', '70000001', true, '2026-09-11 15:38:06.344764', NULL, 1, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (16, 'Carlos', 'Banzer', 'ventas@mitsuba.bo', '$2b$12$jUQRf3yRs/oHZZIR0mNF1uj0SJDUmf6AQHmfAE7oWm6pkZGKf2p9W', '33445566', true, '2026-09-22 03:02:58.889035', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (17, 'Fernando', 'Justiniano', 'contacto@textilesoriente.bo', '$2b$12$YF7/mf4rt7/YF932.4OMd.KSCcZnVgI/slVq5bYDgF3i1ckJ5E/CK', '33556677', true, '2026-09-22 03:02:58.889039', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (18, 'Mariela', 'Vaca', 'info@pimabolivia.com', '$2b$12$LZt03SkMKbDThg90rqZDZON.V5UXquAFNWk.BGySQcH7aIQ2ZfNAy', '33667788', true, '2026-09-22 03:02:58.889041', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (19, 'Rodrigo', 'Camacho Vargas', 'contacto@gradientcolor.bo', '$2b$12$hfiIUUqXsYTSTaRJHCeAFuwSVdDqNUjk/7skjAtqYGKVWSnK5wKEy', '33778899', true, '2026-09-22 03:02:58.889042', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (20, 'Andrea', 'Peñaranda Soliz', 'ventas@ranglanstyle.com', '$2b$12$9ylqUJqNJ/X6okw8sLEptOP2xtKpxrFxxtYSnFjQxvPri2G0.LmYO', '33889900', true, '2026-09-22 03:02:58.889043', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (21, 'Marcelo', 'Torrico Chávez', 'pedidos@sublisport.bo', '$2b$12$U0ptbQB9lfCZypvs3RS8ZOk9yRrEXjuWFe2PM9qWczQTmGoAfvQv.', '33990011', true, '2026-09-22 03:02:58.889044', NULL, 2, true, NULL, NULL);
INSERT INTO public.usuario (id, nombre, apellido, email, passwordhash, telefono, activo, fechacreacion, sucursalid, rolid, verificado, codigoverificacion, codigoexpiracion) VALUES (2, 'Diogo', 'Rocha Jaimez', 'diogomars2026@gmail.com', '$2b$12$2E72eAqvrZNemRCoeE8N3OtxHiu26/ovbocuoi5JrtQq8z8w7zKY6', '74611114', true, '2026-09-11 15:38:06.344768', NULL, 1, true, NULL, NULL);


--
-- Data for Name: variante_producto; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (1, 1, 1, 1, 'POL-1-1-1', NULL, NULL, 130.00, true, '2026-09-22 02:54:05.624797');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (2, 2, 1, 1, 'POL-2-1-1', NULL, NULL, 100.00, true, '2026-09-22 03:01:50.716882');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (3, 3, 1, 1, 'POL-3-1-1', NULL, NULL, 100.00, true, '2026-09-22 03:12:03.747896');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (4, 4, 1, 1, 'POL-4-1-1', NULL, NULL, 100.00, true, '2026-09-22 03:14:35.512532');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (5, 5, 1, 1, 'POL-5-1-1', NULL, NULL, 130.00, true, '2026-09-22 05:24:29.79455');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (6, 6, 1, 1, 'POL-6-1-1', NULL, NULL, 150.00, true, '2026-09-22 05:24:29.814384');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (7, 7, 1, 1, 'POL-7-1-1', NULL, NULL, 110.00, true, '2026-09-22 05:24:29.822258');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (8, 8, 1, 1, 'POL-8-1-1', NULL, NULL, 150.00, true, '2026-09-22 05:24:29.829399');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (9, 9, 1, 1, 'POL-9-1-1', NULL, NULL, 115.00, true, '2026-09-22 05:24:29.836195');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (10, 10, 1, 1, 'POL-10-1-1', NULL, NULL, 150.00, true, '2026-09-22 05:24:29.842401');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (11, 11, 1, 1, 'POL-11-1-1', NULL, NULL, 90.00, true, '2026-09-22 05:24:29.849296');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (12, 12, 1, 1, 'POL-12-1-1', NULL, NULL, 90.00, true, '2026-09-22 05:24:29.85504');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (13, 13, 1, 1, 'POL-13-1-1', NULL, NULL, 170.00, true, '2026-09-22 05:24:29.86273');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (14, 19, 1, 1, 'POL-19-1-1', NULL, NULL, 140.00, true, '2026-09-22 06:07:45.648004');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (15, 20, 1, 1, 'POL-20-1-1', NULL, NULL, 180.00, true, '2026-09-22 06:07:45.661585');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (16, 21, 1, 1, 'POL-21-1-1', NULL, NULL, 180.00, true, '2026-09-22 06:07:45.668887');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (17, 22, 1, 1, 'POL-22-1-1', NULL, NULL, 199.50, true, '2026-09-22 06:07:45.676671');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (18, 14, 1, 1, 'POL-14-1-1', NULL, NULL, 120.00, true, '2026-09-22 06:07:45.723643');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (19, 15, 1, 1, 'POL-15-1-1', NULL, NULL, 115.00, true, '2026-09-22 06:07:45.729835');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (20, 16, 1, 1, 'POL-16-1-1', NULL, NULL, 80.00, true, '2026-09-22 06:07:45.73701');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (21, 17, 1, 1, 'POL-17-1-1', NULL, NULL, 150.00, true, '2026-09-22 06:07:45.742488');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (22, 18, 1, 1, 'POL-18-1-1', NULL, NULL, 150.00, true, '2026-09-22 06:07:45.746779');
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, codigobarra, imagenurl, precioventa, activo, fechacreacion) VALUES (23, 23, 1, 1, 'POL-23-1-1', NULL, NULL, 120.00, true, '2026-09-22 06:18:50.484696');


--
-- Data for Name: venta; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.venta (id, codigoventa, tipoventa, estado, subtotal, descuento, total, fecha, sucursalid, clienteid, usuarioid) VALUES (1, 'ORD-202609220453-994', 'Digital', 'Completada', 130.00, 0.00, 130.00, '2026-09-22 04:53:56.777065', 1, 24, 14);
INSERT INTO public.venta (id, codigoventa, tipoventa, estado, subtotal, descuento, total, fecha, sucursalid, clienteid, usuarioid) VALUES (2, 'POS-202609220659-766', 'Presencial', 'Completada', 80.00, 0.00, 80.00, '2026-09-22 06:59:10.927043', 3, 31, 1);
INSERT INTO public.venta (id, codigoventa, tipoventa, estado, subtotal, descuento, total, fecha, sucursalid, clienteid, usuarioid) VALUES (3, 'POS-202609220721-776', 'Presencial', 'Completada', 199.50, 0.00, 199.50, '2026-09-22 07:21:11.073231', 3, 31, 1);


--
-- Name: bitacora_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.bitacora_id_seq', 51, true);


--
-- Name: carrito_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.carrito_id_seq', 11, true);


--
-- Name: categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categoria_id_seq', 13, true);


--
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cliente_id_seq', 31, true);


--
-- Name: coleccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.coleccion_id_seq', 1, false);


--
-- Name: color_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.color_id_seq', 10, true);


--
-- Name: inventario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inventario_id_seq', 69, true);


--
-- Name: inventario_sucursal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inventario_sucursal_id_seq', 1, false);


--
-- Name: metodo_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.metodo_pago_id_seq', 5, true);


--
-- Name: movimiento_inventario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.movimiento_inventario_id_seq', 3, true);


--
-- Name: notificacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notificacion_id_seq', 1, false);


--
-- Name: pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pago_id_seq', 1, true);


--
-- Name: producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.producto_id_seq', 23, true);


--
-- Name: proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.proveedor_id_seq', 7, true);


--
-- Name: recibo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.recibo_id_seq', 1, false);


--
-- Name: reserva_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reserva_id_seq', 1, false);


--
-- Name: rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rol_id_seq', 4, true);


--
-- Name: sucursal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sucursal_id_seq', 3, true);


--
-- Name: talla_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.talla_id_seq', 5, true);


--
-- Name: temporada_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.temporada_id_seq', 2, true);


--
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuario_id_seq', 21, true);


--
-- Name: variante_producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.variante_producto_id_seq', 23, true);


--
-- Name: venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.venta_id_seq', 3, true);


--
-- Name: bitacora bitacora_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bitacora
    ADD CONSTRAINT bitacora_pkey PRIMARY KEY (id);


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
-- Name: inventario inventario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_pkey PRIMARY KEY (id);


--
-- Name: inventario_sucursal inventario_sucursal_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario_sucursal
    ADD CONSTRAINT inventario_sucursal_pkey PRIMARY KEY (id);


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
-- Name: notificacion notificacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notificacion
    ADD CONSTRAINT notificacion_pkey PRIMARY KEY (id);


--
-- Name: pago pago_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id);


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
-- Name: rol rol_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_nombre_key UNIQUE (nombre);


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
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


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
-- Name: venta venta_codigoventa_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_codigoventa_key UNIQUE (codigoventa);


--
-- Name: venta venta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_pkey PRIMARY KEY (id);


--
-- Name: ix_bitacora_accion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_accion ON public.bitacora USING btree (accion);


--
-- Name: ix_bitacora_accion_fechahora; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_accion_fechahora ON public.bitacora USING btree (accion, fechahora);


--
-- Name: ix_bitacora_fechahora; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_fechahora ON public.bitacora USING btree (fechahora);


--
-- Name: ix_bitacora_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_id ON public.bitacora USING btree (id);


--
-- Name: ix_bitacora_modulo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_modulo ON public.bitacora USING btree (modulo);


--
-- Name: ix_bitacora_modulo_fechahora; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_modulo_fechahora ON public.bitacora USING btree (modulo, fechahora);


--
-- Name: ix_bitacora_usuarioid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bitacora_usuarioid ON public.bitacora USING btree (usuarioid);


--
-- Name: ix_carrito_clienteid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_carrito_clienteid ON public.carrito USING btree (clienteid);


--
-- Name: ix_carrito_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_carrito_id ON public.carrito USING btree (id);


--
-- Name: ix_carrito_sucursalid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_carrito_sucursalid ON public.carrito USING btree (sucursalid);


--
-- Name: ix_categoria_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_categoria_id ON public.categoria USING btree (id);


--
-- Name: ix_cliente_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cliente_id ON public.cliente USING btree (id);


--
-- Name: ix_coleccion_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_coleccion_id ON public.coleccion USING btree (id);


--
-- Name: ix_color_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_color_id ON public.color USING btree (id);


--
-- Name: ix_inventario_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_inventario_id ON public.inventario USING btree (id);


--
-- Name: ix_inventario_sucursal_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_inventario_sucursal_id ON public.inventario_sucursal USING btree (id);


--
-- Name: ix_inventario_sucursal_sucursalid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_inventario_sucursal_sucursalid ON public.inventario_sucursal USING btree (sucursalid);


--
-- Name: ix_inventario_sucursal_varianteid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_inventario_sucursal_varianteid ON public.inventario_sucursal USING btree (varianteid);


--
-- Name: ix_metodo_pago_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_metodo_pago_id ON public.metodo_pago USING btree (id);


--
-- Name: ix_movimiento_inventario_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_movimiento_inventario_id ON public.movimiento_inventario USING btree (id);


--
-- Name: ix_notificacion_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notificacion_id ON public.notificacion USING btree (id);


--
-- Name: ix_notificacion_usuario_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notificacion_usuario_id ON public.notificacion USING btree (usuario_id);


--
-- Name: ix_pago_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_pago_id ON public.pago USING btree (id);


--
-- Name: ix_producto_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_producto_id ON public.producto USING btree (id);


--
-- Name: ix_proveedor_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_proveedor_id ON public.proveedor USING btree (id);


--
-- Name: ix_recibo_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recibo_id ON public.recibo USING btree (id);


--
-- Name: ix_reserva_clienteid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reserva_clienteid ON public.reserva USING btree (clienteid);


--
-- Name: ix_reserva_codigoreserva; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_reserva_codigoreserva ON public.reserva USING btree (codigoreserva);


--
-- Name: ix_reserva_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reserva_id ON public.reserva USING btree (id);


--
-- Name: ix_reserva_sucursalid; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_reserva_sucursalid ON public.reserva USING btree (sucursalid);


--
-- Name: ix_sucursal_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sucursal_id ON public.sucursal USING btree (id);


--
-- Name: ix_talla_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_talla_id ON public.talla USING btree (id);


--
-- Name: ix_temporada_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_temporada_id ON public.temporada USING btree (id);


--
-- Name: ix_variante_producto_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_variante_producto_id ON public.variante_producto USING btree (id);


--
-- Name: ix_venta_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_venta_id ON public.venta USING btree (id);


--
-- Name: bitacora bitacora_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bitacora
    ADD CONSTRAINT bitacora_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id) ON DELETE SET NULL;


--
-- Name: carrito carrito_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.usuario(id) ON DELETE CASCADE;


--
-- Name: carrito_item carrito_item_carritoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito_item
    ADD CONSTRAINT carrito_item_carritoid_fkey FOREIGN KEY (carritoid) REFERENCES public.carrito(id) ON DELETE CASCADE;


--
-- Name: carrito_item carrito_item_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito_item
    ADD CONSTRAINT carrito_item_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON DELETE RESTRICT;


--
-- Name: carrito carrito_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON DELETE RESTRICT;


--
-- Name: cliente cliente_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id) ON DELETE CASCADE;


--
-- Name: coleccion coleccion_temporadaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coleccion
    ADD CONSTRAINT coleccion_temporadaid_fkey FOREIGN KEY (temporadaid) REFERENCES public.temporada(id);


--
-- Name: detalle_venta detalle_venta_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id);


--
-- Name: detalle_venta detalle_venta_ventaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_ventaid_fkey FOREIGN KEY (ventaid) REFERENCES public.venta(id);


--
-- Name: inventario_sucursal inventario_sucursal_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario_sucursal
    ADD CONSTRAINT inventario_sucursal_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON DELETE CASCADE;


--
-- Name: inventario_sucursal inventario_sucursal_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario_sucursal
    ADD CONSTRAINT inventario_sucursal_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON DELETE CASCADE;


--
-- Name: inventario inventario_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id);


--
-- Name: inventario inventario_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id);


--
-- Name: movimiento_inventario movimiento_inventario_inventarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario
    ADD CONSTRAINT movimiento_inventario_inventarioid_fkey FOREIGN KEY (inventarioid) REFERENCES public.inventario(id);


--
-- Name: movimiento_inventario movimiento_inventario_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.movimiento_inventario
    ADD CONSTRAINT movimiento_inventario_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id);


--
-- Name: notificacion notificacion_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notificacion
    ADD CONSTRAINT notificacion_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id) ON DELETE CASCADE;


--
-- Name: pago pago_metodoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_metodoid_fkey FOREIGN KEY (metodoid) REFERENCES public.metodo_pago(id);


--
-- Name: pago pago_reciboid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_reciboid_fkey FOREIGN KEY (reciboid) REFERENCES public.recibo(id);


--
-- Name: pago pago_ventaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_ventaid_fkey FOREIGN KEY (ventaid) REFERENCES public.venta(id);


--
-- Name: producto producto_categoriaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_categoriaid_fkey FOREIGN KEY (categoriaid) REFERENCES public.categoria(id);


--
-- Name: producto_proveedor producto_proveedor_idproducto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_proveedor
    ADD CONSTRAINT producto_proveedor_idproducto_fkey FOREIGN KEY (idproducto) REFERENCES public.producto(id);


--
-- Name: producto_proveedor producto_proveedor_idproveedor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto_proveedor
    ADD CONSTRAINT producto_proveedor_idproveedor_fkey FOREIGN KEY (idproveedor) REFERENCES public.proveedor(id);


--
-- Name: reserva reserva_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.usuario(id) ON DELETE CASCADE;


--
-- Name: reserva_detalle reserva_detalle_reservaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva_detalle
    ADD CONSTRAINT reserva_detalle_reservaid_fkey FOREIGN KEY (reservaid) REFERENCES public.reserva(id) ON DELETE CASCADE;


--
-- Name: reserva_detalle reserva_detalle_varianteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva_detalle
    ADD CONSTRAINT reserva_detalle_varianteid_fkey FOREIGN KEY (varianteid) REFERENCES public.variante_producto(id) ON DELETE RESTRICT;


--
-- Name: reserva reserva_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id) ON DELETE RESTRICT;


--
-- Name: usuario usuario_rolid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_rolid_fkey FOREIGN KEY (rolid) REFERENCES public.rol(id) ON DELETE SET NULL;


--
-- Name: variante_producto variante_producto_colorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_colorid_fkey FOREIGN KEY (colorid) REFERENCES public.color(id);


--
-- Name: variante_producto variante_producto_productoid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_productoid_fkey FOREIGN KEY (productoid) REFERENCES public.producto(id);


--
-- Name: variante_producto variante_producto_tallaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.variante_producto
    ADD CONSTRAINT variante_producto_tallaid_fkey FOREIGN KEY (tallaid) REFERENCES public.talla(id);


--
-- Name: venta venta_clienteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_clienteid_fkey FOREIGN KEY (clienteid) REFERENCES public.cliente(id);


--
-- Name: venta venta_sucursalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_sucursalid_fkey FOREIGN KEY (sucursalid) REFERENCES public.sucursal(id);


--
-- Name: venta venta_usuarioid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES public.usuario(id);


--
-- PostgreSQL database dump complete
--


