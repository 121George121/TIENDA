# ==============================================================================
# CAPA MODELO (MVC - MODEL)
# Entidades de la Base de Datos PostgreSQL (rol, usuario, sucursal, categoria, temporada, coleccion, producto, color, talla, variante, proveedor, producto_proveedor)
# ==============================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class RolModel(Base):
    __tablename__ = "rol"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    usuarios = relationship("UsuarioModel", back_populates="rol")

class SucursalModel(Base):
    __tablename__ = "sucursal"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    latitud = Column(Numeric(10, 8), nullable=True)
    longitud = Column(Numeric(11, 8), nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("UsuarioModel", back_populates="sucursal")

class UsuarioModel(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    passwordhash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    rolid = Column(Integer, ForeignKey("rol.id"), nullable=True)
    sucursalid = Column(Integer, ForeignKey("sucursal.id"), nullable=True)
    activo = Column(Boolean, default=True)
    verificado = Column(Boolean, default=False)
    codigoverificacion = Column(String(255), nullable=True)
    codigoexpiracion = Column(DateTime, nullable=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    rol = relationship("RolModel", back_populates="usuarios")
    sucursal = relationship("SucursalModel", back_populates="usuarios")

    @property
    def created_at(self):
        return self.fechacreacion

    @property
    def rol_id(self):
        return self.rolid

class CategoriaModel(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    productos = relationship("ProductoModel", back_populates="categoria")

class TemporadaModel(Base):
    __tablename__ = "temporada"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fechainicio = Column(Date, nullable=True)
    fechafin = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)

    colecciones = relationship("ColeccionModel", back_populates="temporada")

class ColeccionModel(Base):
    __tablename__ = "coleccion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagenurl = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    temporadaid = Column(Integer, ForeignKey("temporada.id"), nullable=True)

    temporada = relationship("TemporadaModel", back_populates="colecciones")

class ProductoModel(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    marca = Column(String(100), nullable=True)
    genero = Column(String(50), nullable=True)
    grupoedad = Column(String(50), nullable=True)
    preciobase = Column(Numeric(10, 2), nullable=False, default=0.00)
    imagenprincipal = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    categoriaid = Column(Integer, ForeignKey("categoria.id"), nullable=True)

    categoria = relationship("CategoriaModel", back_populates="productos")
    variantes = relationship("VarianteProductoModel", back_populates="producto")

class ColorModel(Base):
    __tablename__ = "color"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    codigohex = Column(String(10), nullable=True)
    activo = Column(Boolean, default=True)

class TallaModel(Base):
    __tablename__ = "talla"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), nullable=False)
    grupoedad = Column(String(50), nullable=True)
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True)

class VarianteProductoModel(Base):
    __tablename__ = "variante_producto"

    id = Column(Integer, primary_key=True, index=True)
    productoid = Column(Integer, ForeignKey("producto.id"), nullable=False)
    colorid = Column(Integer, ForeignKey("color.id"), nullable=True)
    tallaid = Column(Integer, ForeignKey("talla.id"), nullable=True)
    sku = Column(String(50), nullable=True)
    codigobarra = Column(String(100), nullable=True)
    imagenurl = Column(Text, nullable=True)
    precioventa = Column(Numeric(10, 2), nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    producto = relationship("ProductoModel", back_populates="variantes")
    color = relationship("ColorModel")
    talla = relationship("TallaModel")

class ProveedorModel(Base):
    __tablename__ = "proveedor"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    razonsocial = Column(String(150), nullable=True)
    nit = Column(String(50), nullable=True)
    contacto = Column(String(100), nullable=True)
    telefono = Column(String(30), nullable=True)
    email = Column(String(150), nullable=True)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)

    productos_suministrados = relationship("ProductoProveedorModel", back_populates="proveedor")

class ProductoProveedorModel(Base):
    __tablename__ = "producto_proveedor"

    idproducto = Column(Integer, ForeignKey("producto.id"), primary_key=True)
    idproveedor = Column(Integer, ForeignKey("proveedor.id"), primary_key=True)
    costocompra = Column(Numeric(10, 2), nullable=True)
    cantidad = Column(Integer, default=0)

    proveedor = relationship("ProveedorModel", back_populates="productos_suministrados")
    producto = relationship("ProductoModel")


class InventarioSucursalModel(Base):
    __tablename__ = "inventario_sucursal"

    id = Column(Integer, primary_key=True, index=True)
    varianteid = Column(Integer, ForeignKey("variante_producto.id", ondelete="CASCADE"), nullable=False, index=True)
    sucursalid = Column(Integer, ForeignKey("sucursal.id", ondelete="CASCADE"), nullable=False, index=True)
    cantidad = Column(Integer, default=0, nullable=False) # stock físico
    stockreservado = Column(Integer, default=0, nullable=False) # stock apartado para reservas
    stockminimo = Column(Integer, default=5, nullable=True)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    variante = relationship("VarianteProductoModel", backref="inventarios")
    sucursal = relationship("SucursalModel", backref="inventarios")


class CarritoModel(Base):
    __tablename__ = "carrito"

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50), default="ACTIVO", nullable=False) # ACTIVO, ABANDONADO, CONVERTIDO
    fechacreacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fechaactualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    clienteid = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True)
    sucursalid = Column(Integer, ForeignKey("sucursal.id", ondelete="RESTRICT"), nullable=True, index=True)

    cliente = relationship("UsuarioModel", backref="carritos")
    sucursal = relationship("SucursalModel", backref="carritos")
    items = relationship("CarritoItemModel", back_populates="carrito", cascade="all, delete-orphan")


class CarritoItemModel(Base):
    __tablename__ = "carrito_item"

    carritoid = Column(Integer, ForeignKey("carrito.id", ondelete="CASCADE"), primary_key=True)
    varianteid = Column(Integer, ForeignKey("variante_producto.id", ondelete="RESTRICT"), primary_key=True)
    cantidad = Column(Integer, default=1, nullable=False)
    preciounitario = Column(Numeric(12, 2), nullable=False)
    fechaagregado = Column(DateTime, default=datetime.utcnow)

    carrito = relationship("CarritoModel", back_populates="items")
    variante = relationship("VarianteProductoModel")
