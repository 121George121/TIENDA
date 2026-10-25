# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU3 - Gestionar Clientes (Multi-Tenant SaaS)
# Ubicación: backend/app/controllers/cu3_gestionar_clientes/cliente_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.cu3_gestionar_clientes.cliente_service import ClienteService
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteController:
    """
    Controlador MVC para la gestión de clientes en entorno Multi-Tenant SaaS.
    Coordina peticiones de la API hacia la lógica de dominio y auditoría de clientes.
    """

    @staticmethod
    def listar_clientes(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Lista clientes con aislamiento estricto por tenant"""
        return ClienteService.listar_clientes(
            db=db,
            tenant_id=tenant_id,
            search=search,
            activo=activo,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def obtener_cliente_por_id(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Obtiene el detalle completo de un cliente validando el tenant"""
        return ClienteService.obtener_cliente_por_id(
            db=db,
            cliente_id=cliente_id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_cliente(
        db: Session,
        cliente_data: ClienteCreate,
        tenant_id: int = 1,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Registra un nuevo cliente para el tenant asignado"""
        return ClienteService.crear_cliente(
            db=db,
            cliente_data=cliente_data,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def actualizar_cliente(
        db: Session,
        cliente_id: int,
        cliente_data: ClienteUpdate,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Actualiza la información personal y de perfil del cliente"""
        return ClienteService.actualizar_cliente(
            db=db,
            cliente_id=cliente_id,
            cliente_data=cliente_data,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def cambiar_estado_cliente(
        db: Session,
        cliente_id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Activa o suspende el acceso del cliente"""
        return ClienteService.cambiar_estado_cliente(
            db=db,
            cliente_id=cliente_id,
            activo=activo,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def dar_baja_logica_cliente(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Aplica baja lógica al cliente"""
        return ClienteService.dar_baja_logica_cliente(
            db=db,
            cliente_id=cliente_id,
            tenant_id=tenant_id,
            operador_id=operador_id
        )

    @staticmethod
    def obtener_historial_compras(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Consulta el historial de órdenes y compras del cliente"""
        return ClienteService.obtener_historial_compras(
            db=db,
            cliente_id=cliente_id,
            tenant_id=tenant_id
        )

    @staticmethod
    def obtener_historial_reservas(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Consulta las reservas de prendas del cliente en las sucursales"""
        return ClienteService.obtener_historial_reservas(
            db=db,
            cliente_id=cliente_id,
            tenant_id=tenant_id
        )


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
CustomerController = ClienteController

ClienteController.obtener_cliente = ClienteController.obtener_cliente_por_id
ClienteController.cambiar_estado = ClienteController.cambiar_estado_cliente
ClienteController.baja_logica = ClienteController.dar_baja_logica_cliente
ClienteController.obtener_compras = ClienteController.obtener_historial_compras
ClienteController.obtener_reservas = ClienteController.obtener_historial_reservas

ClienteController.get_all = ClienteController.listar_clientes
ClienteController.get_by_id = ClienteController.obtener_cliente_por_id
ClienteController.create = ClienteController.crear_cliente
ClienteController.update = ClienteController.actualizar_cliente
ClienteController.toggle_status = ClienteController.cambiar_estado_cliente
ClienteController.logical_delete = ClienteController.dar_baja_logica_cliente
