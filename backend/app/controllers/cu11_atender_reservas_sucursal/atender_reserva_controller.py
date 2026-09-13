# ==============================================================================
# CU11 - ATENDER RESERVAS EN SUCURSAL -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu11_atender_reservas_sucursal/atender_reserva_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.models import (
    ReservaModel,
    InventarioSucursalModel,
)
from app.schemas.reserva_schema import (
    ReservaResponse,
    AtenderReservaRequest,
)
from app.controllers.cu10_gestionar_reservas_prendas.reserva_controller import (
    formatear_reserva,
)


class AtenderReservaController:

    @staticmethod
    def listar_reservas_admin(
        db: Session,
        sucursal_id: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[ReservaResponse]:
        """
        CU11: Listado de reservas para el panel administrativo / caja de sucursal.
        Permite filtrar por sucursal física y por estado de reserva.
        """
        query = db.query(ReservaModel)
        if sucursal_id:
            query = query.filter(ReservaModel.sucursalid == sucursal_id)
        if estado and estado.upper() != "TODAS":
            query = query.filter(ReservaModel.estado == estado.upper())

        reservas = query.order_by(ReservaModel.fechareserva.desc()).all()
        return [formatear_reserva(r) for r in reservas]

    @staticmethod
    def buscar_reserva_codigo(db: Session, codigo: str) -> ReservaResponse:
        """
        CU11: Búsqueda rápida por código de reserva en el punto de atención de sucursal.
        """
        limpio = codigo.strip().upper()
        reserva = db.query(ReservaModel).filter(ReservaModel.codigoreserva == limpio).first()
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró ninguna reserva con el código '{limpio}'. Verifique que el código esté bien escrito.",
            )
        return formatear_reserva(reserva)

    @staticmethod
    def atender_reserva_sucursal(
        db: Session,
        reserva_id: int,
        datos: AtenderReservaRequest,
        usuario_staff_id: Optional[int] = None,
    ) -> ReservaResponse:
        """
        CU11: Atender reserva en sucursal física.
        - ENTREGAR: Cambia estado a ENTREGADA, libera 'stockreservado' y descuenta definitivamente 'cantidad' (stock físico).
        - CANCELAR: Cambia estado a CANCELADA y libera 'stockreservado' (el stock físico queda disponible en tienda).
        """
        reserva = db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reserva con ID {reserva_id} no encontrada.",
            )

        if reserva.estado in ["ENTREGADA", "CANCELADA", "EXPIRADA"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La reserva ya se encuentra en estado '{reserva.estado}' y no puede modificarse nuevamente.",
            )

        accion = datos.accion.strip().upper()

        if accion == "ENTREGAR":
            # 1. Descontar stock físico y liberar stock reservado
            for d in reserva.detalles:
                inv = (
                    db.query(InventarioSucursalModel)
                    .filter(
                        InventarioSucursalModel.varianteid == d.varianteid,
                        InventarioSucursalModel.sucursalid == reserva.sucursalid,
                    )
                    .first()
                )
                if inv:
                    inv.stockreservado = max(0, inv.stockreservado - d.cantidad)
                    inv.cantidad = max(0, inv.cantidad - d.cantidad)

            reserva.estado = "ENTREGADA"
            nota = "[Entregada y Cobrada en Tienda]"
            if datos.observaciones:
                nota += f" Nota: {datos.observaciones}"
            reserva.observaciones = f"{reserva.observaciones or ''} {nota}".strip()

        elif accion == "CANCELAR":
            # 2. Cancelar: solo liberar el stock reservado para devolverlo a disponible
            for d in reserva.detalles:
                inv = (
                    db.query(InventarioSucursalModel)
                    .filter(
                        InventarioSucursalModel.varianteid == d.varianteid,
                        InventarioSucursalModel.sucursalid == reserva.sucursalid,
                    )
                    .first()
                )
                if inv:
                    inv.stockreservado = max(0, inv.stockreservado - d.cantidad)

            reserva.estado = "CANCELADA"
            nota = "[Cancelada por inasistencia o decisión del cliente en tienda]"
            if datos.observaciones:
                nota += f" Motivo: {datos.observaciones}"
            reserva.observaciones = f"{reserva.observaciones or ''} {nota}".strip()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Acción '{datos.accion}' no permitida. Use 'ENTREGAR' o 'CANCELAR'.",
            )

        db.commit()
        db.refresh(reserva)
        return formatear_reserva(reserva)
