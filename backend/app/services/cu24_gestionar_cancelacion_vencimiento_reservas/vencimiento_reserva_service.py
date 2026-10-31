# ==============================================================================
# CU24 - GESTIONAR CANCELACIÓN Y VENCIMIENTO DE RESERVAS -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu24_gestionar_cancelacion_vencimiento_reservas/vencimiento_reserva_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.cu10_gestionar_reservas_prendas.reserva_model import ReservaModel, ReservaDetalleModel
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import InventarioModel


class VencimientoReservaService:
    """
    Servicio para auditar vencimientos (48 horas), cancelar reservas no recogidas
    y liberar automáticamente el stock reservado de poleras para devolverlo a disponibilidad.
    """

    @staticmethod
    def cancelar_reservas_vencidas(db: Session, tenant_id: int) -> Dict[str, Any]:
        ahora = datetime.utcnow()
        limite_tiempo = ahora - timedelta(hours=48)

        # Buscar reservas pendientes cuyo plazo ha expirado
        reservas_expiradas = db.query(ReservaModel).filter(
            ReservaModel.tenant_id == tenant_id,
            ReservaModel.estado == "PENDIENTE",
            ReservaModel.fechareserva <= limite_tiempo
        ).all()

        total_canceladas = 0
        prendas_liberadas = 0

        for res in reservas_expiradas:
            res.estado = "VENCIDA"
            total_canceladas += 1

            # Devolver stock reservado
            detalles = db.query(ReservaDetalleModel).filter(ReservaDetalleModel.reservaid == res.id).all()
            for det in detalles:
                # Actualizar inventario
                inv = db.query(InventarioModel).filter(
                    InventarioModel.varianteid == det.varianteid,
                    InventarioModel.sucursalid == res.sucursalid,
                    InventarioModel.tenant_id == tenant_id
                ).first()
                if inv:
                    inv.stockreservado = max(0, (inv.stockreservado or 0) - det.cantidad)
                    prendas_liberadas += det.cantidad

        db.commit()
        return {
            "reservas_vencidas_canceladas": total_canceladas,
            "prendas_liberadas_al_stock": prendas_liberadas,
            "fecha_ejecucion": ahora.isoformat()
        }

    @staticmethod
    def cancelar_reserva_manual(db: Session, reserva_id: int, tenant_id: int, motivo: str) -> Optional[ReservaModel]:
        res = db.query(ReservaModel).filter(
            ReservaModel.id == reserva_id,
            ReservaModel.tenant_id == tenant_id
        ).first()
        if not res or res.estado != "PENDIENTE":
            return None

        res.estado = "CANCELADA"
        # Devolver stock
        detalles = db.query(ReservaDetalleModel).filter(ReservaDetalleModel.reservaid == res.id).all()
        for det in detalles:
            inv = db.query(InventarioModel).filter(
                InventarioModel.varianteid == det.varianteid,
                InventarioModel.sucursalid == res.sucursalid,
                InventarioModel.tenant_id == tenant_id
            ).first()
            if inv:
                inv.stockreservado = max(0, (inv.stockreservado or 0) - det.cantidad)

        db.commit()
        db.refresh(res)
        return res

