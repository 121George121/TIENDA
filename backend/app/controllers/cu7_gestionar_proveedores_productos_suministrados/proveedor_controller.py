# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU7 - Gestionar Proveedores y Productos Suministrados (Multi-Tenant SaaS)
# Ubicación: backend/app/controllers/cu7_gestionar_proveedores_productos_suministrados/proveedor_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import Proveedor, ProductoProveedor
from app.services.cu7_gestionar_proveedores_productos_suministrados.proveedor_service import ProveedorService
from app.schemas.proveedor_schema import (
    ProveedorCreate, ProveedorUpdate, ProductoProveedorCreate
)


class ProveedorController:
    """
    Controlador MVC para la administración de proveedores y su catálogo de suministros.
    Garantiza aislamiento por tenant, trazabilidad y control de costos.
    """

    @staticmethod
    def listar_proveedores(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Proveedor]:
        """Lista los proveedores registrados para el tenant"""
        return ProveedorService.listar_proveedores(
            db=db,
            tenant_id=tenant_id,
            search=search,
            activo=activo,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def obtener_proveedor_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Proveedor:
        """Obtiene el detalle completo de un proveedor por ID"""
        return ProveedorService.obtener_proveedor_por_id(
            db=db,
            id=id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_proveedor(
        db: Session,
        data: ProveedorCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Proveedor:
        """Registra un nuevo proveedor en el tenant"""
        return ProveedorService.crear_proveedor(
            db=db,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def actualizar_proveedor(
        db: Session,
        id: int,
        data: ProveedorUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Proveedor:
        """Actualiza los datos del proveedor"""
        return ProveedorService.actualizar_proveedor(
            db=db,
            id=id,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def cambiar_estado_proveedor(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Proveedor:
        """Activa o suspende el estado comercial del proveedor"""
        return ProveedorService.cambiar_estado_proveedor(
            db=db,
            id=id,
            activo=activo,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def eliminar_proveedor(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Elimina definitivamente o aplica baja lógica si tiene suministros"""
        return ProveedorService.eliminar_proveedor(
            db=db,
            id=id,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def vincular_producto_suministrado(
        db: Session,
        data: ProductoProveedorCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> ProductoProveedor:
        """Vincula un producto al proveedor con su respectivo costo de compra"""
        return ProveedorService.vincular_producto_suministrado(
            db=db,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def listar_productos_suministrados(
        db: Session,
        proveedor_id: int,
        tenant_id: int = 1
    ) -> List[ProductoProveedor]:
        """Lista los productos suministrados por un proveedor"""
        return ProveedorService.listar_productos_suministrados(
            db=db,
            proveedor_id=proveedor_id,
            tenant_id=tenant_id
        )


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
ProveedorController.obtener_proveedor = ProveedorController.obtener_proveedor_por_id
ProveedorController.baja_proveedor = ProveedorController.eliminar_proveedor
ProveedorController.vincular_producto = ProveedorController.vincular_producto_suministrado

ProveedorController.get_all = ProveedorController.listar_proveedores
ProveedorController.get_by_id = ProveedorController.obtener_proveedor_por_id
ProveedorController.create = ProveedorController.crear_proveedor
ProveedorController.update = ProveedorController.actualizar_proveedor
ProveedorController.delete = ProveedorController.eliminar_proveedor

SupplierController = ProveedorController
