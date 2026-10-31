# ==============================================================================
# CU11 - ATENDER RESERVAS EN SUCURSAL -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Arquitectura: Multi-Tenant SaaS con Auditoría (CU26) y Movimientos de Inventario (CU13)
# Ubicación: backend/app/controllers/cu11_atender_reservas_sucursal/atender_reserva_controller.py
# ==============================================================================

from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.reserva_schema import (
    ReservaResponse,
    AtenderReservaRequest,
)
from app.services.cu11_atender_reservas_sucursal.atender_reserva_service import (
    AtenderReservaService,
)


class AtenderReservaController:
    """
    Controlador MVC para la atención física de reservas en sucursal.
    Orquesta llamadas a la capa de servicio, manteniendo compatibilidad de nombres.
    """

    @classmethod
    def listar_reservas_admin(
        cls,
        db: Session,
        sucursal_id: Optional[int] = None,
        estado: Optional[str] = None,
        tenant_id: int = 1,
    ) -> List[ReservaResponse]:
        """CU11: Listado de reservas para el panel administrativo / caja de sucursal"""
        return AtenderReservaService.listar_reservas_admin(
            db=db,
            sucursal_id=sucursal_id,
            estado=estado,
            tenant_id=tenant_id,
        )

    @classmethod
    def buscar_reserva_codigo(
        cls,
        db: Session,
        codigo: str,
        tenant_id: int = 1,
    ) -> ReservaResponse:
        """CU11: Búsqueda rápida por código de reserva en el punto de atención de sucursal"""
        return AtenderReservaService.buscar_reserva_codigo(
            db=db,
            codigo=codigo,
            tenant_id=tenant_id,
        )

    @classmethod
    def atender_reserva_sucursal(
        cls,
        db: Session,
        reserva_id: int,
        datos: AtenderReservaRequest,
        usuario_staff_id: Optional[int] = None,
        tenant_id: int = 1,
    ) -> ReservaResponse:
        """CU11: Atender reserva en sucursal física (ENTREGAR o CANCELAR)"""
        return AtenderReservaService.atender_reserva_sucursal(
            db=db,
            reserva_id=reserva_id,
            datos=datos,
            usuario_staff_id=usuario_staff_id,
            tenant_id=tenant_id,
        )

    # --------------------------------------------------------------------------
    # Alias en español para convención MVC uniforme
    # --------------------------------------------------------------------------
    listar_reservas_sucursal = listar_reservas_admin
    buscar_reserva_por_codigo = buscar_reserva_codigo
    atender_reserva_en_sucursal = atender_reserva_sucursal
