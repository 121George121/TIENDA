# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Contiene la Lógica de Negocio para la creación y gestión de Órdenes / Pedidos
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import OrdenModel, OrdenDetalleModel, ProductoModel
from app.schemas.schemas import OrdenCreate
from fastapi import HTTPException, status

class OrderController:

    @staticmethod
    def create_order(db: Session, usuario_id: int, orden_data: OrdenCreate):
        """Procesa y crea un pedido calculando el total y verificando stock"""
        total_acumulado = 0.0
        detalles_a_crear = []

        # 1. Verificar existencia y stock de cada producto
        for item in orden_data.items:
            producto = db.query(ProductoModel).filter(ProductoModel.id == item.producto_id, ProductoModel.activo == True).first()
            if not producto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto ID {item.producto_id} no existe")
            
            if producto.stock < item.cantidad:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")

            # Descontar stock
            producto.stock -= item.cantidad
            subtotal = float(producto.precio) * item.cantidad
            total_acumulado += subtotal

            detalles_a_crear.append({
                "producto_id": producto.id,
                "cantidad": item.cantidad,
                "precio_unitario": producto.precio,
                "subtotal": subtotal
            })

        # 2. Crear cabecera de orden
        nueva_orden = OrdenModel(
            usuario_id=usuario_id,
            total=total_acumulado,
            estado="PAGADO",
            direccion_envio=orden_data.direccion_envio
        )
        db.add(nueva_orden)
        db.flush() # Genera el ID de la orden sin hacer commit completo todavía

        # 3. Crear los detalles de la orden
        for d in detalles_a_crear:
            detalle = OrdenDetalleModel(
                orden_id=nueva_orden.id,
                producto_id=d["producto_id"],
                cantidad=d["cantidad"],
                precio_unitario=d["precio_unitario"],
                subtotal=d["subtotal"]
            )
            db.add(detalle)

        db.commit()
        db.refresh(nueva_orden)
        return nueva_orden

    @staticmethod
    def get_user_orders(db: Session, usuario_id: int):
        """Obtiene las órdenes realizadas por un usuario específico"""
        return db.query(OrdenModel).filter(OrdenModel.usuario_id == usuario_id).all()
