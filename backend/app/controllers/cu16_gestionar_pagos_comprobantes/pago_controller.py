# ==============================================================================
# CU16 - GESTIONAR PAGOS Y COMPROBANTES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu16_gestionar_pagos_comprobantes/pago_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any
from app.models.models import UsuarioModel
from app.services.cu16_gestionar_pagos_comprobantes.pago_service import PagoService


class PagoController:

    @staticmethod
    def listar_metodos_pago(db: Session, tenant_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        CU16: Delegación para listar métodos de pago disponibles en el sistema.
        """
        return PagoService.listar_metodos_pago(db=db, tenant_id=tenant_id)

    @staticmethod
    def iniciar_pago(
        db: Session,
        current_user: UsuarioModel,
        venta_id: int,
        metodo_id: int,
        return_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        CU16: Inicia la transacción de cobro (PayPal, QR Interoperable, Tarjeta o Efectivo).
        """
        return PagoService.iniciar_pago(
            db=db,
            current_user=current_user,
            venta_id=venta_id,
            metodo_id=metodo_id,
            return_url=return_url,
            cancel_url=cancel_url,
            tenant_id=tenant_id
        )

    @staticmethod
    def capturar_pago_paypal(
        db: Session,
        current_user: UsuarioModel,
        venta_id: int,
        token_paypal: Optional[str] = None,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        CU16: Confirma el retorno exitoso de la pasarela de PayPal.
        """
        return PagoService.capturar_pago_paypal(
            db=db,
            current_user=current_user,
            venta_id=venta_id,
            token_paypal=token_paypal,
            tenant_id=tenant_id
        )

    @staticmethod
    def obtener_comprobante_oficial(
        db: Session,
        venta_id: int,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        CU16: Retorna los datos estructurados del comprobante/recibo oficial con QR fiscal.
        """
        return PagoService.obtener_comprobante_oficial(
            db=db,
            venta_id=venta_id,
            tenant_id=tenant_id
        )
