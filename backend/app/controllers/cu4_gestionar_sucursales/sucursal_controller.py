# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU4 - Gestionar Sucursales (Multi-Tenant SaaS)
# Ubicación: backend/app/controllers/cu4_gestionar_sucursales/sucursal_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.cu4_gestionar_sucursales.sucursal_service import SucursalService
from app.schemas.sucursal_schema import SucursalCreate, SucursalUpdate
from app.models.models import Sucursal


class SucursalController:
    """
    Controlador MVC para la gestión de sucursales físicas en entorno Multi-Tenant SaaS.
    Aplica políticas de restricción por plan de suscripción y trazabilidad de eventos.
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
        """Lista las sucursales pertenecientes al tenant activo"""
        return SucursalService.listar_sucursales(
            db=db,
            tenant_id=tenant_id,
            search=search,
            ciudad=ciudad,
            activo=activo,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def obtener_sucursal_por_id(
        db: Session,
        sucursal_id: int,
        tenant_id: Optional[int] = None
    ) -> Sucursal:
        """Obtiene el detalle de una sucursal verificando su tenant"""
        return SucursalService.obtener_sucursal_por_id(
            db=db,
            sucursal_id=sucursal_id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_sucursal(
        db: Session,
        sucursal_data: SucursalCreate,
        tenant_id: int = 1,
        operador_id: Optional[int] = None
    ) -> Sucursal:
        """Crea una sucursal validando el límite del plan de suscripción"""
        return SucursalService.crear_sucursal(
            db=db,
            sucursal_data=sucursal_data,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def actualizar_sucursal(
        db: Session,
        sucursal_id: int,
        sucursal_data: SucursalUpdate,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Sucursal:
        """Actualiza los datos comerciales y de localización de la sucursal"""
        return SucursalService.actualizar_sucursal(
            db=db,
            sucursal_id=sucursal_id,
            sucursal_data=sucursal_data,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def cambiar_estado_sucursal(
        db: Session,
        sucursal_id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Sucursal:
        """Activa o suspende una sucursal física"""
        return SucursalService.cambiar_estado_sucursal(
            db=db,
            sucursal_id=sucursal_id,
            activo=activo,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def dar_baja_logica_sucursal(
        db: Session,
        sucursal_id: int,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Aplica baja lógica preservando inventarios y registros vinculados"""
        return SucursalService.dar_baja_logica_sucursal(
            db=db,
            sucursal_id=sucursal_id,
            tenant_id=tenant_id,
            operador_id=operador_id
        )


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
BranchController = SucursalController

SucursalController.obtener_sucursal = SucursalController.obtener_sucursal_por_id
SucursalController.cambiar_estado = SucursalController.cambiar_estado_sucursal
SucursalController.baja_logica = SucursalController.dar_baja_logica_sucursal

SucursalController.get_all = SucursalController.listar_sucursales
SucursalController.get_by_id = SucursalController.obtener_sucursal_por_id
SucursalController.create = SucursalController.crear_sucursal
SucursalController.update = SucursalController.actualizar_sucursal
SucursalController.toggle_status = SucursalController.cambiar_estado_sucursal
SucursalController.logical_delete = SucursalController.dar_baja_logica_sucursal
