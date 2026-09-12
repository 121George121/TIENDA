# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER)
# Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
# Ubicación: backend/app/routes/inventario_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.models import SucursalModel
from app.schemas.inventario_schema import (
    ProductoCatalogoItem, DisponibilidadProductoResponse, ActualizarStockRequest
)
from app.controllers.inventario_controller import InventarioController

router = APIRouter(prefix="/inventario", tags=["CU08 - Catálogo y Disponibilidad"])

@router.get("/catalogo", response_model=List[ProductoCatalogoItem])
def consultar_catalogo(
    sucursal_id: Optional[int] = Query(None, description="Filtrar stock por ID de sucursal específica"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    genero: Optional[str] = Query(None, description="Filtrar por género"),
    search: Optional[str] = Query(None, description="Buscar por nombre, marca o descripción"),
    solo_disponibles: bool = Query(False, description="Mostrar únicamente productos con stock > 0"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """CU08: Consulta el catálogo de productos con stock en tiempo real"""
    return InventarioController.listar_catalogo(
        db=db,
        sucursal_id=sucursal_id,
        categoria_id=categoria_id,
        genero=genero,
        search=search,
        solo_disponibles=solo_disponibles,
        skip=skip,
        limit=limit
    )

@router.get("/producto/{id}/disponibilidad", response_model=DisponibilidadProductoResponse)
def consultar_disponibilidad_producto(
    id: int,
    db: Session = Depends(get_db)
):
    """CU08: Consulta la disponibilidad de un producto en todas las sucursales físicas"""
    return InventarioController.obtener_disponibilidad_producto(db=db, producto_id=id)

@router.put("/stock", status_code=status.HTTP_200_OK)
def actualizar_stock_sucursal(
    datos: ActualizarStockRequest,
    db: Session = Depends(get_db)
):
    """Actualiza las existencias de una variante en una tienda física"""
    return InventarioController.actualizar_stock(db=db, datos=datos)

@router.get("/sucursales")
def listar_sucursales_activas(db: Session = Depends(get_db)):
    """Lista las tiendas físicas activas para los selectores de sucursal"""
    sucursales = db.query(SucursalModel).filter(SucursalModel.activo == True).all()
    return [
        {
            "id": s.id,
            "nombre": s.nombre,
            "ciudad": s.ciudad,
            "direccion": s.direccion,
            "telefono": s.telefono
        }
        for s in sucursales
    ]
