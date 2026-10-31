# ==============================================================================
# CU13 - GESTIONAR INVENTARIO Y MOVIMIENTOS -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu13_gestionar_inventario_movimientos/inventario_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Header, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff, require_admin
from app.models.models import UsuarioModel
from app.schemas.inventario_schema import (
    InventarioResponse,
    MovimientoInventarioCreate,
    StockMinimoUpdate,
    MovimientoInventarioResponse,
    TrasladoStockRequest,
    TrasladoStockResponse,
)
from app.controllers.cu13_gestionar_inventario_movimientos.inventario_controller import (
    InventarioController,
)

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario y Almacén (CU13 - Vista API)"],
    dependencies=[Depends(require_staff)],
)


def _resolver_tenant_id(
    x_tenant_id: Optional[int], current_user: Optional[UsuarioModel]
) -> int:
    if x_tenant_id is not None:
        return x_tenant_id
    if current_user and getattr(current_user, "tenant_id", None):
        return current_user.tenant_id
    return 1


@router.get("", response_model=List[InventarioResponse], summary="Listar inventario de prendas por sucursal")
def listar_inventario(
    sucursal_id: Optional[int] = Query(None, description="Filtrar por ID de sucursal"),
    search: Optional[str] = Query(None, description="Buscar por nombre de prenda, marca o SKU"),
    solo_bajo_stock: Optional[bool] = Query(False, description="Filtrar solo productos que requieran reabastecimiento"),
    skip: int = 0,
    limit: int = 100,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """Consulta de existencias físicas, existencias reservadas y disponibilidad con aislamiento multitenant"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    return InventarioController.listar_inventario(
        db=db,
        sucursal_id=sucursal_id,
        search=search,
        solo_bajo_stock=solo_bajo_stock,
        skip=skip,
        limit=limit,
        tenant_id=tenant_id,
    )


@router.get("/{inventario_id}", response_model=InventarioResponse, summary="Obtener detalle de un ítem de inventario")
def obtener_detalle(
    inventario_id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """Obtiene el estado de stock físico y reservado de un registro específico de inventario"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    return InventarioController.obtener_detalle_inventario(
        db=db,
        inventario_id=inventario_id,
        tenant_id=tenant_id,
    )


@router.post("/{inventario_id}/movimiento", summary="Registrar movimiento manual de inventario (Kardex)")
def registrar_movimiento(
    inventario_id: int,
    data: MovimientoInventarioCreate,
    request: Request,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """Registra una Entrada, Salida o Ajuste manual de stock en el almacén con control de reservas activas"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    ip_origen = request.client.host if request.client else "127.0.0.1"
    return InventarioController.registrar_movimiento(
        db=db,
        current_user=current_user,
        inventario_id=inventario_id,
        data=data,
        tenant_id=tenant_id,
        ip_origen=ip_origen,
    )


@router.post("/{inventario_id}/traslado", response_model=TrasladoStockResponse, summary="Trasladar prendas entre sucursales")
def trasladar_stock(
    inventario_id: int,
    data: TrasladoStockRequest,
    request: Request,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """
    Traslada existencias físicas entre sucursales de la misma empresa (tenant).
    Valida disponibilidad, descuenta origen e incrementa destino con doble kardex.
    """
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    ip_origen = request.client.host if request.client else "127.0.0.1"
    return InventarioController.trasladar_stock(
        db=db,
        current_user=current_user,
        inventario_origen_id=inventario_id,
        data=data,
        tenant_id=tenant_id,
        ip_origen=ip_origen,
    )


@router.put("/{inventario_id}/stock-minimo", summary="Actualizar umbral de stock mínimo de seguridad")
def actualizar_stock_minimo(
    inventario_id: int,
    data: StockMinimoUpdate,
    request: Request,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin),
):
    """Permite al administrador modificar el nivel de stock de seguridad para alertas de reabastecimiento"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    ip_origen = request.client.host if request.client else "127.0.0.1"
    return InventarioController.actualizar_stock_minimo(
        db=db,
        inventario_id=inventario_id,
        data=data,
        current_user=current_user,
        tenant_id=tenant_id,
        ip_origen=ip_origen,
    )


@router.get("/{inventario_id}/movimientos", response_model=List[MovimientoInventarioResponse], summary="Consultar historial de movimientos (Kardex)")
def consultar_kardex(
    inventario_id: int,
    limit: int = 50,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff),
):
    """Obtiene el historial cronológico de entradas, salidas y traslados de una prenda en sucursal"""
    tenant_id = _resolver_tenant_id(x_tenant_id, current_user)
    return InventarioController.obtener_kardex(
        db=db,
        inventario_id=inventario_id,
        limit=limit,
        tenant_id=tenant_id,
    )
