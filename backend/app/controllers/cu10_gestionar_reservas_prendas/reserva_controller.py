# ==============================================================================
# CU10 - GESTIONAR RESERVAS DE PRENDAS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu10_gestionar_reservas_prendas/reserva_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
import random
import string

from app.models.models import (
    ReservaModel,
    ReservaDetalleModel,
    CarritoModel,
    CarritoItemModel,
    InventarioSucursalModel,
    SucursalModel,
    VarianteProductoModel,
    UsuarioModel,
)
from app.schemas.reserva_schema import (
    ReservaCreate,
    ReservaResponse,
    ReservaDetalleResponse,
    ReservaSucursalResponse,
)


def generar_codigo_reserva(db: Session) -> str:
    """Genera un código único alfanumérico para la reserva (ej: RES-7X9K2M)."""
    while True:
        sufijo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        codigo = f"RES-{sufijo}"
        existente = db.query(ReservaModel).filter(ReservaModel.codigoreserva == codigo).first()
        if not existente:
            return codigo


def formatear_reserva(reserva: ReservaModel) -> ReservaResponse:
    """Convierte un modelo de SQLAlchemy ReservaModel a un schema Pydantic enriquecido."""
    sucursal_resp = None
    if reserva.sucursal:
        sucursal_resp = ReservaSucursalResponse(
            id=reserva.sucursal.id,
            nombre=reserva.sucursal.nombre,
            ciudad=reserva.sucursal.ciudad,
            direccion=reserva.sucursal.direccion,
            telefono=reserva.sucursal.telefono,
        )

    # Datos del Cliente
    cliente_nombre = None
    cliente_email = None
    cliente_tel = None
    if reserva.cliente:
        cliente_nombre = f"{reserva.cliente.nombre} {reserva.cliente.apellido or ''}".strip()
        cliente_email = reserva.cliente.email
        cliente_tel = reserva.cliente.telefono

    detalles_resp: List[ReservaDetalleResponse] = []
    total_items = 0
    total_estimado = 0.0

    for d in reserva.detalles:
        variante = d.variante
        prod = variante.producto if variante else None

        prod_nombre = prod.nombre if prod else "Prenda"
        talla_nombre = variante.talla.nombre if variante and variante.talla else None
        color_nombre = variante.color.nombre if variante and variante.color else None
        color_hex = variante.color.codigohex if variante and variante.color else None
        imagen_url = (variante.imagenurl if variante and variante.imagenurl else None) or (prod.imagenprincipal if prod else None)

        precio = float(variante.precioventa if variante and variante.precioventa else (prod.preciobase if prod else 0.0))
        subtotal = round(precio * d.cantidad, 2)

        detalles_resp.append(
            ReservaDetalleResponse(
                variante_id=d.varianteid,
                producto_nombre=prod_nombre,
                talla=talla_nombre,
                color=color_nombre,
                codigo_hex=color_hex,
                imagen_url=imagen_url,
                precio_unitario=precio,
                cantidad=d.cantidad,
                subtotal=subtotal,
            )
        )
        total_items += d.cantidad
        total_estimado += subtotal

    return ReservaResponse(
        id=reserva.id,
        codigo_reserva=reserva.codigoreserva,
        fecha_reserva=reserva.fechareserva,
        estado=reserva.estado,
        observaciones=reserva.observaciones,
        cliente_id=reserva.clienteid,
        cliente_nombre=cliente_nombre,
        cliente_email=cliente_email,
        cliente_telefono=cliente_tel,
        sucursal=sucursal_resp,
        detalles=detalles_resp,
        total_items=total_items,
        total_estimado=round(total_estimado, 2),
    )


