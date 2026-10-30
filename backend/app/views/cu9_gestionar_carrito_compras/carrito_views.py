# ==============================================================================
# CU09 - GESTIONAR CARRITO DE COMPRAS -> CAPA VISTA / RUTAS API (MVC - VIEW)
# Ubicación: backend/app/views/cu9_gestionar_carrito_compras/carrito_views.py
# ==============================================================================

from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.models import UsuarioModel, ClienteModel
from app.models.saas_tenant.tenant_model import Tenant
from app.schemas.carrito_schema import (
    CarritoResponse, AgregarItemCarritoRequest,
    ActualizarCantidadItemRequest, AsignarSucursalCarritoRequest
)
from app.controllers.cu9_gestionar_carrito_compras.carrito_controller import (
    CarritoController
)

router = APIRouter(prefix="/carrito", tags=["CU09 - Carrito de Compras"])


def get_current_cart_user_id(
    authorization: Optional[str] = Header(None),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
) -> int:
    """Extrae el ID del cliente del token JWT respetando el tenant; si es invitado, usa o crea el cliente demo del tenant"""
    tenant_id = x_tenant_id or 1

    # Validar que el tenant exista en la plataforma SaaS
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant con ID {tenant_id} no existe en la plataforma SaaS"
        )

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        email = verify_token(token)
        if email:
            user = db.query(UsuarioModel).filter(
                UsuarioModel.email == email,
                UsuarioModel.tenant_id == tenant_id
            ).first()
            if user:
                return user.id

    # Caso Invitado / Demo: usuario activo del tenant
    user_tenant = db.query(UsuarioModel).filter(
        UsuarioModel.tenant_id == tenant_id,
        UsuarioModel.activo == True
    ).first()

    if user_tenant:
        return user_tenant.id

    from app.core.security import get_password_hash
    nuevo_invitado = UsuarioModel(
        nombre=f"Cliente Tenant {tenant_id}",
        apellido="Invitado",
        email=f"invitado_tenant{tenant_id}@tienda.bo",
        passwordhash=get_password_hash("guest123"),
        telefono="70000000",
        tenant_id=tenant_id,
        rolid=3,
        activo=True
    )
    db.add(nuevo_invitado)
    db.commit()
    db.refresh(nuevo_invitado)
    return nuevo_invitado.id


@router.get("", response_model=CarritoResponse, summary="Obtener carrito activo")
def obtener_carrito(
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Retorna el contenido del carrito activo con cálculo de subtotales y stock en tiempo real"""
    tenant_id = x_tenant_id or 1
    return CarritoController.obtener_carrito(
        db=db,
        usuario_id=usuario_id,
        tenant_id=tenant_id
    )


@router.post("/items", response_model=CarritoResponse, status_code=status.HTTP_201_CREATED, summary="Agregar prenda al carrito")
def agregar_item(
    datos: AgregarItemCarritoRequest,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Agrega una prenda/variante validando existencias en la sucursal del tenant"""
    tenant_id = x_tenant_id or 1
    return CarritoController.agregar_item(
        db=db,
        usuario_id=usuario_id,
        datos=datos,
        tenant_id=tenant_id
    )


@router.put("/items/{variante_id}", response_model=CarritoResponse, summary="Actualizar cantidad de una prenda")
def actualizar_cantidad_item(
    variante_id: int,
    datos: ActualizarCantidadItemRequest,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Modifica la cantidad de una prenda o la elimina si la cantidad es 0"""
    tenant_id = x_tenant_id or 1
    return CarritoController.actualizar_cantidad(
        db=db,
        usuario_id=usuario_id,
        variante_id=variante_id,
        datos=datos,
        tenant_id=tenant_id
    )


@router.delete("/items/{variante_id}", response_model=CarritoResponse, summary="Eliminar prenda del carrito")
def eliminar_item(
    variante_id: int,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Quita una prenda del carrito"""
    tenant_id = x_tenant_id or 1
    return CarritoController.eliminar_item(
        db=db,
        usuario_id=usuario_id,
        variante_id=variante_id,
        tenant_id=tenant_id
    )


@router.patch("/sucursal", response_model=CarritoResponse, summary="Asignar tienda física de retiro/compra")
def asignar_sucursal(
    datos: AsignarSucursalCarritoRequest,
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Asigna la sucursal física al carrito para validar stock del pedido"""
    tenant_id = x_tenant_id or 1
    return CarritoController.asignar_sucursal(
        db=db,
        usuario_id=usuario_id,
        datos=datos,
        tenant_id=tenant_id
    )


@router.delete("", response_model=CarritoResponse, summary="Vaciar todo el carrito")
def vaciar_carrito(
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Vacía todos los ítems del carrito"""
    tenant_id = x_tenant_id or 1
    return CarritoController.vaciar_carrito(
        db=db,
        usuario_id=usuario_id,
        tenant_id=tenant_id
    )
