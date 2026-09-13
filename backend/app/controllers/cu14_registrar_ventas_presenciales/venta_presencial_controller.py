# ==============================================================================
# CU14 - REGISTRAR VENTAS PRESENCIALES -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu14_registrar_ventas_presenciales/venta_presencial_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime
import random

from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    VentaModel, DetalleVentaModel, MetodoPagoModel, PagoModel, ReciboModel
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
from app.schemas.orden_schema import VentaPresencialCreate


class VentaPresencialController:

    @staticmethod
    def _asegurar_metodos_pago(db: Session):
        count = db.query(MetodoPagoModel).count()
        if count == 0:
            metodos_defecto = [
                MetodoPagoModel(nombre="Efectivo", estado=True),
                MetodoPagoModel(nombre="Tarjeta de Débito / Crédito", estado=True),
                MetodoPagoModel(nombre="QR / Transferencia Bancaria", estado=True),
                MetodoPagoModel(nombre="Pago Digital / Online", estado=True),
            ]
            db.add_all(metodos_defecto)
            db.commit()

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

        sku = f"TSH-{producto.id}-{color.id}-{talla.id}"
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
    def registrar_venta_presencial(
        db: Session,
        current_user: UsuarioModel,
        data: VentaPresencialCreate
    ) -> Dict:
        if not data.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debe ingresar al menos un producto en la venta")

        VentaPresencialController._asegurar_metodos_pago(db)

        # 1. Sucursal
        sucursal = db.query(SucursalModel).filter(SucursalModel.id == data.sucursal_id).first()
        if not sucursal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")

        # 2. Cliente (o Consumidor Final)
        cliente = None
        if data.cliente_id:
            cliente = db.query(ClienteModel).filter(ClienteModel.id == data.cliente_id).first()

        if not cliente:
            cliente = db.query(ClienteModel).filter(ClienteModel.nombre.ilike("Consumidor Final")).first()
            if not cliente:
                cliente = ClienteModel(
                    nombre=data.cliente_nombre or "Consumidor Final",
                    apellido="",
                    email=f"consumidor_{random.randint(1000, 9999)}@boutique.com",
                    telefono="",
                    usuarioid=current_user.id,
                    activo=True
                )
                db.add(cliente)
                db.flush()

        # 3. Método de pago
        metodo_pago = db.query(MetodoPagoModel).filter(MetodoPagoModel.id == data.metodo_pago_id).first()
        if not metodo_pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Método de pago no válido")

        # 4. Validar stock y armar detalles
        total_acumulado = Decimal("0.00")
        items_a_procesar = []

        for item in data.items:
            prod = db.query(ProductoModel).filter(ProductoModel.id == item.producto_id).first()
            if not prod:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {item.producto_id} no encontrado")

            variante = VentaPresencialController._obtener_o_crear_variante(db, prod, item.variante_id)

            inv = db.query(InventarioModel).filter(
                InventarioModel.sucursalid == sucursal.id,
                InventarioModel.varianteid == variante.id
            ).first()

            if not inv or inv.stockfisico < item.cantidad:
                stock_disp = inv.stockfisico if inv else 0
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para '{prod.nombre}'. Disponible en {sucursal.nombre}: {stock_disp}, Solicitado: {item.cantidad}"
                )

            precio_unit = Decimal(str(variante.precioventa or prod.preciobase))
            subtotal = precio_unit * Decimal(item.cantidad)
            total_acumulado += subtotal

            items_a_procesar.append({
                "variante": variante,
                "cantidad": item.cantidad,
                "precio_unitario": precio_unit,
                "subtotal": subtotal,
                "inv": inv
            })

        # 5. Generar venta presencial
        ahora = datetime.utcnow()
        codigo_venta = f"POS-{ahora.strftime('%Y%m%d%H%M')}-{random.randint(100, 999)}"

        nueva_venta = VentaModel(
            codigoventa=codigo_venta,
            tipoventa="Presencial",
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

        # 6. Guardar renglones y descontar stock
        for it in items_a_procesar:
            det = DetalleVentaModel(
                ventaid=nueva_venta.id,
                varianteid=it["variante"].id,
                cantidad=it["cantidad"],
                preciounitario=it["precio_unitario"],
                descuento=Decimal("0.00"),
                subtotal=it["subtotal"]
            )
            db.add(det)

            VentaPresencialController._descontar_stock_y_registrar_kardex(
                db=db,
                sucursal_id=sucursal.id,
                variante_id=it["variante"].id,
                cantidad=it["cantidad"],
                tipo_mov="Venta Presencial",
                referencia=codigo_venta,
                usuario_id=current_user.id
            )

        # 7. Registrar pago
        pago = PagoModel(
            monto=total_acumulado,
            estado="Aprobado",
            referencia=f"CAJA-{codigo_venta}",
            fecha=ahora,
            ventaid=nueva_venta.id,
            metodoid=metodo_pago.id
        )
        db.add(pago)

        db.commit()
        db.refresh(nueva_venta)

        cambio = Decimal("0.00")
        if data.monto_recibido and data.monto_recibido > total_acumulado:
            cambio = data.monto_recibido - total_acumulado

        return {
            "id": nueva_venta.id,
            "codigoventa": nueva_venta.codigoventa,
            "tipoventa": nueva_venta.tipoventa,
            "estado": nueva_venta.estado,
            "subtotal": nueva_venta.subtotal,
            "descuento": nueva_venta.descuento,
            "total": nueva_venta.total,
            "fecha": nueva_venta.fecha,
            "sucursalid": sucursal.id,
            "sucursal_nombre": sucursal.nombre,
            "cliente_nombre": cliente.nombre,
            "metodo_pago_nombre": metodo_pago.nombre,
            "cambio": cambio
        }

    @staticmethod
    def listar_metodos_pago(db: Session) -> List[MetodoPagoModel]:
        VentaPresencialController._asegurar_metodos_pago(db)
        return db.query(MetodoPagoModel).filter(MetodoPagoModel.estado == True).all()

    @staticmethod
    def listar_todas_ventas(
        db: Session,
        tipoventa: Optional[str] = None,
        sucursal_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        query = db.query(VentaModel)

        if tipoventa:
            query = query.filter(VentaModel.tipoventa.ilike(f"%{tipoventa}%"))

        if sucursal_id:
            query = query.filter(VentaModel.sucursalid == sucursal_id)

        ventas = query.order_by(VentaModel.id.desc()).offset(skip).limit(limit).all()

        resultado = []
        for v in ventas:
            metodo_nombre = None
            if v.pagos and len(v.pagos) > 0:
                metodo_nombre = v.pagos[0].metodo.nombre if v.pagos[0].metodo else None

            resultado.append({
                "id": v.id,
                "codigoventa": v.codigoventa,
                "tipoventa": v.tipoventa,
                "estado": v.estado,
                "subtotal": v.subtotal,
                "descuento": v.descuento,
                "total": v.total,
                "fecha": v.fecha,
                "sucursalid": v.sucursalid,
                "sucursal_nombre": v.sucursal.nombre if v.sucursal else "Sucursal Central",
                "cliente_nombre": f"{v.cliente.nombre} {v.cliente.apellido or ''}".strip() if v.cliente else "Consumidor Final",
                "metodo_pago_nombre": metodo_nombre or "Efectivo",
                "cambio": Decimal("0.00")
            })

        return resultado

    @staticmethod
    def obtener_venta_por_id(db: Session, venta_id: int) -> Dict:
        v = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
        if not v:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        metodo_nombre = None
        if v.pagos and len(v.pagos) > 0:
            metodo_nombre = v.pagos[0].metodo.nombre if v.pagos[0].metodo else None

        detalles_lista = []
        for d in v.detalles:
            prod_nombre = "Producto"
            talla_nombre = "-"
            color_nombre = "-"
            if d.variante:
                if d.variante.producto:
                    prod_nombre = d.variante.producto.nombre
                if d.variante.talla:
                    talla_nombre = d.variante.talla.nombre
                if d.variante.color:
                    color_nombre = d.variante.color.nombre

            detalles_lista.append({
                "variante_id": d.varianteid,
                "producto_nombre": prod_nombre,
                "talla": talla_nombre,
                "color": color_nombre,
                "cantidad": d.cantidad,
                "preciounitario": d.preciounitario,
                "descuento": d.descuento,
                "subtotal": d.subtotal
            })

        return {
            "id": v.id,
            "codigoventa": v.codigoventa,
            "tipoventa": v.tipoventa,
            "estado": v.estado,
            "subtotal": v.subtotal,
            "descuento": v.descuento,
            "total": v.total,
            "fecha": v.fecha,
            "sucursalid": v.sucursalid,
            "sucursal_nombre": v.sucursal.nombre if v.sucursal else "Sucursal Central",
            "cliente_nombre": f"{v.cliente.nombre} {v.cliente.apellido or ''}".strip() if v.cliente else "Consumidor Final",
            "metodo_pago_nombre": metodo_nombre or "Efectivo",
            "cambio": Decimal("0.00"),
            "detalles": detalles_lista
        }