class ReservaController:

    @staticmethod
    def crear_reserva_desde_carrito(db: Session, usuario_id: int, datos: ReservaCreate) -> ReservaResponse:
        """
        CU10: Convierte el carrito activo del cliente en una Reserva física con código único.
        Reserva el stock físico incrementando 'stockreservado' en inventario_sucursal.
        """
        # 1. Obtener carrito activo del usuario
        carrito = (
            db.query(CarritoModel)
            .filter(CarritoModel.clienteid == usuario_id, CarritoModel.estado == "ACTIVO")
            .first()
        )

        if not carrito or not carrito.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El carrito está vacío. Agregue prendas al carrito antes de generar una reserva.",
            )

        # 2. Determinar la sucursal física
        sucursal_id = datos.sucursal_id or carrito.sucursalid
        if not sucursal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe seleccionar la sucursal física donde retirará sus prendas reservadas.",
            )

        sucursal = db.query(SucursalModel).filter(SucursalModel.id == sucursal_id, SucursalModel.activo == True).first()
        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La sucursal con ID {sucursal_id} no existe o no se encuentra activa.",
            )

        # 3. Validar disponibilidad de stock en la sucursal seleccionada
        # El stock disponible para reservar es: stock_fisico - stock_reservado
        inventarios_afectados = []
        for item in carrito.items:
            inv = (
                db.query(InventarioSucursalModel)
                .filter(
                    InventarioSucursalModel.varianteid == item.varianteid,
                    InventarioSucursalModel.sucursalid == sucursal_id,
                )
                .first()
            )

            stock_fisico = inv.cantidad if inv else 0
            stock_apartado = inv.stockreservado if inv else 0
            stock_disponible = max(0, stock_fisico - stock_apartado)

            nombre_prenda = (
                item.variante.producto.nombre if item.variante and item.variante.producto else f"Variante #{item.varianteid}"
            )

            if stock_disponible < item.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Stock insuficiente en la sucursal '{sucursal.nombre}' para la prenda '{nombre_prenda}'. "
                        f"Disponibles para reserva: {stock_disponible}, solicitadas: {item.cantidad}."
                    ),
                )
            inventarios_afectados.append((inv, item.cantidad))

        # 4. Crear código único de reserva
        codigo = generar_codigo_reserva(db)

        # 5. Crear la cabecera de la Reserva
        nueva_reserva = ReservaModel(
            codigoreserva=codigo,
            fechareserva=datetime.utcnow(),
            estado="PENDIENTE",
            observaciones=datos.observaciones,
            sucursalid=sucursal_id,
            clienteid=usuario_id,
        )
        db.add(nueva_reserva)
        db.flush()  # Para obtener nueva_reserva.id

        # 6. Crear los detalles de la Reserva e incrementar el stockreservado
        for inv, cantidad_item in inventarios_afectados:
            detalle = ReservaDetalleModel(
                varianteid=inv.varianteid,
                reservaid=nueva_reserva.id,
                cantidad=cantidad_item,
            )
            db.add(detalle)

            # Incrementar el stock reservado en la sucursal
            inv.stockreservado += cantidad_item

        # 7. Marcar carrito actual como CONVERTIDO
        carrito.estado = "CONVERTIDO"

        db.commit()
        db.refresh(nueva_reserva)

        return formatear_reserva(nueva_reserva)

    @staticmethod
    def listar_reservas_usuario(db: Session, usuario_id: int) -> List[ReservaResponse]:
        """Obtiene todas las reservas del usuario ordenadas de más reciente a más antigua."""
        reservas = (
            db.query(ReservaModel)
            .filter(ReservaModel.clienteid == usuario_id)
            .order_by(ReservaModel.fechareserva.desc())
            .all()
        )
        return [formatear_reserva(r) for r in reservas]

    @staticmethod
    def obtener_reserva_por_id_o_codigo(db: Session, id_o_codigo: str, usuario_id: Optional[int] = None) -> ReservaResponse:
        """Consulta el detalle de una reserva por su ID o por su código alfanumérico."""
        query = db.query(ReservaModel)
        if id_o_codigo.isdigit():
            query = query.filter((ReservaModel.id == int(id_o_codigo)) | (ReservaModel.codigoreserva == id_o_codigo))
        else:
            query = query.filter(ReservaModel.codigoreserva == id_o_codigo.upper())

        reserva = query.first()
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró ninguna reserva con identificador '{id_o_codigo}'.",
            )

        if usuario_id and reserva.clienteid != usuario_id:
            # Si se valida por usuario y no le pertenece
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta reserva.",
            )

        return formatear_reserva(reserva)

    @staticmethod
    def cancelar_reserva_cliente(db: Session, reserva_id: int, usuario_id: int, motivo: Optional[str] = None) -> ReservaResponse:
        """
        Permite al cliente cancelar una reserva que aún esté en estado PENDIENTE.
        Libera el stockreservado en inventario_sucursal.
        """
        reserva = (
            db.query(ReservaModel)
            .filter(ReservaModel.id == reserva_id, ReservaModel.clienteid == usuario_id)
            .first()
        )
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada.",
            )

        if reserva.estado != "PENDIENTE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cancelar una reserva con estado '{reserva.estado}'. Solo se pueden cancelar reservas PENDIENTES.",
            )

        # Liberar stock reservado en la sucursal
        for d in reserva.detalles:
            inv = (
                db.query(InventarioSucursalModel)
                .filter(
                    InventarioSucursalModel.varianteid == d.varianteid,
                    InventarioSucursalModel.sucursalid == reserva.sucursalid,
                )
                .first()
            )
            if inv:
                inv.stockreservado = max(0, inv.stockreservado - d.cantidad)

        reserva.estado = "CANCELADA"
        if motivo:
            nota = f"[Cancelada por cliente: {motivo}]"
            reserva.observaciones = f"{reserva.observaciones or ''} {nota}".strip()

        db.commit()
        db.refresh(reserva)
        return formatear_reserva(reserva)
