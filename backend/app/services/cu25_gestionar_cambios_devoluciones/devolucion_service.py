# ==============================================================================
# CU25 - GESTIONAR CAMBIOS Y DEVOLUCIONES DE PRENDAS -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu25_gestionar_cambios_devoluciones/devolucion_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.models.cu25_gestionar_cambios_devoluciones.devolucion_model import Devolucion, DetalleDevolucion
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import InventarioModel


class DevolucionService:
    """
    Servicio integral para procesar cambios de talla/prenda y devoluciones con reintegro a stock.
    """

    @staticmethod
    def solicitar_devolucion(
        db: Session,
        tenant_id: int,
        venta_id: int,
        cliente_id: Optional[int],
        usuario_id: Optional[int],
        sucursal_id: int,
        tipo_devolucion: str,
        motivo: str,
        monto_reembolso: float,
        items: List[Dict[str, Any]]
    ) -> Devolucion:
        codigo = f"DEV-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        devolucion = Devolucion(
            tenant_id=tenant_id,
            venta_id=venta_id,
            cliente_id=cliente_id,
            usuario_id=usuario_id,
            sucursal_id=sucursal_id,
            codigo_devolucion=codigo,
            tipo_devolucion=tipo_devolucion,
            motivo=motivo,
            estado="APROBADA",
            monto_reembolso=monto_reembolso,
            reingreso_inventario=True,
            fecha_solicitud=datetime.utcnow(),
            fecha_resolucion=datetime.utcnow()
        )
        db.add(devolucion)
        db.flush()

        for item in items:
            det = DetalleDevolucion(
                devolucion_id=devolucion.id,
                variante_devuelta_id=item["variante_devuelta_id"],
                variante_nueva_id=item.get("variante_nueva_id"),
                cantidad=item.get("cantidad", 1),
                precio_unitario=item.get("precio_unitario", 0.0),
                subtotal=item.get("subtotal", 0.0),
                estado_prenda=item.get("estado_prenda", "PERFECTO_ESTADO")
            )
            db.add(det)

            # Reingresar stock al inventario
            inv_devuelto = db.query(InventarioModel).filter(
                InventarioModel.varianteid == item["variante_devuelta_id"],
                InventarioModel.sucursalid == sucursal_id,
                InventarioModel.tenant_id == tenant_id
            ).first()
            if inv_devuelto:
                inv_devuelto.stockfisico = (inv_devuelto.stockfisico or 0) + item.get("cantidad", 1)

            # Si es cambio por otra variante, descontar la variante nueva
            if item.get("variante_nueva_id"):
                inv_nuevo = db.query(InventarioModel).filter(
                    InventarioModel.varianteid == item["variante_nueva_id"],
                    InventarioModel.sucursalid == sucursal_id,
                    InventarioModel.tenant_id == tenant_id
                ).first()
                if inv_nuevo:
                    inv_nuevo.stockfisico = max(0, (inv_nuevo.stockfisico or 0) - item.get("cantidad", 1))

        db.commit()
        db.refresh(devolucion)
        return devolucion

    @staticmethod
    def listar_devoluciones(db: Session, tenant_id: int, sucursal_id: Optional[int] = None) -> List[Devolucion]:
        q = db.query(Devolucion).filter(Devolucion.tenant_id == tenant_id)
        if sucursal_id:
            q = q.filter(Devolucion.sucursal_id == sucursal_id)
        return q.order_by(Devolucion.id.desc()).all()
