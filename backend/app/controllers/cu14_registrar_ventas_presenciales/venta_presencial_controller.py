# ==============================================================================
# CU14 - REGISTRAR VENTAS PRESENCIALES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu14_registrar_ventas_presenciales/venta_presencial_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Optional

from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    MetodoPagoModel,
)
from app.models.models import UsuarioModel
from app.schemas.orden_schema import VentaPresencialCreate
from app.services.cu14_registrar_ventas_presenciales.venta_presencial_service import (
    VentaPresencialService,
)


class VentaPresencialController:
    """
    Controlador MVC para el Caso de Uso CU14: Registrar Ventas Presenciales (POS).
    Orquesta las solicitudes provenientes de las vistas API y delega la lógica de negocio
    a VentaPresencialService asegurando aislamiento SaaS y auditoría en Bitácora (CU26).
    """

    @classmethod
    def registrar_venta_presencial(
        cls,
        db: Session,
        current_user: UsuarioModel,
        data: VentaPresencialCreate,
        tenant_id: int = 1,
        ip_origen: str = "127.0.0.1",
    ) -> Dict:
        return VentaPresencialService.registrar_venta_presencial(
            db=db,
            data=data,
            usuario_id=current_user.id,
            tenant_id=tenant_id,
            ip_origen=ip_origen,
        )

    @classmethod
    def listar_todas_ventas(
        cls,
        db: Session,
        tipoventa: Optional[str] = None,
        sucursal_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        tenant_id: int = 1,
    ) -> List[Dict]:
        return VentaPresencialService.listar_todas_ventas(
            db=db,
            tipoventa=tipoventa,
            sucursal_id=sucursal_id,
            skip=skip,
            limit=limit,
            tenant_id=tenant_id,
        )

    @classmethod
    def obtener_venta_por_id(
        cls,
        db: Session,
        venta_id: int,
        tenant_id: int = 1,
    ) -> Dict:
        return VentaPresencialService.obtener_venta_por_id(
            db=db,
            venta_id=venta_id,
            tenant_id=tenant_id,
        )

    @classmethod
    def listar_metodos_pago(cls, db: Session) -> List[MetodoPagoModel]:
        return VentaPresencialService.listar_metodos_pago(db=db)


# ==============================================================================
# ALIASES DE COMPATIBILIDAD (CONVENCIONES EN ESPAÑOL Y DIAGRAMAS)
# ==============================================================================
VentaPresencialController.registrar = VentaPresencialController.registrar_venta_presencial
VentaPresencialController.listar = VentaPresencialController.listar_todas_ventas
VentaPresencialController.obtener = VentaPresencialController.obtener_venta_por_id
VentaPresencialController.metodos_pago = VentaPresencialController.listar_metodos_pago
