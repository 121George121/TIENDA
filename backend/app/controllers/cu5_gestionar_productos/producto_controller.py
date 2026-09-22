# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: Productos y Catálogo Retail (CU05)
# Ubicación: backend/app/controllers/producto_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Optional, List
from app.services.cu5_gestionar_productos.producto_service import ProductoService
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate
from app.models.models import ProductoModel

class ProductoController:

    @staticmethod
    def listar_productos(
        db: Session,
        search: Optional[str] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductoModel]:
        return ProductoService.get_all(
            db=db, search=search, categoria_id=categoria_id, genero=genero, activo=activo, skip=skip, limit=limit
        )

    @staticmethod
    def obtener_producto(db: Session, id: int) -> ProductoModel:
        return ProductoService.get_by_id(db=db, id=id)

    @staticmethod
    def crear_producto(db: Session, data: ProductoCreate, usuario_id: Optional[int] = None) -> ProductoModel:
        prod = ProductoService.create(db=db, data=data)
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR",
                modulo="PRODUCTOS",
                usuario_id=usuario_id,
                detalle=f"Registro de nuevo producto: {prod.nombre} (ID: {prod.id})",
                datos_nuevos={"id": prod.id, "nombre": prod.nombre, "precio": float(prod.preciobase or 0)}
            )
        except Exception:
            pass
        return prod

    @staticmethod
    def actualizar_producto(db: Session, id: int, data: ProductoUpdate, usuario_id: Optional[int] = None) -> ProductoModel:
        prod = ProductoService.update(db=db, id=id, data=data)
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="MODIFICAR",
                modulo="PRODUCTOS",
                usuario_id=usuario_id,
                detalle=f"Actualización del producto ID={id} ({prod.nombre})",
                datos_nuevos={"id": prod.id, "nombre": prod.nombre, "precio": float(prod.preciobase or 0)}
            )
        except Exception:
            pass
        return prod

    @staticmethod
    def cambiar_estado(db: Session, id: int, activo: bool, usuario_id: Optional[int] = None) -> ProductoModel:
        prod = ProductoService.toggle_status(db=db, id=id, activo=activo)
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO",
                modulo="PRODUCTOS",
                usuario_id=usuario_id,
                detalle=f"Cambio de estado del producto ID={id} a {'Activo' if activo else 'Inactivo'}",
                datos_nuevos={"id": id, "activo": activo}
            )
        except Exception:
            pass
        return prod

    @staticmethod
    def eliminar_producto(db: Session, id: int, usuario_id: Optional[int] = None) -> dict:
        res = ProductoService.delete(db=db, id=id)
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ELIMINAR",
                modulo="PRODUCTOS",
                usuario_id=usuario_id,
                detalle=f"Baja de producto ID={id} del catálogo"
            )
        except Exception:
            pass
        return res

    @staticmethod
    def baja_logica(db: Session, id: int) -> dict:
        return ProductoController.eliminar_producto(db=db, id=id)
