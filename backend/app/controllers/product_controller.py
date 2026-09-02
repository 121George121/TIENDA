# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Contiene la Lógica de Negocio y Operaciones de Base de Datos para Productos
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import ProductoModel
from app.schemas.schemas import ProductoCreate
from fastapi import HTTPException, status

class ProductoController:

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        """Obtiene la lista de productos activos de la tienda"""
        return db.query(ProductoModel).filter(ProductoModel.activo == True).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, producto_id: int):
        """Obtiene un producto por su ID"""
        producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id, ProductoModel.activo == True).first()
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return producto

    @staticmethod
    def create(db: Session, producto_data: ProductoCreate):
        """Crea un nuevo producto en el catálogo"""
        nuevo_producto = ProductoModel(
            nombre=producto_data.nombre,
            descripcion=producto_data.descripcion,
            precio=producto_data.precio,
            stock=producto_data.stock,
            categoria_id=producto_data.categoria_id,
            imagen_url=producto_data.imagen_url
        )
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto)
        return nuevo_producto

    @staticmethod
    def update(db: Session, producto_id: int, producto_data: ProductoCreate):
        """Actualiza la información de un producto existente"""
        producto = ProductoController.get_by_id(db, producto_id)
        producto.nombre = producto_data.nombre
        producto.descripcion = producto_data.descripcion
        producto.precio = producto_data.precio
        producto.stock = producto_data.stock
        producto.categoria_id = producto_data.categoria_id
        producto.imagen_url = producto_data.imagen_url
        
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def delete(db: Session, producto_id: int):
        """Eliminación lógica de un producto"""
        producto = ProductoController.get_by_id(db, producto_id)
        producto.activo = False
        db.commit()
        return {"message": f"Producto {producto_id} desactivado correctamente"}
