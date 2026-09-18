# ==============================================================================
# CU17 - CONSULTAR HISTORIAL DE COMPRAS Y RESERVAS -> CAPA CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu17_consultar_historial_compras_reservas/historial_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import io
import base64

from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    VentaModel, DetalleVentaModel, PagoModel, MetodoPagoModel
)
from app.models.cu10_gestionar_reservas_prendas.reserva_model import (
    ReservaModel, ReservaDetalleModel
)
from app.models.cu5_gestionar_productos.producto_model import (
    ProductoModel, VarianteProductoModel
)
from app.models.cu4_gestionar_sucursales.sucursal_model import SucursalModel
from app.models.cu3_gestionar_clientes.cliente_model import ClienteModel
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel


class HistorialController:

    @staticmethod
    def _generar_qr_base64(contenido: str) -> str:
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=6, border=2)
            qr.add_data(contenido)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered)
            return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
        except Exception:
            return ""

    @staticmethod
    def _calcular_tracking(venta: VentaModel) -> List[Dict[str, Any]]:
        """Genera el timeline de seguimiento logístico para la venta"""
        estado = (venta.estado or "Pendiente").lower()
        fecha_base = venta.fecha or datetime.utcnow()

        paso1 = {"paso": 1, "titulo": "Pedido Registrado", "fecha": fecha_base.strftime("%d/%m/%Y %H:%M"), "completado": True}
        paso2 = {"paso": 2, "titulo": "Pago Confirmado", "fecha": (fecha_base + timedelta(minutes=5)).strftime("%d/%m/%Y %H:%M"), "completado": False}
        paso3 = {"paso": 3, "titulo": "En Preparación en Tienda", "fecha": (fecha_base + timedelta(hours=2)).strftime("%d/%m/%Y %H:%M"), "completado": False}
        paso4 = {"paso": 4, "titulo": "En Ruta de Entrega / Retiro", "fecha": (fecha_base + timedelta(hours=4)).strftime("%d/%m/%Y %H:%M"), "completado": False}
        paso5 = {"paso": 5, "titulo": "Completado y Entregado", "fecha": (fecha_base + timedelta(hours=6)).strftime("%d/%m/%Y %H:%M"), "completado": False}

        if estado in ["completada", "pagado", "aprobado", "entregado"]:
            paso2["completado"] = True
            paso3["completado"] = True
            paso4["completado"] = True
            paso5["completado"] = True
        elif estado in ["en_proceso", "preparando"]:
            paso2["completado"] = True
            paso3["completado"] = True
        elif estado in ["pendiente"]:
            paso2["completado"] = False

        return [paso1, paso2, paso3, paso4, paso5]

    @staticmethod
    def obtener_resumen_cliente(db: Session, current_user: UsuarioModel) -> Dict[str, Any]:
        """CU17: Retorna indicadores clave del cliente para su panel de compras y reservas"""
        cliente = db.query(ClienteModel).filter(ClienteModel.usuarioid == current_user.id).first()
        cliente_id = cliente.id if cliente else None

        # Compras
        condiciones_ventas = [VentaModel.usuarioid == current_user.id]
        if cliente_id:
            condiciones_ventas.append(VentaModel.clienteid == cliente_id)
        ventas_query = db.query(VentaModel).filter(or_(*condiciones_ventas))
        total_compras = ventas_query.count()
        total_gastado = sum([float(v.total or 0) for v in ventas_query.all()])

        # Reservas
        if cliente_id:
            reservas_query = db.query(ReservaModel).filter(ReservaModel.clienteid == cliente_id)
            total_reservas = reservas_query.count()
            reservas_activas = reservas_query.filter(ReservaModel.estado == "PENDIENTE").count()
        else:
            total_reservas = 0
            reservas_activas = 0

        return {
            "cliente_nombre": f"{current_user.nombre} {current_user.apellido or ''}".strip(),
            "total_pedidos": total_compras,
            "total_invertido_bs": round(total_gastado, 2),
            "total_reservas": total_reservas,
            "reservas_activas": reservas_activas
        }

    @staticmethod
    def listar_compras_cliente(db: Session, current_user: UsuarioModel) -> List[Dict[str, Any]]:
        """CU17: Retorna el historial completo de compras con detalles, items y estado de entrega"""
        cliente = db.query(ClienteModel).filter(ClienteModel.usuarioid == current_user.id).first()
        cliente_id = cliente.id if cliente else None

        condiciones_ventas = [VentaModel.usuarioid == current_user.id]
        if cliente_id:
            condiciones_ventas.append(VentaModel.clienteid == cliente_id)
        ventas = db.query(VentaModel).filter(or_(*condiciones_ventas)).order_by(VentaModel.id.desc()).all()

        resultado = []
        for v in ventas:
            # Obtener sucursal
            suc = db.query(SucursalModel).filter(SucursalModel.id == v.sucursalid).first()
            sucursal_nombre = suc.nombre if suc else "Sucursal Central"

            # Obtener pago y método
            pago = db.query(PagoModel).filter(PagoModel.ventaid == v.id).first()
            metodo_nombre = "Digital"
            if pago:
                mp = db.query(MetodoPagoModel).filter(MetodoPagoModel.id == pago.metodoid).first()
                if mp:
                    metodo_nombre = mp.nombre

            # Obtener items
            detalles = db.query(DetalleVentaModel).filter(DetalleVentaModel.ventaid == v.id).all()
            items = []
            for d in detalles:
                variante = db.query(VarianteProductoModel).filter(VarianteProductoModel.id == d.varianteid).first()
                producto_nombre = "Prenda Clásica"
                imagen_url = None
                if variante:
                    prod = db.query(ProductoModel).filter(ProductoModel.id == variante.productoid).first()
                    if prod:
                        producto_nombre = prod.nombre
                        imagen_url = getattr(prod, 'imagenprincipal', None) or getattr(prod, 'imagen_url', None)

                items.append({
                    "id": d.varianteid,
                    "producto": producto_nombre,
                    "cantidad": d.cantidad,
                    "precio_unitario": float(d.preciounitario or 0),
                    "subtotal": float(d.subtotal or 0),
                    "imagen_url": imagen_url
                })

            resultado.append({
                "id": v.id,
                "codigo_venta": v.codigoventa,
                "tipo_venta": v.tipoventa,
                "estado": v.estado,
                "total": float(v.total or 0),
                "fecha": v.fecha.strftime("%d/%m/%Y %H:%M") if v.fecha else "",
                "sucursal": sucursal_nombre,
                "metodo_pago": metodo_nombre,
                "tracking": HistorialController._calcular_tracking(v),
                "items_count": len(items),
                "items": items,
                "comprobante_url": f"/api/v1/pagos/{v.id}/comprobante-html"
            })

        return resultado

    @staticmethod
    def listar_reservas_cliente(db: Session, current_user: UsuarioModel) -> List[Dict[str, Any]]:
        """CU17: Retorna el historial de reservas de prendas con QR para retiro en tienda y tiempo restante"""
        cliente = db.query(ClienteModel).filter(ClienteModel.usuarioid == current_user.id).first()
        if not cliente:
            return []

        reservas = db.query(ReservaModel).filter(ReservaModel.clienteid == cliente.id).order_by(ReservaModel.id.desc()).all()
        resultado = []
        ahora = datetime.utcnow()

        for r in reservas:
            suc = db.query(SucursalModel).filter(SucursalModel.id == r.sucursalid).first()
            sucursal_nombre = suc.nombre if suc else "Sucursal Central"
            sucursal_direccion = suc.direccion if suc else "Av. Principal #123"

            # Horas restantes antes de expiración (ventana 48h desde fechareserva)
            fecha_res = r.fechareserva or ahora
            fecha_limite = fecha_res + timedelta(hours=48)
            diff = fecha_limite - ahora
            horas_restantes = max(0.0, round(diff.total_seconds() / 3600, 1))

            # QR para mostrar en mostrador al retirar
            qr_base64 = HistorialController._generar_qr_base64(
                f"RESERVA:{r.codigoreserva}|CLIENTE:{current_user.email}|SUCURSAL:{sucursal_nombre}"
            )

            # Items y total estimado
            detalles = db.query(ReservaDetalleModel).filter(ReservaDetalleModel.reservaid == r.id).all()
            items = []
            total_estimado = 0.0
            for d in detalles:
                variante = db.query(VarianteProductoModel).filter(VarianteProductoModel.id == d.varianteid).first()
                producto_nombre = "Prenda Seleccionada"
                imagen_url = None
                precio_unit = 0.0
                if variante:
                    precio_unit = float(getattr(variante, 'precioventa', 0) or 0)
                    prod = db.query(ProductoModel).filter(ProductoModel.id == variante.productoid).first()
                    if prod:
                        producto_nombre = prod.nombre
                        if precio_unit <= 0:
                            precio_unit = float(prod.preciobase or 0)
                        imagen_url = getattr(prod, 'imagenprincipal', None) or getattr(prod, 'imagen_url', None)

                subtotal_item = round(precio_unit * d.cantidad, 2)
                total_estimado += subtotal_item
                items.append({
                    "id": d.varianteid,
                    "producto": producto_nombre,
                    "cantidad": d.cantidad,
                    "precio_unitario": precio_unit,
                    "subtotal": subtotal_item,
                    "imagen_url": imagen_url
                })

            resultado.append({
                "id": r.id,
                "codigo_reserva": r.codigoreserva,
                "estado": r.estado,
                "total_estimado": round(total_estimado, 2),
                "fecha_reserva": fecha_res.strftime("%d/%m/%Y %H:%M"),
                "fecha_limite": fecha_limite.strftime("%d/%m/%Y %H:%M"),
                "horas_restantes": horas_restantes,
                "sucursal_nombre": sucursal_nombre,
                "sucursal_direccion": sucursal_direccion,
                "qr_retiro": qr_base64,
                "items": items
            })

        return resultado
