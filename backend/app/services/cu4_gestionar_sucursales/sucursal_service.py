# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: CU4 - Gestionar Sucursales (Multi-Tenant SaaS)
# Ubicación: backend/app/services/cu4_gestionar_sucursales/sucursal_service.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.models import Sucursal, Tenant, PlanSuscripcion, Bitacora
from app.schemas.sucursal_schema import SucursalCreate, SucursalUpdate


class SucursalService:
    """
    Servicio de dominio para la administración de sucursales físicas,
    aislamiento Multi-Tenant, control estricto de cuotas por Plan de Suscripción y auditoría.
    """

    @staticmethod
    def listar_sucursales(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        ciudad: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Sucursal]:
        """
        Lista todas las sucursales del tenant aplicando filtros de búsqueda y estado.
        """
        query = db.query(Sucursal).filter(Sucursal.tenant_id == tenant_id)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                (Sucursal.nombre.ilike(pattern)) |
                (Sucursal.direccion.ilike(pattern)) |
                (Sucursal.ciudad.ilike(pattern)) |
                (Sucursal.telefono.ilike(pattern))
            )

        if ciudad:
            query = query.filter(Sucursal.ciudad.ilike(f"%{ciudad.strip()}%"))

        if activo is not None:
            query = query.filter(Sucursal.activo == activo)

        return query.order_by(Sucursal.id.asc()).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_sucursal_por_id(
        db: Session,
        sucursal_id: int,
        tenant_id: Optional[int] = None
    ) -> Sucursal:
        """
        Obtiene el detalle de una sucursal validando su pertenencia al Tenant.
        """
        query = db.query(Sucursal).filter(Sucursal.id == sucursal_id)
        if tenant_id is not None:
            query = query.filter(Sucursal.tenant_id == tenant_id)

        sucursal = query.first()
        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sucursal no encontrada en este comercio"
            )
        return sucursal

    @staticmethod
    def crear_sucursal(
        db: Session,
        sucursal_data: SucursalCreate,
        tenant_id: int = 1,
        operador_id: Optional[int] = None
    ) -> Sucursal:
        """
        Registra una nueva sucursal física validando el límite estipulado por el Plan de Suscripción.
        """
        # 1. Validar restricción por Plan de Suscripción del Tenant
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant and tenant.plan_id:
            plan = db.query(PlanSuscripcion).filter(PlanSuscripcion.id == tenant.plan_id).first()
            if plan and plan.limite_sucursales:
                total_activas = db.query(Sucursal).filter(
                    Sucursal.tenant_id == tenant_id,
                    Sucursal.activo == True
                ).count()
                if total_activas >= plan.limite_sucursales:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=(
                            f"Límite de sucursales alcanzado: su plan '{plan.nombre}' permite un máximo de "
                            f"{plan.limite_sucursales} sucursales físicas activas. Actualice su suscripción para registrar más sedes."
                        )
                    )

        # 2. Validar que no exista otra sucursal con el mismo nombre en el tenant
        clean_nombre = sucursal_data.nombre.strip()
        existente = db.query(Sucursal).filter(
            func.lower(Sucursal.nombre) == clean_nombre.lower(),
            Sucursal.tenant_id == tenant_id
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una sucursal con ese nombre en este comercio"
            )

        # 3. Crear registro
        nueva_sucursal = Sucursal(
            tenant_id=tenant_id,
            nombre=clean_nombre,
            ciudad=sucursal_data.ciudad.strip() if sucursal_data.ciudad else None,
            direccion=sucursal_data.direccion.strip() if sucursal_data.direccion else None,
            telefono=sucursal_data.telefono.strip() if sucursal_data.telefono else None,
            latitud=sucursal_data.latitud,
            longitud=sucursal_data.longitud,
            activo=sucursal_data.activo if sucursal_data.activo is not None else True
        )
        db.add(nueva_sucursal)
        db.commit()
        db.refresh(nueva_sucursal)

        # 4. Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_SUCURSAL",
                modulo="SUCURSALES",
                usuario_id=operador_id or 1,
                detalle=f"Apertura de sucursal '{nueva_sucursal.nombre}' ({nueva_sucursal.ciudad or 'Sin ciudad'}) en tenant #{tenant_id}",
                datos_nuevos={
                    "nombre": nueva_sucursal.nombre,
                    "ciudad": nueva_sucursal.ciudad,
                    "direccion": nueva_sucursal.direccion,
                    "tenant_id": tenant_id
                }
            )
        except Exception:
            pass

        return nueva_sucursal

    @staticmethod
    def actualizar_sucursal(
        db: Session,
        sucursal_id: int,
        sucursal_data: SucursalUpdate,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Sucursal:
        """
        Actualiza los datos comerciales, de ubicación o contacto de la sucursal.
        """
        sucursal = SucursalService.obtener_sucursal_por_id(db, sucursal_id, tenant_id=tenant_id)

        if sucursal_data.nombre:
            clean_nombre = sucursal_data.nombre.strip()
            if clean_nombre.lower() != sucursal.nombre.lower():
                existente = db.query(Sucursal).filter(
                    func.lower(Sucursal.nombre) == clean_nombre.lower(),
                    Sucursal.tenant_id == sucursal.tenant_id,
                    Sucursal.id != sucursal.id
                ).first()
                if existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe otra sucursal con ese nombre en este comercio"
                    )
                sucursal.nombre = clean_nombre

        if sucursal_data.ciudad is not None:
            sucursal.ciudad = sucursal_data.ciudad.strip() if sucursal_data.ciudad else None
        if sucursal_data.direccion is not None:
            sucursal.direccion = sucursal_data.direccion.strip() if sucursal_data.direccion else None
        if sucursal_data.telefono is not None:
            sucursal.telefono = sucursal_data.telefono.strip() if sucursal_data.telefono else None
        if sucursal_data.latitud is not None:
            sucursal.latitud = sucursal_data.latitud
        if sucursal_data.longitud is not None:
            sucursal.longitud = sucursal_data.longitud
        if sucursal_data.activo is not None:
            sucursal.activo = sucursal_data.activo

        db.commit()
        db.refresh(sucursal)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR_SUCURSAL",
                modulo="SUCURSALES",
                usuario_id=operador_id or 1,
                detalle=f"Actualización de datos para la sucursal '{sucursal.nombre}'",
                datos_nuevos={"nombre": sucursal.nombre, "ciudad": sucursal.ciudad, "activo": sucursal.activo}
            )
        except Exception:
            pass

        return sucursal

    @staticmethod
    def cambiar_estado_sucursal(
        db: Session,
        sucursal_id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Sucursal:
        """
        Activa o suspende una sucursal, verificando límites si se intenta reactivar.
        """
        sucursal = SucursalService.obtener_sucursal_por_id(db, sucursal_id, tenant_id=tenant_id)

        # Si se reactiva, verificar límite de plan
        if activo and not sucursal.activo:
            tenant = db.query(Tenant).filter(Tenant.id == sucursal.tenant_id).first()
            if tenant and tenant.plan_id:
                plan = db.query(PlanSuscripcion).filter(PlanSuscripcion.id == tenant.plan_id).first()
                if plan and plan.limite_sucursales:
                    total_activas = db.query(Sucursal).filter(
                        Sucursal.tenant_id == sucursal.tenant_id,
                        Sucursal.activo == True
                    ).count()
                    if total_activas >= plan.limite_sucursales:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=(
                                f"No se puede reactivar la sucursal: su plan '{plan.nombre}' permite un máximo de "
                                f"{plan.limite_sucursales} sucursales activas."
                            )
                        )

        sucursal.activo = activo
        db.commit()
        db.refresh(sucursal)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO_SUCURSAL",
                modulo="SUCURSALES",
                usuario_id=operador_id or 1,
                detalle=f"Cambio de estado de sucursal '{sucursal.nombre}' a {'Activa' if activo else 'Inactiva'}",
                datos_nuevos={"activo": activo}
            )
        except Exception:
            pass

        return sucursal

    @staticmethod
    def dar_baja_logica_sucursal(
        db: Session,
        sucursal_id: int,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Aplica baja lógica a una sucursal física manteniendo el historial de inventario y reservas.
        """
        sucursal = SucursalService.cambiar_estado_sucursal(
            db=db,
            sucursal_id=sucursal_id,
            activo=False,
            tenant_id=tenant_id,
            operador_id=operador_id
        )
        return {
            "message": f"Sucursal '{sucursal.nombre}' dada de baja lógicamente de forma exitosa",
            "id": sucursal_id,
            "activo": False
        }


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
SucursalService.get_all = SucursalService.listar_sucursales
SucursalService.get_by_id = SucursalService.obtener_sucursal_por_id
SucursalService.create = SucursalService.crear_sucursal
SucursalService.update = SucursalService.actualizar_sucursal
SucursalService.toggle_status = SucursalService.cambiar_estado_sucursal
SucursalService.logical_delete = SucursalService.dar_baja_logica_sucursal
