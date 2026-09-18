# ==============================================================================
# CU18 - GESTIONAR RECOMENDACIONES MEDIANTE IA -> VISTAS / RUTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu18_gestionar_recomendaciones_ia/recomendacion_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.controllers.cu18_gestionar_recomendaciones_ia.recomendacion_controller import RecomendacionController

router = APIRouter(prefix="/recomendaciones", tags=["CU18 - Gestionar Recomendaciones mediante IA (Web y Móvil)"])


class OutfitRequest(BaseModel):
    producto_id: Optional[int] = None
    carrito_ids: Optional[List[int]] = None
    limite: int = 3


@router.post("/outfit", summary="Generar recomendaciones de outfit con Gemini AI / Stylist")
def recomendar_outfit(
    data: OutfitRequest,
    db: Session = Depends(get_db)
):
    """
    CU18: Sugiere prendas complementarias para armar un outfit completo,
    analizando color, corte y estilo mediante Gemini AI.
    """
    return RecomendacionController.recomendar_outfit(
        db=db,
        producto_id=data.producto_id,
        carrito_ids=data.carrito_ids,
        limite=data.limite
    )


@router.get("/tendencias", summary="Obtener prendas en tendencia recomendadas")
def obtener_tendencias(
    limite: int = Query(4, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """CU18: Retorna productos destacados en tendencia para inspiración del comprador."""
    return RecomendacionController.obtener_tendencias(db=db, limite=limite)
