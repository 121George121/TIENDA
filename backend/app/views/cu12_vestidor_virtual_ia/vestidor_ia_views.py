# ==============================================================================
# CU12 - UTILIZAR VESTIDOR VIRTUAL -> VISTAS / ROUTER (CAPA VIEW - MVC)
# Ubicación: backend/app/views/cu12_vestidor_virtual_ia/vestidor_ia_views.py
# ==============================================================================

from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional

from app.controllers.cu12_vestidor_virtual_ia.vestidor_ia_controller import VestidorIaController

router = APIRouter(prefix="/vestidor", tags=["CU12 - Vestidor Virtual e IA"])


@router.post("/analisis-ia")
async def analizar_fisonomia_vestidor(
    producto_nombre: str = Form(...),
    talla_actual: str = Form("M"),
    color_seleccionado: str = Form("Grafito"),
    imagen: Optional[UploadFile] = File(None)
):
    """
    CU12: Analiza la fotografía del usuario y la prenda seleccionada con Inteligencia Artificial
    para determinar contextura corporal, recomendar la talla adecuada y calce ergonómico.
    """
    resultado = await VestidorIaController.analizar_fisonomia_y_ajuste(
        imagen=imagen,
        producto_nombre=producto_nombre,
        talla_actual=talla_actual,
        color_seleccionado=color_seleccionado
    )
    return resultado
