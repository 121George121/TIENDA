# ==============================================================================
# CU16 - GESTIONAR PAGOS Y COMPROBANTES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu16_gestionar_pagos_comprobantes/pago_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal
from datetime import datetime
import io
import base64
import urllib.parse

from app.models.models import (
    VentaModel,
    DetalleVentaModel,
    MetodoPagoModel,
    PagoModel,
    ReciboModel,
    UsuarioModel,
    ClienteModel,
    SucursalModel,
    InventarioModel,
    MovimientoInventarioModel,
)


def generar_qr_base64(texto: str) -> str:
    """Genera una imagen QR en Base64 PNG a partir de un texto o URL."""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(texto)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1a1a2e", back_color="#ffffff")
        buffered = io.BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generando QR: {e}")
        return ""


class PagoController:

    @staticmethod
    def listar_metodos_pago(db: Session):
        """Retorna todos los métodos de pago activos configurados en el ERP."""
        metodos = db.query(MetodoPagoModel).filter(MetodoPagoModel.estado == True).all()
        resultado = []
        for m in metodos:
            icono = "credit_card"
            descripcion = "Pago seguro"
            if "paypal" in m.nombre.lower():
                icono = "account_balance_wallet"
                descripcion = "Redirección oficial a PayPal (Iniciar sesión o Tarjeta de débito/crédito)"
            elif "qr" in m.nombre.lower() or "transferencia" in m.nombre.lower():
                icono = "qr_code_2"
                descripcion = "Escanea con cualquier app bancaria nacional e internacional"
            elif "efectivo" in m.nombre.lower():
                icono = "payments"
                descripcion = "Paga en caja al momento de retirar tus prendas en sucursal"

            resultado.append({
                "id": m.id,
                "nombre": m.nombre,
                "icono": icono,
                "descripcion": descripcion,
                "activo": m.estado,
            })
        return resultado

    @staticmethod
    def iniciar_pago(db: Session, current_user: UsuarioModel, venta_id: int, metodo_id: int, return_url: str = None, cancel_url: str = None):
        """
        CU16: Inicia el proceso de pago según el método seleccionado (PayPal, QR o Efectivo).
        Conectado directamente a las tablas venta, pago y metodo_pago.
        """
        venta = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la venta con ID {venta_id}."
            )

        metodo = db.query(MetodoPagoModel).filter(MetodoPagoModel.id == metodo_id, MetodoPagoModel.estado == True).first()
        if not metodo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Método de pago con ID {metodo_id} no válido o inactivo."
            )

        ahora = datetime.utcnow()
        nombre_lower = metodo.nombre.lower()

        # -------------------------------------------------------------
        # 1. FLUJO PAYPAL (Redirección oficial a login / tarjeta)
        # -------------------------------------------------------------
        if "paypal" in nombre_lower:
            # Buscar o crear pago en estado Pendiente
            pago = db.query(PagoModel).filter(PagoModel.ventaid == venta.id).first()
            token_paypal = f"EC-{venta.id}{int(ahora.timestamp())}"
            
            if not pago:
                pago = PagoModel(
                    monto=venta.total,
                    estado="Pendiente",
                    referencia=f"PAYPAL-ORD-{token_paypal}",
                    fecha=ahora,
                    ventaid=venta.id,
                    metodoid=metodo.id
                )
                db.add(pago)
            else:
                pago.metodoid = metodo.id
                pago.referencia = f"PAYPAL-ORD-{token_paypal}"
                pago.estado = "Pendiente"
            db.commit()

            # URL oficial de PayPal Checkout (Sandbox / Live)
            # En Sandbox estándar, redirige a la interfaz real de PayPal para iniciar sesión o poner tarjeta
            monto_usd = round(float(venta.total) / 6.96, 2)  # Conversión referencial a USD si moneda base es BOB
            if monto_usd <= 0:
                monto_usd = float(venta.total)

            params = {
                "cmd": "_xclick",
                "business": "tienda.fashionstore.boutique@gmail.com",
                "item_name": f"Orden Boutique FashionStore #{venta.codigoventa}",
                "amount": f"{monto_usd:.2f}",
                "currency_code": "USD",
                "custom": str(venta.id),
                "invoice": venta.codigoventa,
                "return": return_url or f"http://localhost:4200/mis-pedidos?pago_status=exito&orden_id={venta.id}&token={token_paypal}",
                "cancel_return": cancel_url or f"http://localhost:4200/carrito?pago_status=cancelado&orden_id={venta.id}",
            }
            url_paypal_checkout = f"https://www.sandbox.paypal.com/cgi-bin/webscr?{urllib.parse.urlencode(params)}"

            return {
                "metodo": "PayPal",
                "requiere_redireccion": True,
                "url_redireccion": url_paypal_checkout,
                "token": token_paypal,
                "monto_total": float(venta.total),
                "monto_usd": monto_usd,
                "mensaje": "Redirigiendo a la pasarela oficial de PayPal para iniciar sesión o pagar con tarjeta..."
            }

        # -------------------------------------------------------------
        # 2. FLUJO QR (Generación de código QR oficial con timer)
        # -------------------------------------------------------------
        elif "qr" in nombre_lower or "transferencia" in nombre_lower:
            pago = db.query(PagoModel).filter(PagoModel.ventaid == venta.id).first()
            ref_qr = f"QR-BCP-{venta.codigoventa}"
            
            if not pago:
                pago = PagoModel(
                    monto=venta.total,
                    estado="Aprobado",  # En simulación se auto-aprueba al escanear
                    referencia=ref_qr,
                    fecha=ahora,
                    ventaid=venta.id,
                    metodoid=metodo.id
                )
                db.add(pago)
            else:
                pago.metodoid = metodo.id
                pago.referencia = ref_qr
                pago.estado = "Aprobado"

            # Marcar venta completada y emitir recibo
            venta.estado = "Completada"
            
            recibo = db.query(ReciboModel).filter(ReciboModel.id == pago.reciboid).first()
            if not recibo:
                recibo = ReciboModel(estado="Emitido", fecha=ahora)
                db.add(recibo)
                db.flush()
                pago.reciboid = recibo.id

            db.commit()

            datos_qr = (
                f"BOUTIQUE FASHIONSTORE | VENTA: {venta.codigoventa} | "
                f"MONTO: {float(venta.total):.2f} Bs. | FECHA: {ahora.strftime('%Y-%m-%d %H:%M')} | "
                f"CUENTA: 1000004928371 BCP | TITULAR: FashionStore S.R.L."
            )
            qr_base64 = generar_qr_base64(datos_qr)

            return {
                "metodo": "QR",
                "requiere_redireccion": False,
                "qr_image": qr_base64,
                "codigo_pago": ref_qr,
                "monto_total": float(venta.total),
                "cuenta_bancaria": "1000004928371 (Banco BCP - Moneda Nacional)",
                "titular": "FashionStore Boutique S.R.L. (NIT 1029384756)",
                "tiempo_expiracion_minutos": 15,
                "mensaje": "Código QR generado con éxito. Escanéalo desde tu app bancaria."
            }

        # -------------------------------------------------------------
        # 3. FLUJO EFECTIVO (Pago en sucursal / mostrador)
        # -------------------------------------------------------------
        else:
            pago = db.query(PagoModel).filter(PagoModel.ventaid == venta.id).first()
            ref_efectivo = f"EFE-{venta.codigoventa}"
            
            if not pago:
                pago = PagoModel(
                    monto=venta.total,
                    estado="Aprobado" if venta.tipoventa == "Presencial" else "Pendiente",
                    referencia=ref_efectivo,
                    fecha=ahora,
                    ventaid=venta.id,
                    metodoid=metodo.id
                )
                db.add(pago)
            else:
                pago.metodoid = metodo.id
                pago.referencia = ref_efectivo
                pago.estado = "Aprobado" if venta.tipoventa == "Presencial" else "Pendiente"

            if venta.tipoventa == "Presencial":
                venta.estado = "Completada"

            recibo = db.query(ReciboModel).filter(ReciboModel.id == pago.reciboid).first()
            if not recibo:
                recibo = ReciboModel(estado="Emitido", fecha=ahora)
                db.add(recibo)
                db.flush()
                pago.reciboid = recibo.id

            db.commit()

            return {
                "metodo": "Efectivo",
                "requiere_redireccion": False,
                "referencia": ref_efectivo,
                "monto_total": float(venta.total),
                "estado_pago": pago.estado,
                "mensaje": "Pago registrado. Presenta este comprobante en caja al retirar tus prendas."
            }

    @staticmethod
    def capturar_pago_paypal(db: Session, current_user: UsuarioModel, venta_id: int, token_paypal: str = None):
        """
        CU16: Callback cuando el usuario regresa exitosamente de la pasarela de PayPal.
        Actualiza el estado de la venta a Completada, pago Aprobado y genera Recibo.
        """
        venta = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
        if not venta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada.")

        ahora = datetime.utcnow()
        pago = db.query(PagoModel).filter(PagoModel.ventaid == venta.id).first()
        
        metodo_paypal = db.query(MetodoPagoModel).filter(MetodoPagoModel.nombre.ilike("%paypal%")).first()
        if not metodo_paypal:
            metodo_paypal = db.query(MetodoPagoModel).first()

        if not pago:
            pago = PagoModel(
                monto=venta.total,
                estado="Aprobado",
                referencia=f"PAYPAL-OK-{token_paypal or venta.codigoventa}",
                fecha=ahora,
                ventaid=venta.id,
                metodoid=metodo_paypal.id
            )
            db.add(pago)
        else:
            pago.estado = "Aprobado"
            pago.referencia = f"PAYPAL-OK-{token_paypal or pago.referencia}"
            pago.fecha = ahora

        venta.estado = "Completada"

        recibo = db.query(ReciboModel).filter(ReciboModel.id == pago.reciboid).first()
        if not recibo:
            recibo = ReciboModel(estado="Emitido", fecha=ahora)
            db.add(recibo)
            db.flush()
            pago.reciboid = recibo.id

        db.commit()
        db.refresh(venta)

        return {
            "status": "exito",
            "mensaje": "¡Pago procesado con éxito a través de PayPal!",
            "venta_id": venta.id,
            "codigo_venta": venta.codigoventa,
            "monto": float(venta.total),
            "referencia": pago.referencia
        }

    @staticmethod
    def obtener_comprobante_oficial(db: Session, venta_id: int):
        """
        CU16: Retorna los datos estructurados y enriquecidos del Comprobante / Recibo Oficial
        incluyendo código QR de autenticidad, desglose de prendas, variantes e IVA.
        """
        venta = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
        if not venta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado.")

        cliente = venta.cliente
        sucursal = venta.sucursal
        pago = db.query(PagoModel).filter(PagoModel.ventaid == venta.id).first()
        metodo_nombre = pago.metodo.nombre if pago and pago.metodo else "Pago Digital"

        items = []
        for det in venta.detalles:
            variante = det.variante
            prod_nombre = variante.producto.nombre if variante and variante.producto else "Prenda"
            color_nombre = variante.color.nombre if variante and variante.color else "Estándar"
            talla_nombre = variante.talla.nombre if variante and variante.talla else "M"
            items.append({
                "producto": prod_nombre,
                "variante": f"Talla: {talla_nombre} | Color: {color_nombre}",
                "cantidad": det.cantidad,
                "precio_unitario": float(det.preciounitario),
                "subtotal": float(det.subtotal),
            })

        # Cálculo de IVA (13% ley tributaria de retail)
        subtotal_val = float(venta.subtotal)
        iva_val = round(subtotal_val * 0.13, 2)
        total_val = float(venta.total)

        # Generar código QR de validación fiscal
        datos_fiscales = (
            f"FASHIONSTORE NIT:1029384756|RECIBO:{venta.codigoventa}|"
            f"TOTAL:{total_val:.2f}|FECHA:{venta.fecha.strftime('%Y-%m-%d %H:%M')}|"
            f"CLIENTE:{cliente.nombre if cliente else 'Cliente'}"
        )
        qr_fiscal = generar_qr_base64(datos_fiscales)

        return {
            "empresa": {
                "nombre": "BOUTIQUE FASHIONSTORE S.R.L.",
                "nit": "1029384756",
                "sucursal": sucursal.nombre if sucursal else "Sucursal Central",
                "direccion": sucursal.direccion if sucursal else "Av. San Martín #450",
                "telefono": sucursal.telefono if sucursal else "+591 70000000",
                "ciudad": sucursal.ciudad if sucursal else "Santa Cruz - Bolivia",
            },
            "comprobante": {
                "nro_recibo": venta.codigoventa,
                "tipo_venta": venta.tipoventa,
                "fecha": venta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "estado": venta.estado,
                "metodo_pago": metodo_nombre,
                "referencia_pago": pago.referencia if pago else "N/A",
                "codigo_autorizacion": f"AUT-{venta.id * 8372}-{int(venta.fecha.timestamp())}",
            },
            "cliente": {
                "nombre": f"{cliente.nombre} {cliente.apellido or ''}".strip() if cliente else "Cliente Final",
                "email": cliente.email if cliente else "N/A",
                "telefono": cliente.telefono if cliente else "N/A",
            },
            "items": items,
            "totales": {
                "subtotal": subtotal_val,
                "descuento": float(venta.descuento),
                "iva_13": iva_val,
                "total": total_val,
            },
            "qr_autenticidad": qr_fiscal,
        }
