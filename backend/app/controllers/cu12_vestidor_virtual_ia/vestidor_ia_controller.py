# ==============================================================================
# CU12 - UTILIZAR VESTIDOR VIRTUAL MEDIANTE IA -> CONTROLADOR SENIOR (MVC)
# Ubicación: backend/app/controllers/cu12_vestidor_virtual_ia/vestidor_ia_controller.py
# ==============================================================================

import os
from typing import Dict, Any, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.services.cu12_vestidor_virtual_ia.vestidor_service import VestidorService


class VestidorIaController:
    """
    Controlador MVC para el Vestidor Virtual con Inteligencia Artificial.
    Orquesta las peticiones entre las Vistas (Web/Móvil) y la Capa de Servicio.
    """

    @classmethod
    async def analizar_fisonomia_y_ajuste(
        cls,
        imagen: Optional[UploadFile],
        producto_nombre: str,
        talla_actual: str,
        color_seleccionado: str,
        db: Optional[Session] = None,
        usuario_id: Optional[int] = None,
        tenant_id: int = 1,
    ) -> Dict[str, Any]:
        """CU12: Diagnóstico fisonómico, contextura corporal y recomendación inteligente de talla"""
        return await VestidorService.analizar_fisonomia_y_ajuste(
            imagen=imagen,
            producto_nombre=producto_nombre,
            talla_actual=talla_actual,
            color_seleccionado=color_seleccionado,
            db=db,
            usuario_id=usuario_id,
            tenant_id=tenant_id,
        )

    @classmethod
    def aislar_prenda_transparente(cls, imagen_url: str) -> bytes:
        """CU12: Aislamiento automático de prendas removiendo el fondo (Alpha PNG)"""
        return VestidorService.aislar_prenda_transparente(imagen_url)

    @classmethod
    async def generar_virtual_tryon(
        cls,
        imagen_usuario: UploadFile,
        prenda_url: str,
        talla: str,
        color: str,
        producto_nombre: str = "",
        db: Optional[Session] = None,
        usuario_id: Optional[int] = None,
        tenant_id: int = 1,
    ) -> Dict[str, Any]:
        """CU12: Motor de prueba fotorrealista de ropa en cascada neuronal (Decart -> HF -> Local HD)"""
        return await VestidorService.generar_virtual_tryon(
            imagen_usuario=imagen_usuario,
            prenda_url=prenda_url,
            talla=talla,
            color=color,
            producto_nombre=producto_nombre,
            db=db,
            usuario_id=usuario_id,
            tenant_id=tenant_id,
        )

    @staticmethod
    def _ejecutar_hf_idm_vton(user_path: str, garm_path: str, garment_des: str) -> Optional[str]:
        """Ejecuta inferencia fotorrealista con el modelo oficial IDM-VTON en Hugging Face"""
        try:
            from gradio_client import Client, handle_file
            client = Client("yisol/IDM-VTON")
            result = client.predict(
                dict={
                    "background": handle_file(user_path),
                    "layers": [],
                    "composite": None
                },
                garm_img=handle_file(garm_path),
                garment_des=garment_des,
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=30,
                seed=42,
                api_name="/tryon"
            )
            if isinstance(result, (list, tuple)) and len(result) > 0:
                return result[0]
            elif isinstance(result, str):
                return result
            return None
        except Exception as e:
            print(f"[Hugging Face IDM-VTON] Nota: {e}")
            return None

    # --------------------------------------------------------------------------
    # Alias en español para convención MVC uniforme
    # --------------------------------------------------------------------------
    analizar_fisonomia = analizar_fisonomia_y_ajuste
    obtener_prenda_transparente = aislar_prenda_transparente
    probar_prenda_virtual = generar_virtual_tryon
