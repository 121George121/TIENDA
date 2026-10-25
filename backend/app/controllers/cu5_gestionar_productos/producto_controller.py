# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU5 - Gestionar Productos y Catálogo Retail (Multi-Tenant SaaS)
# Ubicación: backend/app/controllers/cu5_gestionar_productos/producto_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.cu5_gestionar_productos.producto_service import ProductoService
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate
from app.models.models import Producto


class ProductoController:
    """
    Controlador MVC para la administración del catálogo de prendas y productos.
    Garantiza aislamiento por tenant, validación de cuotas de inventario y trazabilidad.
    """

    @staticmethod
    def listar_productos(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Producto]:
        """Lista el catálogo de productos con filtros y aislamiento por tenant"""
        return ProductoService.listar_productos(
            db=db,
            tenant_id=tenant_id,
            search=search,
            categoria_id=categoria_id,
            genero=genero,
            activo=activo,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def obtener_producto_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Producto:
        """Obtiene el detalle de un producto verificando su pertenencia al tenant"""
        return ProductoService.obtener_producto_por_id(
            db=db,
            id=id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_producto(
        db: Session,
        data: ProductoCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Producto:
        """Registra un nuevo producto validando la cuota máxima permitida por el plan"""
        return ProductoService.crear_producto(
            db=db,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def actualizar_producto(
        db: Session,
        id: int,
        data: ProductoUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Producto:
        """Actualiza los datos comerciales y clasificación del producto"""
        return ProductoService.actualizar_producto(
            db=db,
            id=id,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def cambiar_estado_producto(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Producto:
        """Activa o suspende la visibilidad del producto en el catálogo"""
        return ProductoService.cambiar_estado_producto(
            db=db,
            id=id,
            activo=activo,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def eliminar_producto(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Elimina un producto de la base de datos o lo desactiva si tiene ventas registradas"""
        return ProductoService.eliminar_producto(
            db=db,
            id=id,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
ProductController = ProductoController

ProductoController.obtener_producto = ProductoController.obtener_producto_por_id
ProductoController.cambiar_estado = ProductoController.cambiar_estado_producto
ProductoController.baja_logica = ProductoController.eliminar_producto

ProductoController.get_all = ProductoController.listar_productos
ProductoController.get_by_id = ProductoController.obtener_producto_por_id
ProductoController.create = ProductoController.crear_producto
ProductoController.update = ProductoController.actualizar_producto
ProductoController.toggle_status = ProductoController.cambiar_estado_producto
ProductoController.delete = ProductoController.eliminar_producto
ProductoController.logical_delete = ProductoController.eliminar_producto
