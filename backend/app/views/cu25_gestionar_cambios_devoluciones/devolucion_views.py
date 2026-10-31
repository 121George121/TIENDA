# ==============================================================================
# CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu25_gestionar_cambios_devoluciones/devolucion_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu25_gestionar_cambios_devoluciones.devolucion_controller import DevolucionController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/devoluciones", tags=["CU25 - Cambios y Devoluciones"])


class ItemDevolucionRequest(BaseModel):
    variante_devuelta_id: int
    variante_nueva_id: Optional[int] = None
    cantidad: int = 1
    precio_unitario: float = 0.0
    subtotal: float = 0.0
    estado_prenda: str = "PERFECTO_ESTADO"


class SolicitudDevolucionRequest(BaseModel):
    venta_id: int
    sucursal_id: int
    cliente_id: Optional[int] = None
    tipo_devolucion: str  # CAMBIO_TALLA, CAMBIO_PRENDA, REEMBOLSO_TOTAL, NOTA_CREDITO
    motivo: str
    monto_reembolso: float = 0.0
    items: List[ItemDevolucionRequest]


@router.post("/solicitar", summary="Registrar solicitud y ejecución de cambio de prenda o devolución")
def solicitar_devolucion(
    req: SolicitudDevolucionRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    items_dict = [it.dict() for it in req.items]
    devolucion = DevolucionController.procesar_devolucion(
        db=db,
        tenant_id=tenant_id,
        venta_id=req.venta_id,
        cliente_id=req.cliente_id,
        usuario_id=current_user.id,
        sucursal_id=req.sucursal_id,
        tipo_devolucion=req.tipo_devolucion,
        motivo=req.motivo,
        monto_reembolso=req.monto_reembolso,
        items=items_dict
    )
    return {"exito": True, "devolucion": devolucion}


@router.get("/", summary="Listar cambios y devoluciones de prendas registradas")
def listar_devoluciones(
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    tenant_id = getattr(current_user, "tenant_id", 1) or 1
    devoluciones = DevolucionController.listar_devoluciones(db, tenant_id, sucursal_id)
    return {"exito": True, "devoluciones": devoluciones}
