# ==============================================================================
# CU12 - UTILIZAR VESTIDOR VIRTUAL -> VISTAS / ROUTER (CAPA VIEW - MVC)
# Ubicación: backend/app/views/cu12_vestidor_virtual_ia/vestidor_ia_views.py
# ==============================================================================

import io
from fastapi import APIRouter, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
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
    CU12: Analiza la fotografía del usuario y la prenda seleccionada con Google Gemini AI
    para determinar contextura corporal, recomendar la talla adecuada y calce ergonómico.
    """
    resultado = await VestidorIaController.analizar_fisonomia_y_ajuste(
        imagen=imagen,
        producto_nombre=producto_nombre,
        talla_actual=talla_actual,
        color_seleccionado=color_seleccionado
    )
    return resultado


@router.get("/prenda-transparente")
def obtener_prenda_transparente(
    imagen_url: str = Query(..., description="URL de la imagen del producto en el catálogo")
):
    """
    CU12: Toma una imagen del producto del catálogo y le remueve el fondo con IA (Rembg / BiRefNet),
    entregando un PNG transparente con sombras suaves de tela en tiempo real.
    """
    png_bytes = VestidorIaController.aislar_prenda_transparente(imagen_url)
    return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")


@router.post("/try-on-fotorrealista")
async def generar_tryon_fotorrealista(
    prenda_url: str = Form(...),
    talla: str = Form("M"),
    color: str = Form("Grafito"),
    imagen_usuario: UploadFile = File(...)
):
    """
    CU12: Motor de Virtual Try-On Fotorrealista (IDM-VTON / Diffusion Pipeline).
    Toma la foto del usuario y la prenda y genera la imagen real de la persona
    vistiendo la ropa.
    """
    resultado = await VestidorIaController.generar_virtual_tryon(
        imagen_usuario=imagen_usuario,
        prenda_url=prenda_url,
        talla=talla,
        color=color
    )
    return resultado
