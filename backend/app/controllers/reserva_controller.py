# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU10 y CU11 - Gestión y Atención de Reservas de Prendas (Fachada)
# Ubicación: backend/app/controllers/reserva_controller.py
# ==============================================================================

from app.controllers.cu10_gestionar_reservas_prendas.reserva_controller import (
    ReservaController as CU10ReservaController,
    generar_codigo_reserva,
    formatear_reserva,
)
from app.controllers.cu11_atender_reservas_sucursal.atender_reserva_controller import (
    AtenderReservaController as CU11AtenderReservaController,
)


class ReservaController(CU10ReservaController):
    """
    Controlador unificado que hereda las operaciones del cliente (CU10)
    y delega las operaciones de personal de sucursal / caja (CU11).
    """

    listar_reservas_admin = staticmethod(CU11AtenderReservaController.listar_reservas_admin)
    buscar_reserva_codigo = staticmethod(CU11AtenderReservaController.buscar_reserva_codigo)
    atender_reserva_sucursal = staticmethod(CU11AtenderReservaController.atender_reserva_sucursal)


__all__ = [
    "ReservaController",
    "generar_codigo_reserva",
    "formatear_reserva",
]
