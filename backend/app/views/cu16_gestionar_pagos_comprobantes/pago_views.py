# ==============================================================================
# CU16 - GESTIONAR PAGOS Y COMPROBANTES -> CAPA VISTA / RUTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu16_gestionar_pagos_comprobantes/pago_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.models import UsuarioModel
from app.controllers.cu16_gestionar_pagos_comprobantes.pago_controller import PagoController

router = APIRouter(prefix="/pagos", tags=["CU16 - Gestionar Pagos y Comprobantes (Web y Móvil)"])


class IniciarPagoSchema(BaseModel):
    venta_id: int
    metodo_id: int
    return_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CapturarPayPalSchema(BaseModel):
    venta_id: int
    token: Optional[str] = None


@router.get("/metodos", summary="Listar métodos de pago disponibles (PayPal, QR, Efectivo)")
def listar_metodos(db: Session = Depends(get_db)):
    """CU16: Retorna los métodos de pago activos configurados en el sistema."""
    return PagoController.listar_metodos_pago(db=db)


@router.post("/iniciar", summary="Iniciar transacción de pago multimétodo")
def iniciar_pago(
    data: IniciarPagoSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """
    CU16:
    - PayPal: Genera URL oficial de checkout para redirigir al login y pago con tarjeta.
    - QR: Genera imagen Base64 del código QR oficial con temporizador de 15 minutos.
    - Efectivo: Registra orden para pago y retiro en caja de la sucursal.
    """
    return PagoController.iniciar_pago(
        db=db,
        current_user=current_user,
        venta_id=data.venta_id,
        metodo_id=data.metodo_id,
        return_url=data.return_url,
        cancel_url=data.cancel_url,
    )


@router.post("/paypal/capturar", summary="Confirmar y capturar pago devuelto por PayPal")
def capturar_paypal(
    data: CapturarPayPalSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU16: Callback cuando el usuario vuelve exitosamente de PayPal."""
    return PagoController.capturar_pago_paypal(
        db=db,
        current_user=current_user,
        venta_id=data.venta_id,
        token_paypal=data.token,
    )


@router.get("/{venta_id}/comprobante", summary="Obtener comprobante oficial con código QR fiscal")
def obtener_comprobante(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """CU16: Retorna todos los datos de la factura/recibo oficial con código QR en Base64."""
    return PagoController.obtener_comprobante_oficial(db=db, venta_id=venta_id)


@router.get("/{venta_id}/comprobante-html", response_class=HTMLResponse, summary="Ver comprobante listo para imprimir o descargar en PDF")
def ver_comprobante_html(
    venta_id: int,
    db: Session = Depends(get_db)
):
    """CU16: Renderiza el recibo/factura en HTML responsive imprimible con QR y diseño formal."""
    datos = PagoController.obtener_comprobante_oficial(db=db, venta_id=venta_id)
    empresa = datos["empresa"]
    comp = datos["comprobante"]
    cli = datos["cliente"]
    tot = datos["totales"]

    filas_items = ""
    for item in datos["items"]:
        filas_items += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">
                <strong>{item['producto']}</strong><br>
                <small style="color: #64748b;">{item['variante']}</small>
            </td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: center;">{item['cantidad']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">{item['precio_unitario']:.2f} Bs.</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 600;">{item['subtotal']:.2f} Bs.</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Recibo Oficial - {comp['nro_recibo']}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; margin: 0; padding: 20px; color: #1e293b; }}
            .ticket-card {{ max-width: 650px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }}
            .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 20px; }}
            .title {{ font-size: 22px; font-weight: 800; color: #0f172a; margin: 0 0 5px 0; }}
            .badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; background: #dcfce7; color: #166534; }}
            .grid-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; font-size: 13px; line-height: 1.6; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 14px; }}
            th {{ background: #f1f5f9; padding: 10px; text-align: left; font-size: 12px; text-transform: uppercase; color: #475569; }}
            .totales {{ display: flex; justify-content: space-between; align-items: center; border-top: 2px dashed #cbd5e1; padding-top: 20px; }}
            .btn-print {{ display: block; width: 100%; max-width: 220px; margin: 25px auto 0 auto; padding: 12px 20px; background: #0f172a; color: #ffffff; text-align: center; border-radius: 8px; text-decoration: none; font-weight: 700; cursor: pointer; border: none; }}
            @media print {{
                body {{ background: #ffffff; padding: 0; }}
                .ticket-card {{ box-shadow: none; border: none; padding: 0; }}
                .btn-print {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="ticket-card">
            <div class="header">
                <div>
                    <h1 class="title">{empresa['nombre']}</h1>
                    <div style="font-size: 13px; color: #64748b;">NIT: {empresa['nit']}</div>
                    <div style="font-size: 13px; color: #64748b;">{empresa['sucursal']} - {empresa['ciudad']}</div>
                    <div style="font-size: 13px; color: #64748b;">{empresa['direccion']}</div>
                </div>
                <div style="text-align: right;">
                    <div class="badge">ESTADO: {comp['estado'].upper()}</div>
                    <h3 style="margin: 8px 0 0 0; color: #0f172a; font-size: 16px;">{comp['nro_recibo']}</h3>
                    <small style="color: #64748b;">{comp['fecha']}</small>
                </div>
            </div>

            <div class="grid-info">
                <div>
                    <strong>DATOS DEL CLIENTE:</strong><br>
                    Nombre: {cli['nombre']}<br>
                    Email: {cli['email']}<br>
                    Teléfono: {cli['telefono']}
                </div>
                <div>
                    <strong>DETALLE DE TRANSACCIÓN:</strong><br>
                    Método de Pago: <strong>{comp['metodo_pago']}</strong><br>
                    Referencia: <small style="font-family: monospace;">{comp['referencia_pago']}</small><br>
                    Autorización: <small style="font-family: monospace;">{comp['codigo_autorizacion']}</small>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Descripción de Prenda</th>
                        <th style="text-align: center;">Cant.</th>
                        <th style="text-align: right;">P. Unit</th>
                        <th style="text-align: right;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_items}
                </tbody>
            </table>

            <div class="totales">
                <div>
                    <img src="{datos['qr_autenticidad']}" alt="QR Fiscal" style="width: 110px; height: 110px; border-radius: 6px; border: 1px solid #cbd5e1;">
                    <div style="font-size: 10px; color: #64748b; margin-top: 4px; text-align: center;">Escanear para verificar</div>
                </div>
                <div style="text-align: right; min-width: 200px;">
                    <div style="margin-bottom: 6px; color: #64748b;">Subtotal: <strong>{tot['subtotal']:.2f} Bs.</strong></div>
                    <div style="margin-bottom: 6px; color: #64748b;">IVA incluido (13%): <strong>{tot['iva_13']:.2f} Bs.</strong></div>
                    <div style="font-size: 20px; font-weight: 800; color: #0f172a; border-top: 2px solid #e2e8f0; padding-top: 8px;">
                        TOTAL: {tot['total']:.2f} Bs.
                    </div>
                </div>
            </div>

            <button class="btn-print" onclick="window.print()">🖨️ Imprimir / Guardar PDF</button>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
