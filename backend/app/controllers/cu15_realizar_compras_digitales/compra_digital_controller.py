# ==============================================================================
# CU15 - REALIZAR COMPRAS DIGITALES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu15_realizar_compras_digitales/compra_digital_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime
import random

from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    VentaModel, DetalleVentaModel, MetodoPagoModel, PagoModel
)
from app.models.cu15_realizar_compras_digitales.compra_digital_model import (
    CarritoModel, CarritoItemModel
)
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import (
    InventarioModel, MovimientoInventarioModel
)
from app.models.cu5_gestionar_productos.producto_model import (
    ProductoModel, VarianteProductoModel, ColorModel, TallaModel
)
from app.models.cu4_gestionar_sucursales.sucursal_model import SucursalModel
from app.models.cu3_gestionar_clientes.cliente_model import ClienteModel
from app.models.cu1_gestionar_autenticacion.usuario_rol_model import UsuarioModel
from app.schemas.orden_schema import OrdenCreate


class CompraDigitalController:

    @staticmethod
    def _obtener_o_crear_variante(db: Session, producto: ProductoModel, variante_id: Optional[int] = None) -> VarianteProductoModel:
        if variante_id:
            variante = db.query(VarianteProductoModel).filter(
                VarianteProductoModel.id == variante_id,
                VarianteProductoModel.productoid == producto.id
            ).first()
            if variante:
                return variante

        variante = db.query(VarianteProductoModel).filter(VarianteProductoModel.productoid == producto.id).first()
        if variante:
            return variante

        color = db.query(ColorModel).first()
        if not color:
            color = ColorModel(nombre="Negro", codigohex="#000000")
            db.add(color)
            db.flush()

        talla = db.query(TallaModel).first()
        if not talla:
            talla = TallaModel(nombre="M", descripcion="Talla Mediana")
            db.add(talla)
            db.flush()

        sku = f"DIG-{producto.id}-{color.id}-{talla.id}"
        nueva_variante = VarianteProductoModel(
            sku=sku,
            productoid=producto.id,
            colorid=color.id,
            tallaid=talla.id,
            precioventa=producto.preciobase,
            activo=True
        )
        db.add(nueva_variante)
        db.flush()
        return nueva_variante

    @staticmethod
    def _descontar_stock_y_registrar_kardex(
        db: Session,
        sucursal_id: int,
        variante_id: int,
        cantidad: int,
        tipo_mov: str,
        referencia: str,
        usuario_id: int
    ):
        inv = db.query(InventarioModel).filter(
            InventarioModel.sucursalid == sucursal_id,
            InventarioModel.varianteid == variante_id
        ).first()

        if not inv:
            inv = InventarioModel(
                sucursalid=sucursal_id,
                varianteid=variante_id,
                stockfisico=100,
                stockreservado=0,
                stockminimo=10,
                fechaactualizacion=datetime.utcnow()
            )
            db.add(inv)
            db.flush()

        inv.stockfisico = max(0, inv.stockfisico - cantidad)
        inv.fechaactualizacion = datetime.utcnow()

        kardex = MovimientoInventarioModel(
            tipomovimiento=tipo_mov,
            cantidad=-cantidad,
            motivo=f"Descuento automático por {tipo_mov} ({referencia})",
            referencia=referencia,
            fecha=datetime.utcnow(),
            inventarioid=inv.id,
            usuarioid=usuario_id
        )
        db.add(kardex)

    @staticmethod
    def procesar_orden_digital(
        db: Session,
        current_user: UsuarioModel,
        data: OrdenCreate
    ) -> VentaModel:
        if not data.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La orden debe contener al menos un producto."
            )

        # 1. Cliente asociado
        cliente = db.query(ClienteModel).filter(ClienteModel.usuarioid == current_user.id).first()
        if not cliente:
            cliente = ClienteModel(
                nombre=current_user.nombre,
                apellido=current_user.apellido or "",
                email=current_user.email,
                telefono="",
                usuarioid=current_user.id,
                activo=True
            )
            db.add(cliente)
            db.flush()

        # 2. Sucursal de despacho
        sucursal = None
        if data.sucursal_id:
            sucursal = db.query(SucursalModel).filter(SucursalModel.id == data.sucursal_id, SucursalModel.activo == True).first()
        if not sucursal:
            sucursal = db.query(SucursalModel).filter(SucursalModel.activo == True).first()
        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay sucursales activas registradas para procesar la orden."
            )

        # 3. Items y totales
        total_acumulado = Decimal("0.00")
        items_a_insertar = []

        for item in data.items:
            producto = db.query(ProductoModel).filter(ProductoModel.id == item.producto_id).first()
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {item.producto_id} no encontrado en el catálogo."
                )

            variante = CompraDigitalController._obtener_o_crear_variante(db, producto, item.variante_id)
            precio_unitario = Decimal(str(variante.precioventa or producto.preciobase))
            subtotal_item = precio_unitario * Decimal(item.cantidad)
            total_acumulado += subtotal_item

            items_a_insertar.append({
                "variante": variante,
                "cantidad": item.cantidad,
                "precio_unitario": precio_unitario,
                "subtotal": subtotal_item
            })

        # 4. Crear venta digital
        ahora = datetime.utcnow()
        codigo_venta = f"ORD-{ahora.strftime('%Y%m%d%H%M')}-{random.randint(100, 999)}"

        nueva_venta = VentaModel(
            codigoventa=codigo_venta,
            tipoventa="Digital",
            estado="Completada",
            subtotal=total_acumulado,
            descuento=Decimal("0.00"),
            total=total_acumulado,
            fecha=ahora,
            sucursalid=sucursal.id,
            clienteid=cliente.id,
            usuarioid=current_user.id
        )
        db.add(nueva_venta)
        db.flush()

        # 5. Insertar renglones y descontar stock
        for item_data in items_a_insertar:
            detalle = DetalleVentaModel(
                ventaid=nueva_venta.id,
                varianteid=item_data["variante"].id,
                cantidad=item_data["cantidad"],
                preciounitario=item_data["precio_unitario"],
                descuento=Decimal("0.00"),
                subtotal=item_data["subtotal"]
            )
            db.add(detalle)

            CompraDigitalController._descontar_stock_y_registrar_kardex(
                db=db,
                sucursal_id=sucursal.id,
                variante_id=item_data["variante"].id,
                cantidad=item_data["cantidad"],
                tipo_mov="Venta Digital",
                referencia=codigo_venta,
                usuario_id=current_user.id
            )

        # 6. Registrar pago
        metodo_digital = None
        if data.metodo_id:
            metodo_digital = db.query(MetodoPagoModel).filter(MetodoPagoModel.id == data.metodo_id).first()
        if not metodo_digital:
            metodo_digital = db.query(MetodoPagoModel).filter(MetodoPagoModel.nombre.ilike("%Digital%")).first()
        if not metodo_digital:
            metodo_digital = db.query(MetodoPagoModel).first()

        if metodo_digital:
            pago = PagoModel(
                monto=total_acumulado,
                estado="Aprobado",
                referencia=f"PAY-{codigo_venta}",
                fecha=ahora,
                ventaid=nueva_venta.id,
                metodoid=metodo_digital.id
            )
            db.add(pago)

        db.commit()
        db.refresh(nueva_venta)
        return nueva_venta

    @staticmethod
    def listar_mis_ordenes(db: Session, current_user: UsuarioModel) -> List[Dict]:
        ventas = db.query(VentaModel).filter(
            VentaModel.usuarioid == current_user.id
        ).order_by(VentaModel.id.desc()).all()

        res = []
        for v in ventas:
            res.append({
                "id": v.id,
                "codigoventa": v.codigoventa,
                "estado": v.estado,
                "tipoventa": v.tipoventa,
                "subtotal": v.subtotal,
                "descuento": v.descuento,
                "total": v.total,
                "fecha": v.fecha,
                "mensaje": "Orden procesada exitosamente"
            })
        return res
