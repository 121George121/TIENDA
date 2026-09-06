# ==============================================================================
# CAPA VISTA / RUTAS API (MVC - VIEW / ROUTER)
# Módulo: Clientes (CU03)
# Ubicación: backend/app/routes/cliente_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.models import UsuarioModel
from app.controllers.cu3_gestionar_clientes.cliente_controller import ClienteController
from app.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteEstadoUpdate,
    ClienteResponse,
    ClientePerfilResponse,
    HistorialCompraResponse,
    HistorialReservaResponse
)

router = APIRouter(prefix="/clientes", tags=["Clientes (CU03 - Vista API)"])

# --- RUTAS ACTOR CLIENTE ---

@router.get("/me", response_model=ClientePerfilResponse, summary="Consultar perfil del cliente autenticado")
def consultar_perfil_cliente(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Permite al cliente autenticado consultar su propia información de perfil"""
    return ClienteController.obtener_cliente(db=db, cliente_id=current_user.id)

@router.put("/me", response_model=ClientePerfilResponse, summary="Actualizar información personal del cliente")
def actualizar_perfil_cliente(
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Permite al cliente actualizar sus datos personales de perfil"""
    return ClienteController.actualizar_cliente(db=db, cliente_id=current_user.id, cliente_data=cliente_data)

@router.get("/me/compras", response_model=List[HistorialCompraResponse], summary="Consultar historial de compras del cliente")
def consultar_mis_compras(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Permite al cliente consultar su historial de compras u órdenes realizadas"""
    return ClienteController.obtener_compras(db=db, cliente_id=current_user.id)

@router.get("/me/reservas", response_model=List[HistorialReservaResponse], summary="Consultar historial de reservas del cliente")
def consultar_mis_reservas(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Permite al cliente consultar su historial de reservas"""
    return ClienteController.obtener_reservas(db=db, cliente_id=current_user.id)


# --- RUTAS ACTOR ADMINISTRADOR ---

@router.get("/", response_model=List[ClienteResponse], summary="Listar y buscar clientes (Administrador)")
def listar_clientes(
    search: Optional[str] = Query(None, description="Buscar por nombre, apellido, email o teléfono"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Listar y buscar clientes registrados con métricas de órdenes"""
    return ClienteController.listar_clientes(db=db, search=search, activo=activo, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=ClienteResponse, summary="Ver detalle del cliente")
def obtener_detalle_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Ver el detalle y perfil de un cliente específico por ID"""
    return ClienteController.obtener_cliente(db=db, cliente_id=cliente_id)

@router.post("/", response_model=ClientePerfilResponse, status_code=status.HTTP_201_CREATED, summary="Registrar nuevo cliente")
def crear_cliente(
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Registrar un nuevo cliente desde el panel admin (a diferencia de /auth/registro, este alta no pasa por verificación OTP)"""
    return ClienteController.crear_cliente(db=db, cliente_data=cliente_data)

@router.put("/{cliente_id}", response_model=ClientePerfilResponse, summary="Editar información del cliente")
def editar_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Editar la información personal o de contacto de un cliente"""
    return ClienteController.actualizar_cliente(db=db, cliente_id=cliente_id, cliente_data=cliente_data)

@router.patch("/{cliente_id}/estado", response_model=ClientePerfilResponse, summary="Activar / Desactivar cliente")
def cambiar_estado_cliente(
    cliente_id: int,
    estado_data: ClienteEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Cambiar el estado de acceso activo o inactivo del cliente"""
    return ClienteController.cambiar_estado(db=db, cliente_id=cliente_id, activo=estado_data.activo)

@router.delete("/{cliente_id}", summary="Realizar baja lógica de cliente")
def dar_baja_logica_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Dar de baja lógicamente a un cliente (establece activo = False sin eliminar registros)"""
    return ClienteController.baja_logica(db=db, cliente_id=cliente_id)

@router.get("/{cliente_id}/compras", response_model=List[HistorialCompraResponse], summary="Historial de compras del cliente por ID")
def obtener_compras_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Consultar el historial de compras de un cliente específico por ID"""
    return ClienteController.obtener_compras(db=db, cliente_id=cliente_id)

@router.get("/{cliente_id}/reservas", response_model=List[HistorialReservaResponse], summary="Historial de reservas del cliente por ID")
def obtener_reservas_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_active_user)
):
    """Consultar el historial de reservas de un cliente específico por ID"""
    return ClienteController.obtener_reservas(db=db, cliente_id=cliente_id)
