# ==============================================================================
# CU08 - CONSULTAR CATÁLOGO Y DISPONIBILIDAD -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu8_consultar_catalogo_disponibilidad/catalogo_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, Header, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.inventario_schema import (
    ProductoCatalogoItem, DisponibilidadProductoResponse, ActualizarStockRequest
)
from app.controllers.cu8_consultar_catalogo_disponibilidad.catalogo_controller import (
    CatalogoController
)

router = APIRouter(prefix="/inventario", tags=["CU08 - Catálogo y Disponibilidad"])


@router.get("/catalogo", response_model=List[ProductoCatalogoItem], summary="Consultar catálogo con stock en tiempo real")
def consultar_catalogo(
    sucursal_id: Optional[int] = Query(None, description="Filtrar stock por ID de sucursal específica"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    genero: Optional[str] = Query(None, description="Filtrar por género"),
    search: Optional[str] = Query(None, description="Buscar por nombre, marca o descripción"),
    solo_disponibles: bool = Query(False, description="Mostrar únicamente productos con stock > 0"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    CU08: Consulta el catálogo de productos con stock en tiempo real por sucursal física.
    Soporta multitenant SaaS vía encabezado X-Tenant-ID.
    """
    tenant_id = x_tenant_id or 1
    return CatalogoController.consultar_catalogo(
        db=db,
        tenant_id=tenant_id,
        sucursal_id=sucursal_id,
        categoria_id=categoria_id,
        genero=genero,
        search=search,
        solo_disponibles=solo_disponibles,
        skip=skip,
        limit=limit
    )


@router.get("/producto/{id}/disponibilidad", response_model=DisponibilidadProductoResponse, summary="Disponibilidad multitienda por producto")
def consultar_disponibilidad_producto(
    id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """
    CU08: Consulta la disponibilidad detallada de un producto en todas las sucursales físicas del tenant.
    """
    tenant_id = x_tenant_id or 1
    return CatalogoController.obtener_disponibilidad_producto(
        db=db,
        producto_id=id,
        tenant_id=tenant_id
    )


@router.put("/stock", status_code=status.HTTP_200_OK, summary="Actualizar existencias físicas en sucursal")
def actualizar_stock_sucursal(
    datos: ActualizarStockRequest,
    request: Request,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """
    Actualiza las existencias físicas de una variante en una tienda física con registro en Bitácora (CU26).
    """
    tenant_id = x_tenant_id or 1
    ip_origen = request.client.host if request.client else "127.0.0.1"
    return CatalogoController.actualizar_stock_sucursal(
        db=db,
        datos=datos,
        tenant_id=tenant_id,
        usuario_id=1,
        ip=ip_origen
    )


@router.get("/sucursales", summary="Listar tiendas físicas activas")
def listar_sucursales_activas(
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
):
    """
    Lista las tiendas físicas activas del tenant para los selectores de sucursal.
    """
    tenant_id = x_tenant_id or 1
    return CatalogoController.listar_sucursales_activas(
        db=db,
        tenant_id=tenant_id
    )


@router.api_route("/seed-variantes-stock", methods=["GET", "POST"], tags=["Administración y Mantenimiento"])
def trigger_seed_variantes(db: Session = Depends(get_db)):
    """Ejecuta el seeder para poblar o actualizar las variantes de colores y stock diferenciado por sucursal"""
    from app.core.seeder_variantes import aplicar_seeder_variantes_y_stock
    resultado = aplicar_seeder_variantes_y_stock(db)
    from app.main import sync_db_sequences
    sync_db_sequences()
    return resultado
