# ==============================================================================
# CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> SERVICIO (MVC - SERVICE)
# Ubicación: backend/app/services/cu21_administrar_planes_suscripcion_tenants/suscripcion_tenant_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.saas_tenant.tenant_model import PlanSuscripcion, Tenant, TenantSuscripcion, TenantConfiguracion


class SuscripcionTenantService:
    """
    Servicio de administración SaaS: Planes, cuotas de sucursales/usuarios y suscripciones multi-tenant.
    """

    @staticmethod
    def listar_planes(db: Session) -> List[PlanSuscripcion]:
        return db.query(PlanSuscripcion).filter(PlanSuscripcion.activo == True).all()

    @staticmethod
    def listar_tenants(db: Session) -> List[Tenant]:
        return db.query(Tenant).all()

    @staticmethod
    def obtener_tenant(db: Session, tenant_id: int) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.id == tenant_id).first()

    @staticmethod
    def crear_tenant_con_plan(
        db: Session,
        nombre_empresa: str,
        dominio_slug: str,
        plan_id: int,
        email_admin: str
    ) -> Tenant:
        nuevo_tenant = Tenant(
            nombre=nombre_empresa,
            slug=dominio_slug.lower().replace(" ", "-"),
            activo=True,
            created_at=datetime.utcnow()
        )
        db.add(nuevo_tenant)
        db.commit()
        db.refresh(nuevo_tenant)

        # Crear suscripción activa por 1 año
        suscripcion = TenantSuscripcion(
            tenant_id=nuevo_tenant.id,
            plan_id=plan_id,
            estado="ACTIVA",
            fecha_inicio=datetime.utcnow(),
            fecha_fin=datetime.utcnow() + timedelta(days=365)
        )
        db.add(suscripcion)
        db.commit()
        return nuevo_tenant
