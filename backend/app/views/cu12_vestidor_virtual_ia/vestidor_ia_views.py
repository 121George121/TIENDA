# ==============================================================================
# CU12 - UTILIZAR VESTIDOR VIRTUAL -> VISTAS / ROUTER (CAPA VIEW - MVC)
# Ubicación: backend/app/views/cu12_vestidor_virtual_ia/vestidor_ia_views.py
# ==============================================================================

import io
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, Header, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.models import UsuarioModel
from app.models.saas_tenant.tenant_model import Tenant
from app.controllers.cu12_vestidor_virtual_ia.vestidor_ia_controller import VestidorIaController

router = APIRouter(prefix="/vestidor", tags=["CU12 - Vestidor Virtual e IA"])


def get_current_user_id_optional(
    authorization: Optional[str] = Header(None),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
) -> int:
    """Extrae el ID del usuario si está autenticado; o retorna usuario por defecto del tenant"""
    tenant_id = x_tenant_id or 1

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        email = verify_token(token)
        if email:
            user = (
                db.query(UsuarioModel)
                .filter(
                    UsuarioModel.email == email,
                    UsuarioModel.tenant_id == tenant_id,
                )
                .first()
            )
            if user:
                return user.id

    first_user = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.tenant_id == tenant_id, UsuarioModel.activo == True)
        .first()
    )
    return first_user.id if first_user else 1


@router.post("/analisis-ia", summary="Diagnóstico fisonómico y recomendación de talla con IA")
async def analizar_fisonomia_vestidor(
    producto_nombre: str = Form(...),
    talla_actual: str = Form("M"),
    color_seleccionado: str = Form("Grafito"),
    imagen: Optional[UploadFile] = File(None),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id_optional),
):
    """
    CU12: Analiza la fotografía del usuario y la prenda seleccionada con Google Gemini AI
    para determinar contextura corporal, recomendar la talla adecuada y calce ergonómico.
    Aislado por tenant con verificación de suscripción y registro en bitácora.
    """
    tenant_id = x_tenant_id or 1
    return await VestidorIaController.analizar_fisonomia_y_ajuste(
        imagen=imagen,
        producto_nombre=producto_nombre,
        talla_actual=talla_actual,
        color_seleccionado=color_seleccionado,
        db=db,
        usuario_id=usuario_id,
        tenant_id=tenant_id,
    )


@router.get("/prenda-transparente", summary="Remover fondo de prenda del catálogo en tiempo real")
def obtener_prenda_transparente(
    imagen_url: str = Query(..., description="URL de la imagen del producto en el catálogo"),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
):
    """
    CU12: Toma una imagen del producto del catálogo y le remueve el fondo con IA (Rembg / BiRefNet),
    entregando un PNG transparente con sombras suaves de tela en tiempo real.
    """
    png_bytes = VestidorIaController.aislar_prenda_transparente(imagen_url)
    return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")


@router.post("/try-on-fotorrealista", summary="Prueba virtual de ropa fotorrealista (Virtual Try-On)")
async def generar_tryon_fotorrealista(
    prenda_url: str = Form(...),
    producto_nombre: str = Form(""),
    talla: str = Form("M"),
    color: str = Form("Grafito"),
    imagen_usuario: UploadFile = File(...),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user_id_optional),
):
    """
    CU12: Motor de Virtual Try-On Fotorrealista (IDM-VTON / Diffusion Pipeline / Local HD Composite).
    Toma la foto del usuario y la prenda y genera la imagen real de la persona vistiendo la ropa.
    """
    tenant_id = x_tenant_id or 1
    return await VestidorIaController.generar_virtual_tryon(
        imagen_usuario=imagen_usuario,
        prenda_url=prenda_url,
        producto_nombre=producto_nombre,
        talla=talla,
        color=color,
        db=db,
        usuario_id=usuario_id,
        tenant_id=tenant_id,
    )
