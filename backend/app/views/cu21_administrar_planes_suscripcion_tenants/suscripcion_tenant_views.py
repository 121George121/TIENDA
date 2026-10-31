# ==============================================================================
# CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> VISTAS (MVC - VIEW)
# Ubicación: backend/app/views/cu21_administrar_planes_suscripcion_tenants/suscripcion_tenant_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.controllers.cu21_administrar_planes_suscripcion_tenants.suscripcion_tenant_controller import SuscripcionTenantController
from app.schemas.cu21_administrar_planes_suscripcion_tenants.suscripcion_tenant_schema import (
    PlanSuscripcionCreate, PlanSuscripcionUpdate, PlanSuscripcionResponse,
    TenantCreate, TenantResponse, TenantCambiarPlanRequest,
    TenantToggleEstadoRequest, RenovarSuscripcionRequest, KpiSaaSResponse
)

router = APIRouter(prefix="/suscripciones-tenants", tags=["CU21 - Suscripciones y Tenants"])


# ------------------------------------------------------------------------------
# ENDPOINTS DE PLANES COMERCIALES
# ------------------------------------------------------------------------------

@router.get("/planes", summary="Listar planes de suscripción comerciales")
def listar_planes(
    solo_activos: bool = Query(False, description="Filtrar únicamente planes activos comercialmente"),
    db: Session = Depends(get_db)
):
    """Retorna la lista de planes de suscripción disponibles."""
    planes = SuscripcionTenantController.listar_planes(db, solo_activos=solo_activos)
    return {"exito": True, "planes": planes}


@router.post("/planes", summary="Crear un nuevo plan de suscripción", status_code=status.HTTP_201_CREATED)
def crear_plan(
    data: PlanSuscripcionCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Registra un nuevo plan comercial con límites de sucursales, usuarios y catálogo."""
    try:
        nuevo_plan = SuscripcionTenantController.crear_plan(db, data, usuario_id=current_user.id)
        return {"exito": True, "plan": nuevo_plan}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear plan: {str(e)}")


@router.put("/planes/{plan_id}", summary="Actualizar características de un plan existente")
def actualizar_plan(
    plan_id: int,
    data: PlanSuscripcionUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Actualiza tarifas, límites o estado activo de un plan."""
    try:
        plan = SuscripcionTenantController.actualizar_plan(db, plan_id, data, usuario_id=current_user.id)
        return {"exito": True, "plan": plan}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar plan: {str(e)}")


# ------------------------------------------------------------------------------
# ENDPOINTS DE EMPRESAS / TENANTS
# ------------------------------------------------------------------------------

@router.get("/tenants", summary="Listar tenants con métricas de uso y suscripción actual")
def listar_tenants(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna la lista completa de empresas con su cuota de sucursales y usuarios usados."""
    tenants = SuscripcionTenantController.listar_tenants(db)
    return {"exito": True, "tenants": tenants}


@router.get("/tenants/{tenant_id}", summary="Obtener detalle integral de un tenant")
def obtener_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna métricas, configuración y suscripciones de un tenant específico."""
    data = SuscripcionTenantController.obtener_tenant(db, tenant_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant no encontrado.")
    return {"exito": True, "data": data}


@router.post("/tenants", summary="Dar de alta una nueva empresa (Tenant) con plan y suscripción", status_code=status.HTTP_201_CREATED)
def registrar_tenant(
    data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Registra un nuevo tenant, su configuración regional por defecto y su suscripción inicial."""
    try:
        tenant = SuscripcionTenantController.registrar_tenant(db, data, usuario_id=current_user.id)
        return {"exito": True, "tenant": tenant}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al registrar tenant: {str(e)}")


@router.put("/tenants/{tenant_id}/plan", summary="Cambiar el plan de suscripción de un tenant")
def cambiar_plan_tenant(
    tenant_id: int,
    data: TenantCambiarPlanRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Aplica Upgrade o Downgrade de plan a un tenant generando el registro de auditoría."""
    try:
        tenant = SuscripcionTenantController.cambiar_plan_tenant(
            db, tenant_id=tenant_id, nuevo_plan_id=data.nuevo_plan_id, motivo=data.motivo, usuario_id=current_user.id
        )
        return {"exito": True, "tenant": tenant}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al cambiar plan: {str(e)}")


@router.put("/tenants/{tenant_id}/estado", summary="Activar o suspender el acceso de un tenant")
def toggle_tenant_estado(
    tenant_id: int,
    data: TenantToggleEstadoRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Bloquea o rehabilita el acceso operativo de un tenant en la plataforma."""
    try:
        tenant = SuscripcionTenantController.toggle_tenant_estado(
            db, tenant_id=tenant_id, activo=data.activo, motivo=data.motivo, usuario_id=current_user.id
        )
        return {"exito": True, "tenant": tenant}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al cambiar estado: {str(e)}")


@router.post("/tenants/{tenant_id}/renovar", summary="Renovar la suscripción de un tenant")
def renovar_suscripcion(
    tenant_id: int,
    data: RenovarSuscripcionRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Extiende la vigencia del contrato SaaS de un tenant."""
    try:
        suscripcion = SuscripcionTenantController.renovar_suscripcion(
            db, tenant_id=tenant_id, meses=data.meses, metodo_pago=data.metodo_pago or "TRANSFERENCIA_BANCARIA", usuario_id=current_user.id
        )
        return {"exito": True, "suscripcion": suscripcion}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al renovar suscripción: {str(e)}")


@router.get("/kpis", summary="Obtener KPIs ejecutivos de la plataforma SaaS Multi-Tenant")
def obtener_kpis(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Retorna métricas ejecutivas: Total tenants, MRR estimado, distribución de planes."""
    kpis = SuscripcionTenantController.obtener_kpis(db)
    return {"exito": True, "kpis": kpis}
