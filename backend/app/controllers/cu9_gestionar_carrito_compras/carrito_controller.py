# ==============================================================================
# CU09 - GESTIONAR CARRITO DE COMPRAS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Arquitectura: Multi-Tenant SaaS con Validación de Stock en Tiempo Real
# Ubicación: backend/app/controllers/cu9_gestionar_carrito_compras/carrito_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from app.services.cu9_gestionar_carrito_compras.carrito_service import CarritoService
from app.schemas.carrito_schema import (
    CarritoResponse, AgregarItemCarritoRequest,
    ActualizarCantidadItemRequest, AsignarSucursalCarritoRequest
)


class CarritoController:
    """
    Controlador MVC para la administración del Carrito de Compras.
    Orquesta la lógica de negocio, validaciones multitenant y stock en tiendas físicas.
    """

    @staticmethod
    def obtener_carrito(db: Session, usuario_id: int, tenant_id: int = 1) -> CarritoResponse:
        """Obtiene el estado completo del carrito activo con stock en tiempo real"""
        return CarritoService.obtener_carrito(
            db=db,
            usuario_id=usuario_id,
            tenant_id=tenant_id
        )

    @staticmethod
    def agregar_item(
        db: Session,
        usuario_id: int,
        datos: AgregarItemCarritoRequest,
        tenant_id: int = 1
    ) -> CarritoResponse:
        """Agrega una prenda o variante al carrito con verificación de stock"""
        return CarritoService.agregar_item(
            db=db,
            usuario_id=usuario_id,
            datos=datos,
            tenant_id=tenant_id
        )

    @staticmethod
    def actualizar_cantidad(
        db: Session,
        usuario_id: int,
        variante_id: int,
        datos: ActualizarCantidadItemRequest,
        tenant_id: int = 1
    ) -> CarritoResponse:
        """Modifica la cantidad de una prenda o la retira si la cantidad es 0"""
        return CarritoService.actualizar_cantidad(
            db=db,
            usuario_id=usuario_id,
            variante_id=variante_id,
            datos=datos,
            tenant_id=tenant_id
        )

    @staticmethod
    def eliminar_item(
        db: Session,
        usuario_id: int,
        variante_id: int,
        tenant_id: int = 1
    ) -> CarritoResponse:
        """Elimina una prenda del carrito"""
        return CarritoService.eliminar_item(
            db=db,
            usuario_id=usuario_id,
            variante_id=variante_id,
            tenant_id=tenant_id
        )

    @staticmethod
    def asignar_sucursal(
        db: Session,
        usuario_id: int,
        datos: AsignarSucursalCarritoRequest,
        tenant_id: int = 1
    ) -> CarritoResponse:
        """Asigna la sucursal física de retiro o compra al carrito"""
        return CarritoService.asignar_sucursal(
            db=db,
            usuario_id=usuario_id,
            datos=datos,
            tenant_id=tenant_id
        )

    @staticmethod
    def vaciar_carrito(db: Session, usuario_id: int, tenant_id: int = 1) -> CarritoResponse:
        """Elimina todos los productos del carrito"""
        return CarritoService.vaciar_carrito(
            db=db,
            usuario_id=usuario_id,
            tenant_id=tenant_id
        )

    # Alias de compatibilidad hacia atrás
    obtener_carrito_dto = obtener_carrito
