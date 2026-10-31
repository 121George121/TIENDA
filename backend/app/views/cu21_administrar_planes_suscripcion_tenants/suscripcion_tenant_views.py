# ==============================================================================
# CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu21_administrar_planes_suscripcion_tenants/suscripcion_tenant_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.controllers.cu21_administrar_planes_suscripcion_tenants.suscripcion_tenant_controller import SuscripcionTenantController
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel

router = APIRouter(prefix="/suscripciones-tenants", tags=["CU21 - Suscripciones y Tenants"])


class NuevoTenantRequest(BaseModel):
    nombre: str
    slug: str
    plan_id: int
    email: str


@router.get("/planes", summary="Listar planes de suscripción disponibles (Básico, Profesional, Enterprise)")
def listar_planes(db: Session = Depends(get_db)):
    planes = SuscripcionTenantController.listar_planes(db)
    return {"exito": True, "planes": planes}


@router.get("/tenants", summary="Listar tenants registrados")
def listar_tenants(db: Session = Depends(get_db), current_user: UsuarioModel = Depends(get_current_user)):
    tenants = SuscripcionTenantController.listar_tenants(db)
    return {"exito": True, "tenants": tenants}


@router.post("/tenants", summary="Crear un nuevo tenant con plan de suscripción")
def registrar_tenant(req: NuevoTenantRequest, db: Session = Depends(get_db)):
    tenant = SuscripcionTenantController.registrar_tenant(db, req.nombre, req.slug, req.plan_id, req.email)
    return {"exito": True, "tenant": tenant}
