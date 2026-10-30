# ==============================================================================
# CU08 - CONSULTAR CATÁLOGO Y DISPONIBILIDAD -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Arquitectura: Multi-Tenant SaaS con Auditoría Bitácora (CU26)
# Ubicación: backend/app/controllers/cu8_consultar_catalogo_disponibilidad/catalogo_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.services.cu8_consultar_catalogo_disponibilidad.catalogo_service import CatalogoService
from app.schemas.inventario_schema import (
    ProductoCatalogoItem, DisponibilidadProductoResponse, ActualizarStockRequest
)


class CatalogoController:
    """
    Controlador MVC para la consulta del catálogo y disponibilidad de prendas en tiendas físicas.
    Orquesta la lógica de negocio y asegura la compatibilidad multitenant y trazabilidad.
    """

    @staticmethod
    def consultar_catalogo(
        db: Session,
        tenant_id: int = 1,
        sucursal_id: Optional[int] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        search: Optional[str] = None,
        solo_disponibles: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductoCatalogoItem]:
        """Consulta el catálogo de prendas filtrado por tenant y sucursal"""
        return CatalogoService.consultar_catalogo(
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

    @staticmethod
    def obtener_disponibilidad_producto(
        db: Session,
        producto_id: int,
        tenant_id: int = 1
    ) -> DisponibilidadProductoResponse:
        """Obtiene la disponibilidad de un producto en todas las sucursales del tenant"""
        return CatalogoService.obtener_disponibilidad_producto(
            db=db,
            producto_id=producto_id,
            tenant_id=tenant_id
        )

    @staticmethod
    def listar_sucursales_activas(
        db: Session,
        tenant_id: int = 1
    ) -> List[Dict[str, Any]]:
        """Lista las tiendas físicas activas para los selectores de sucursal"""
        return CatalogoService.listar_sucursales_activas(
            db=db,
            tenant_id=tenant_id
        )

    @staticmethod
    def actualizar_stock_sucursal(
        db: Session,
        datos: ActualizarStockRequest,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None,
        ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """Actualiza el stock físico de una variante en una sucursal específica con auditoría"""
        return CatalogoService.actualizar_stock_sucursal(
            db=db,
            datos=datos,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            ip=ip
        )

    # Alias de compatibilidad hacia atrás
    listar_catalogo = consultar_catalogo
    actualizar_stock = actualizar_stock_sucursal


# Alias canónico
InventarioController = CatalogoController
