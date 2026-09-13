# ==============================================================================
# CU13 - GESTIONAR INVENTARIO Y MOVIMIENTOS -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu13_gestionar_inventario_movimientos/inventario_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import require_staff, require_admin
from app.models.models import UsuarioModel
from app.schemas.inventario_schema import (
    InventarioResponse,
    MovimientoInventarioCreate,
    StockMinimoUpdate,
    MovimientoInventarioResponse
)
from app.controllers.cu13_gestionar_inventario_movimientos.inventario_controller import InventarioController

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario y Almacén (CU13 - Vista API)"],
    dependencies=[Depends(require_staff)]
)


@router.get("", response_model=List[InventarioResponse], summary="Listar inventario de poleras por sucursal")
def listar_inventario(
    sucursal_id: Optional[int] = Query(None, description="Filtrar por ID de sucursal"),
    search: Optional[str] = Query(None, description="Buscar por nombre de polera, marca o SKU"),
    solo_bajo_stock: Optional[bool] = Query(False, description="Filtrar solo productos que requieran reabastecimiento"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Consulta de existencias físicas y niveles de stock mínimo"""
    return InventarioController.listar_inventario(
        db=db,
        sucursal_id=sucursal_id,
        search=search,
        solo_bajo_stock=solo_bajo_stock,
        skip=skip,
        limit=limit
    )


@router.post("/{inventario_id}/movimiento", summary="Registrar movimiento manual de inventario (Kardex)")
def registrar_movimiento(
    inventario_id: int,
    data: MovimientoInventarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_staff)
):
    """Registra una Entrada, Salida o Ajuste manual de stock en el almacén"""
    return InventarioController.registrar_movimiento(
        db=db,
        current_user=current_user,
        inventario_id=inventario_id,
        data=data
    )


@router.put("/{inventario_id}/stock-minimo", summary="Actualizar umbral de stock mínimo de seguridad")
def actualizar_stock_minimo(
    inventario_id: int,
    data: StockMinimoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(require_admin)
):
    """Permite al administrador modificar el nivel de stock de seguridad para alertas"""
    return InventarioController.actualizar_stock_minimo(
        db=db,
        inventario_id=inventario_id,
        data=data
    )


@router.get("/{inventario_id}/movimientos", response_model=List[MovimientoInventarioResponse], summary="Consultar historial de movimientos (Kardex)")
def consultar_kardex(
    inventario_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Obtiene el historial cronológico de entradas y salidas de una prenda"""
    return InventarioController.obtener_kardex(db=db, inventario_id=inventario_id, limit=limit)
