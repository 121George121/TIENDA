# ==============================================================================
# CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu21_administrar_planes_suscripcion_tenants/suscripcion_tenant_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.services.cu21_administrar_planes_suscripcion_tenants.suscripcion_tenant_service import SuscripcionTenantService


class SuscripcionTenantController:

    @staticmethod
    def listar_planes(db: Session) -> List[Any]:
        return SuscripcionTenantService.listar_planes(db)

    @staticmethod
    def listar_tenants(db: Session) -> List[Any]:
        return SuscripcionTenantService.listar_tenants(db)

    @staticmethod
    def obtener_tenant(db: Session, tenant_id: int) -> Optional[Any]:
        return SuscripcionTenantService.obtener_tenant(db, tenant_id)

    @staticmethod
    def registrar_tenant(db: Session, nombre: str, slug: str, plan_id: int, email: str) -> Any:
        return SuscripcionTenantService.crear_tenant_con_plan(db, nombre, slug, plan_id, email)
