# ==============================================================================
# CU09 - GESTIONAR CARRITO DE COMPRAS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu9_gestionar_carrito_compras/carrito_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from fastapi import HTTPException, status

from app.models.models import (
    CarritoModel, CarritoItemModel, VarianteProductoModel,
    SucursalModel, InventarioSucursalModel
)
from app.schemas.carrito_schema import (
    CarritoResponse, CarritoItemResponse,
    AgregarItemCarritoRequest, ActualizarCantidadItemRequest,
    AsignarSucursalCarritoRequest
)

class CarritoController:

    @staticmethod
    def _obtener_carrito_activo(db: Session, usuario_id: int) -> CarritoModel:
        """Busca el carrito activo del usuario o crea uno nuevo en PostgreSQL"""
        carrito = db.query(CarritoModel).filter(
            CarritoModel.clienteid == usuario_id,
            CarritoModel.estado == "ACTIVO"
        ).first()

        if not carrito:
            carrito = CarritoModel(
                clienteid=usuario_id,
                estado="ACTIVO",
                fechacreacion=datetime.utcnow(),
                fechaactualizacion=datetime.utcnow()
            )
            db.add(carrito)
            db.commit()
            db.refresh(carrito)

        return carrito

    @classmethod
    def obtener_carrito_dto(cls, db: Session, usuario_id: int) -> CarritoResponse:
        """Construye la respuesta completa del carrito con stock en tiempo real"""
        carrito = cls._obtener_carrito_activo(db, usuario_id)

        items_resp = []
        total_items = 0
        total_precio = Decimal("0.00")
        tiene_alertas = False

        sucursal_nombre = carrito.sucursal.nombre if carrito.sucursal else None

        for item in carrito.items:
            variante = item.variante
            if not variante:
                continue

            producto = variante.producto

            # Calcular stock disponible en la sucursal del carrito (o global si no tiene sucursal)
            if carrito.sucursalid:
                inv = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == variante.id,
                    InventarioSucursalModel.sucursalid == carrito.sucursalid
                ).first()
                stock_disp = max(0, (inv.cantidad - inv.stockreservado)) if inv else 0
            else:
                invs = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == variante.id
                ).all()
                stock_disp = sum(max(0, (i.cantidad - i.stockreservado)) for i in invs)

            subtotal = Decimal(str(item.cantidad)) * item.preciounitario
            stock_suficiente = item.cantidad <= stock_disp

            if not stock_suficiente:
                tiene_alertas = True

            total_items += item.cantidad
            total_precio += subtotal

            items_resp.append(
                CarritoItemResponse(
                    variante_id=variante.id,
                    producto_id=producto.id,
                    producto_nombre=producto.nombre,
                    imagen_url=variante.imagenurl or producto.imagenprincipal,
                    sku=variante.sku,
                    talla=variante.talla.nombre if variante.talla else None,
                    color=variante.color.nombre if variante.color else None,
                    codigohex=variante.color.codigohex if variante.color else None,
                    precio_unitario=item.preciounitario,
                    cantidad=item.cantidad,
                    subtotal=subtotal,
                    stock_disponible=stock_disp,
                    stock_suficiente=stock_suficiente
                )
            )

        return CarritoResponse(
            id=carrito.id,
            estado=carrito.estado,
            cliente_id=carrito.clienteid,
            sucursal_id=carrito.sucursalid,
            sucursal_nombre=sucursal_nombre,
            items=items_resp,
            total_items=total_items,
            total_precio=total_precio,
            tiene_alertas_stock=tiene_alertas,
            fecha_actualizacion=carrito.fechaactualizacion
        )

    @classmethod
    def agregar_item(cls, db: Session, usuario_id: int, datos: AgregarItemCarritoRequest) -> CarritoResponse:
        """Agrega una prenda al carrito con validación de existencia y stock"""
        variante = db.query(VarianteProductoModel).filter(
            VarianteProductoModel.id == datos.variante_id,
            VarianteProductoModel.activo == True
        ).first()

        if not variante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variante de prenda no encontrada o inactiva")

        carrito = cls._obtener_carrito_activo(db, usuario_id)

        # Si se especificó sucursal en el request y el carrito no tenía una, asignarla
        if datos.sucursal_id:
            carrito.sucursalid = datos.sucursal_id

        # Validar stock disponible
        if carrito.sucursalid:
            inv = db.query(InventarioSucursalModel).filter(
                InventarioSucursalModel.varianteid == datos.variante_id,
                InventarioSucursalModel.sucursalid == carrito.sucursalid
            ).first()
            stock_disp = max(0, (inv.cantidad - inv.stockreservado)) if inv else 0
        else:
            invs = db.query(InventarioSucursalModel).filter(
                InventarioSucursalModel.varianteid == datos.variante_id
            ).all()
            stock_disp = sum(max(0, (i.cantidad - i.stockreservado)) for i in invs)

        item = db.query(CarritoItemModel).filter(
            CarritoItemModel.carritoid == carrito.id,
            CarritoItemModel.varianteid == datos.variante_id
        ).first()

        cantidad_final = (item.cantidad + datos.cantidad) if item else datos.cantidad

        if cantidad_final > stock_disp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente en la tienda. Disponibles: {stock_disp} uds."
            )

        if item:
            item.cantidad = cantidad_final
        else:
            nuevo_item = CarritoItemModel(
                carritoid=carrito.id,
                varianteid=datos.variante_id,
                cantidad=datos.cantidad,
                preciounitario=variante.precioventa or variante.producto.preciobase,
                fechaagregado=datetime.utcnow()
            )
            db.add(nuevo_item)

        carrito.fechaactualizacion = datetime.utcnow()
        db.commit()

        return cls.obtener_carrito_dto(db, usuario_id)

    @classmethod
    def actualizar_cantidad(cls, db: Session, usuario_id: int, variante_id: int, datos: ActualizarCantidadItemRequest) -> CarritoResponse:
        """Modifica la cantidad de un ítem en el carrito"""
        carrito = cls._obtener_carrito_activo(db, usuario_id)

        item = db.query(CarritoItemModel).filter(
            CarritoItemModel.carritoid == carrito.id,
            CarritoItemModel.varianteid == variante_id
        ).first()

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El ítem no está en el carrito")

        if datos.cantidad <= 0:
            db.delete(item)
        else:
            # Validar stock
            if carrito.sucursalid:
                inv = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == variante_id,
                    InventarioSucursalModel.sucursalid == carrito.sucursalid
                ).first()
                stock_disp = max(0, (inv.cantidad - inv.stockreservado)) if inv else 0
            else:
                invs = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == variante_id
                ).all()
                stock_disp = sum(max(0, (i.cantidad - i.stockreservado)) for i in invs)

            if datos.cantidad > stock_disp:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No puedes agregar {datos.cantidad} unidades. Stock disponible: {stock_disp} uds."
                )

            item.cantidad = datos.cantidad

        carrito.fechaactualizacion = datetime.utcnow()
        db.commit()

        return cls.obtener_carrito_dto(db, usuario_id)

    @classmethod
    def eliminar_item(cls, db: Session, usuario_id: int, variante_id: int) -> CarritoResponse:
        """Elimina una prenda del carrito"""
        carrito = cls._obtener_carrito_activo(db, usuario_id)

        item = db.query(CarritoItemModel).filter(
            CarritoItemModel.carritoid == carrito.id,
            CarritoItemModel.varianteid == variante_id
        ).first()

        if item:
            db.delete(item)
            carrito.fechaactualizacion = datetime.utcnow()
            db.commit()

        return cls.obtener_carrito_dto(db, usuario_id)

    @classmethod
    def asignar_sucursal(cls, db: Session, usuario_id: int, datos: AsignarSucursalCarritoRequest) -> CarritoResponse:
        """Asigna o cambia la tienda física donde se retirará/comprará el carrito"""
        sucursal = db.query(SucursalModel).filter(
            SucursalModel.id == datos.sucursal_id,
            SucursalModel.activo == True
        ).first()

        if not sucursal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada o inactiva")

        carrito = cls._obtener_carrito_activo(db, usuario_id)
        carrito.sucursalid = datos.sucursal_id
        carrito.fechaactualizacion = datetime.utcnow()
        db.commit()

        return cls.obtener_carrito_dto(db, usuario_id)

    @classmethod
    def vaciar_carrito(cls, db: Session, usuario_id: int) -> CarritoResponse:
        """Elimina todos los productos del carrito"""
        carrito = cls._obtener_carrito_activo(db, usuario_id)

        db.query(CarritoItemModel).filter(CarritoItemModel.carritoid == carrito.id).delete()
        carrito.fechaactualizacion = datetime.utcnow()
        db.commit()

        return cls.obtener_carrito_dto(db, usuario_id)
