# ==============================================================================
# CU19 - GESTIONAR NOTIFICACIONES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu19_gestionar_notificaciones/notificacion_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.cu19_gestionar_notificaciones.notificacion_model import NotificacionModel
from app.models.cu10_gestionar_reservas_prendas.reserva_model import ReservaModel
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import InventarioModel
from app.models.cu5_gestionar_productos.producto_model import VarianteProductoModel, ProductoModel
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.models.cu3_gestionar_clientes.cliente_model import ClienteModel


class NotificacionController:

    @staticmethod
    def _verificar_alertas_automaticas(db: Session, current_user: UsuarioModel):
        """Genera notificaciones proactivas según eventos del negocio (expiración de reservas, stock bajo)"""
        ahora = datetime.utcnow()

        # 1. Alertas de reservas próximas a vencer (ventana < 6 horas antes de 48h)
        cliente = db.query(ClienteModel).filter(ClienteModel.usuarioid == current_user.id).first()
        if cliente:
            reservas_pendientes = db.query(ReservaModel).filter(
                ReservaModel.clienteid == cliente.id,
                ReservaModel.estado == "PENDIENTE"
            ).all()

            for res in reservas_pendientes:
                fecha_res = res.fechareserva or ahora
                fecha_limite = fecha_res + timedelta(hours=48)
                diff_horas = (fecha_limite - ahora).total_seconds() / 3600.0

                if 0 < diff_horas <= 6.0:
                    ya_existe = db.query(NotificacionModel).filter(
                        NotificacionModel.usuario_id == current_user.id,
                        NotificacionModel.tipo == "RESERVA_EXPIRANDO",
                        NotificacionModel.mensaje.ilike(f"%{res.codigoreserva}%")
                    ).first()

                    if not ya_existe:
                        horas_display = max(1, round(diff_horas))
                        notif = NotificacionModel(
                            usuario_id=current_user.id,
                            titulo=f"⏱️ Reserva {res.codigoreserva} por expirar",
                            mensaje=f"Te quedan menos de {horas_display} horas para recoger tu reserva de poleras en sucursal antes de su cancelación automática.",
                            tipo="RESERVA_EXPIRANDO",
                            enlace="/mis-reservas",
                            fecha_creacion=ahora
                        )
                        db.add(notif)

        # 2. Alertas de inventario crítico (solo para administradores)
        rol_nombre = getattr(current_user.rol, 'nombre', '').upper() if current_user.rol else ''
        if "ADMIN" in rol_nombre:
            items_criticos = db.query(InventarioModel).filter(
                InventarioModel.stockfisico <= InventarioModel.stockminimo
            ).limit(3).all()

            for item in items_criticos:
                ya_existe_stock = db.query(NotificacionModel).filter(
                    NotificacionModel.usuario_id == current_user.id,
                    NotificacionModel.tipo == "STOCK_CRITICO",
                    NotificacionModel.mensaje.ilike(f"%variante #{item.varianteid}%")
                ).first()

                if not ya_existe_stock:
                    notif = NotificacionModel(
                        usuario_id=current_user.id,
                        titulo="⚠️ Alerta de Inventario Crítico",
                        mensaje=f"La variante #{item.varianteid} tiene stock de {item.stockfisico} unidades (mínimo: {item.stockminimo}). Requiere reabastecimiento.",
                        tipo="STOCK_CRITICO",
                        enlace="/admin/inventario",
                        fecha_creacion=ahora
                    )
                    db.add(notif)

        db.commit()

    @staticmethod
    def listar_notificaciones(db: Session, current_user: UsuarioModel) -> List[Dict[str, Any]]:
        """CU19: Retorna la lista de notificaciones activas para el usuario conectado"""
        NotificacionController._verificar_alertas_automaticas(db, current_user)

        notificaciones = db.query(NotificacionModel).filter(
            (NotificacionModel.usuario_id == current_user.id) |
            (NotificacionModel.usuario_id.is_(None))
        ).order_by(NotificacionModel.id.desc()).limit(20).all()

        return [
            {
                "id": n.id,
                "titulo": n.titulo,
                "mensaje": n.mensaje,
                "tipo": n.tipo,
                "leido": n.leido,
                "enlace": n.enlace,
                "fecha": n.fecha_creacion.strftime("%d/%m/%Y %H:%M") if n.fecha_creacion else ""
            }
            for n in notificaciones
        ]

    @staticmethod
    def contar_no_leidas(db: Session, current_user: UsuarioModel) -> int:
        """CU19: Retorna la cantidad de notificaciones pendientes de lectura"""
        return db.query(NotificacionModel).filter(
            (NotificacionModel.usuario_id == current_user.id) |
            (NotificacionModel.usuario_id.is_(None)),
            NotificacionModel.leido == False
        ).count()

    @staticmethod
    def marcar_como_leida(db: Session, current_user: UsuarioModel, notificacion_id: int) -> bool:
        """CU19: Marca una notificación específica como leída"""
        notif = db.query(NotificacionModel).filter(
            NotificacionModel.id == notificacion_id,
            (NotificacionModel.usuario_id == current_user.id) | (NotificacionModel.usuario_id.is_(None))
        ).first()

        if notif:
            notif.leido = True
            db.commit()
            return True
        return False

    @staticmethod
    def marcar_todas_leidas(db: Session, current_user: UsuarioModel) -> bool:
        """CU19: Marca todas las notificaciones pendientes como leídas"""
        db.query(NotificacionModel).filter(
            (NotificacionModel.usuario_id == current_user.id) | (NotificacionModel.usuario_id.is_(None)),
            NotificacionModel.leido == False
        ).update({"leido": True}, synchronize_session=False)

        db.commit()
        return True
