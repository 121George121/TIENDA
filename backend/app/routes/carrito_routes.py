# ==============================================================================
# RUTAS DE LA API (FASTAPI ROUTER)
# Módulo: CU09 - Gestionar Carrito de Compras
# Ubicación: backend/app/routes/carrito_routes.py
# ==============================================================================

from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.models import UsuarioModel
from app.schemas.carrito_schema import (
    CarritoResponse, AgregarItemCarritoRequest,
    ActualizarCantidadItemRequest, AsignarSucursalCarritoRequest
)
from app.controllers.carrito_controller import CarritoController

router = APIRouter(prefix="/carrito", tags=["CU09 - Carrito de Compras"])

def get_current_cart_user_id(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> int:
    """Extrae el ID del usuario del token JWT; si es invitado, asocia al cliente demo predeterminado"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        email = verify_token(token)
        if email:
            user = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
            if user:
                return user.id

    # Usuario cliente predeterminado (o primer usuario encontrado)
    default_user = db.query(UsuarioModel).first()
    return default_user.id if default_user else 1

@router.get("", response_model=CarritoResponse, summary="Obtener carrito activo")
def obtener_carrito(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Retorna el contenido del carrito activo con stock en tiempo real"""
    return CarritoController.obtener_carrito_dto(db=db, usuario_id=usuario_id)

@router.post("/items", response_model=CarritoResponse, status_code=status.HTTP_201_CREATED, summary="Agregar prenda al carrito")
def agregar_item(
    datos: AgregarItemCarritoRequest,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Agrega una prenda/variante validando disponibilidad en la sucursal"""
    return CarritoController.agregar_item(db=db, usuario_id=usuario_id, datos=datos)

@router.put("/items/{variante_id}", response_model=CarritoResponse, summary="Actualizar cantidad de una prenda")
def actualizar_cantidad_item(
    variante_id: int,
    datos: ActualizarCantidadItemRequest,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Modifica la cantidad de una prenda o la elimina si la cantidad es 0"""
    return CarritoController.actualizar_cantidad(
        db=db, usuario_id=usuario_id, variante_id=variante_id, datos=datos
    )

@router.delete("/items/{variante_id}", response_model=CarritoResponse, summary="Eliminar prenda del carrito")
def eliminar_item(
    variante_id: int,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Quita una prenda del carrito"""
    return CarritoController.eliminar_item(db=db, usuario_id=usuario_id, variante_id=variante_id)

@router.patch("/sucursal", response_model=CarritoResponse, summary="Asignar tienda física de retiro/compra")
def asignar_sucursal(
    datos: AsignarSucursalCarritoRequest,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Asigna la sucursal física al carrito para validar stock del pedido"""
    return CarritoController.asignar_sucursal(db=db, usuario_id=usuario_id, datos=datos)

@router.delete("", response_model=CarritoResponse, summary="Vaciar todo el carrito")
def vaciar_carrito(
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_cart_user_id)
):
    """CU09: Vacía todos los ítems del carrito"""
    return CarritoController.vaciar_carrito(db=db, usuario_id=usuario_id)
