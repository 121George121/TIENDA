# ==============================================================================
# CU13 - GESTIONAR INVENTARIO Y MOVIMIENTOS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu13_gestionar_inventario_movimientos/inventario_controller.py
# ==============================================================================

from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from app.models.models import UsuarioModel
from app.schemas.inventario_schema import (
    MovimientoInventarioCreate,
    StockMinimoUpdate,
    TrasladoStockRequest,
)
from app.services.cu13_gestionar_inventario_movimientos.inventario_service import (
    InventarioService,
)


class InventarioController:
    """
    Controlador MVC para el Caso de Uso CU13: Gestionar Inventario y Movimientos.
    Orquesta las solicitudes de la vista API y delega la lógica de negocio al
    InventarioService con soporte multi-tenant y trazabilidad en Bitácora.
    """

    @classmethod
    def _asegurar_variantes_e_inventario(cls, db: Session, tenant_id: int = 1) -> None:
        return InventarioService.asegurar_variantes_e_inventario(db, tenant_id=tenant_id)

    @classmethod
    def listar_inventario(
        cls,
        db: Session,
        sucursal_id: Optional[int] = None,
        search: Optional[str] = None,
        solo_bajo_stock: Optional[bool] = False,
        skip: int = 0,
        limit: int = 100,
        tenant_id: int = 1,
    ) -> List[Dict]:
        return InventarioService.listar_inventario(
            db=db,
            sucursal_id=sucursal_id,
            search=search,
            solo_bajo_stock=solo_bajo_stock,
            skip=skip,
            limit=limit,
            tenant_id=tenant_id,
        )

    @classmethod
    def obtener_detalle_inventario(
        cls,
        db: Session,
        inventario_id: int,
        tenant_id: int = 1,
    ) -> Dict:
        return InventarioService.obtener_detalle_inventario(
            db=db,
            inventario_id=inventario_id,
            tenant_id=tenant_id,
        )

    @classmethod
    def registrar_movimiento(
        cls,
        db: Session,
        current_user: UsuarioModel,
        inventario_id: int,
        data: MovimientoInventarioCreate,
        tenant_id: int = 1,
        ip_origen: str = "127.0.0.1",
    ) -> Dict:
        return InventarioService.registrar_movimiento(
            db=db,
            inventario_id=inventario_id,
            data=data,
            usuario_id=current_user.id,
            tenant_id=tenant_id,
            ip_origen=ip_origen,
        )

    @classmethod
    def trasladar_stock(
        cls,
        db: Session,
        current_user: UsuarioModel,
        inventario_origen_id: int,
        data: TrasladoStockRequest,
        tenant_id: int = 1,
        ip_origen: str = "127.0.0.1",
    ) -> Dict:
        return InventarioService.trasladar_stock(
            db=db,
            inventario_origen_id=inventario_origen_id,
            data=data,
            usuario_id=current_user.id,
            tenant_id=tenant_id,
            ip_origen=ip_origen,
        )

    @classmethod
    def actualizar_stock_minimo(
        cls,
        db: Session,
        inventario_id: int,
        data: StockMinimoUpdate,
        current_user: Optional[UsuarioModel] = None,
        tenant_id: int = 1,
        ip_origen: str = "127.0.0.1",
    ) -> Dict:
        usuario_id = current_user.id if current_user else 1
        return InventarioService.actualizar_stock_minimo(
            db=db,
            inventario_id=inventario_id,
            data=data,
            usuario_id=usuario_id,
            tenant_id=tenant_id,
            ip_origen=ip_origen,
        )

    @classmethod
    def obtener_kardex(
        cls,
        db: Session,
        inventario_id: int,
        limit: int = 50,
        tenant_id: int = 1,
    ) -> List[Dict]:
        return InventarioService.obtener_kardex(
            db=db,
            inventario_id=inventario_id,
            limit=limit,
            tenant_id=tenant_id,
        )


# ==============================================================================
# ALIASES DE COMPATIBILIDAD (CONVENCIONES EN ESPAÑOL Y DIAGRAMAS)
# ==============================================================================
InventarioController.listar = InventarioController.listar_inventario
InventarioController.movimiento = InventarioController.registrar_movimiento
InventarioController.traslado = InventarioController.trasladar_stock
InventarioController.kardex = InventarioController.obtener_kardex
