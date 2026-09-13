# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER - FACHADA RETROCOMPATIBLE)
# Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
# Ubicación: backend/app/routes/inventario_routes.py
# ==============================================================================

from app.views.cu8_consultar_catalogo_disponibilidad.catalogo_views import router

__all__ = ["router"]
