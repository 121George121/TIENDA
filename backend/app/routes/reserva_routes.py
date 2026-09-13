# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER - FACHADA RETROCOMPATIBLE)
# Módulo: CU10 y CU11 - Gestión y Atención de Reservas de Prendas
# Ubicación: backend/app/routes/reserva_routes.py
# ==============================================================================

from fastapi import APIRouter
from app.views.cu11_atender_reservas_sucursal.atender_reserva_views import (
    router as cu11_router,
)
from app.views.cu10_gestionar_reservas_prendas.reserva_views import (
    router as cu10_router,
)

# Creamos un router compuesto unificado que incluye CU11 (rutas fijas /admin/...) y luego CU10
router = APIRouter()
router.include_router(cu11_router)
router.include_router(cu10_router)

__all__ = ["router"]
