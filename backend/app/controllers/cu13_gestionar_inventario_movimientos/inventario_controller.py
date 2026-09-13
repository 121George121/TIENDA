# ==============================================================================
# CU13 - GESTIONAR INVENTARIO Y MOVIMIENTOS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu13_gestionar_inventario_movimientos/inventario_controller.py
# ==============================================================================

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.models import (
    UsuarioModel,
    InventarioModel,
    MovimientoInventarioModel,
    SucursalModel,
    ProductoModel,
    ColorModel,
    TallaModel,
    VarianteProductoModel
)
from app.schemas.inventario_schema import MovimientoInventarioCreate, StockMinimoUpdate


class InventarioController:

    @staticmethod
    def _asegurar_variantes_e_inventario(db: Session):
        """
        Garantiza que todos los productos registrados tengan al menos una variante y fila en
        la tabla inventario para cada sucursal activa, sin alterar la base de datos PostgreSQL.
        """
        sucursales = db.query(SucursalModel).filter(SucursalModel.activo == True).all()
        if not sucursales:
            return

        productos = db.query(ProductoModel).filter(ProductoModel.activo == True).all()
        color_default = db.query(ColorModel).first()
        if not color_default:
            color_default = ColorModel(nombre="Estándar", codigohex="#111827", activo=True)
            db.add(color_default)
            db.flush()

        talla_default = db.query(TallaModel).first()
        if not talla_default:
            talla_default = TallaModel(nombre="Única (M)", grupoedad="Adultos", orden=1, activo=True)
            db.add(talla_default)
            db.flush()

        for p in productos:
            variante = db.query(VarianteProductoModel).filter(
                VarianteProductoModel.productoid == p.id,
                VarianteProductoModel.activo == True
            ).first()

            if not variante:
                variante = VarianteProductoModel(
                    productoid=p.id,
                    colorid=color_default.id,
                    tallaid=talla_default.id,
                    sku=f"POL-{p.id}-{color_default.id}-{talla_default.id}",
                    precioventa=p.preciobase,
                    activo=True
                )
                db.add(variante)
                db.flush()

            # Asegurar inventario en cada sucursal activa
            for suc in sucursales:
                inv = db.query(InventarioModel).filter(
                    InventarioModel.sucursalid == suc.id,
                    InventarioModel.varianteid == variante.id
                ).first()

                if not inv:
                    inv = InventarioModel(
                        sucursalid=suc.id,
                        varianteid=variante.id,
                        stockfisico=20, # Stock inicial de cortesía
                        stockreservado=0,
                        stockminimo=5
                    )
                    db.add(inv)
                    db.flush()

        db.commit()

    @staticmethod
    def listar_inventario(
        db: Session,
        sucursal_id: Optional[int] = None,
        search: Optional[str] = None,
        solo_bajo_stock: Optional[bool] = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        InventarioController._asegurar_variantes_e_inventario(db)

        query = db.query(InventarioModel).join(SucursalModel).join(VarianteProductoModel).join(ProductoModel)

        if sucursal_id:
            query = query.filter(InventarioModel.sucursalid == sucursal_id)

        if search:
            patron = f"%{search}%"
            query = query.filter(
                or_(
                    ProductoModel.nombre.ilike(patron),
                    ProductoModel.marca.ilike(patron),
                    VarianteProductoModel.sku.ilike(patron),
                    SucursalModel.nombre.ilike(patron)
                )
            )

        if solo_bajo_stock:
            query = query.filter(InventarioModel.stockfisico <= InventarioModel.stockminimo)

        items = query.order_by(InventarioModel.id.desc()).offset(skip).limit(limit).all()

        resultado = []
        for inv in items:
            p = inv.variante.producto
            color = inv.variante.color
            talla = inv.variante.talla

            estado_stock = "NORMAL"
            if inv.stockfisico <= 0:
                estado_stock = "AGOTADO"
            elif inv.stockfisico <= inv.stockminimo:
                estado_stock = "BAJO_STOCK"

            resultado.append({
                "id": inv.id,
                "sucursal_id": inv.sucursalid,
                "sucursal_nombre": inv.sucursal.nombre if inv.sucursal else "Sucursal Central",
                "variante_id": inv.varianteid,
                "producto_id": p.id,
                "producto_nombre": p.nombre,
                "producto_marca": p.marca,
                "producto_precio": Decimal(str(inv.variante.precioventa or p.preciobase)),
                "color_nombre": color.nombre if color else "Único",
                "color_hex": color.codigohex if color else "#111827",
                "talla_nombre": talla.nombre if talla else "M",
                "sku": inv.variante.sku or f"SKU-{p.id}",
                "stockfisico": inv.stockfisico,
                "stockreservado": inv.stockreservado,
                "stockminimo": inv.stockminimo,
                "estado_stock": estado_stock,
                "fechaactualizacion": inv.fechaactualizacion
            })

        return resultado

    @staticmethod
    def registrar_movimiento(
        db: Session,
        current_user: UsuarioModel,
        inventario_id: int,
        data: MovimientoInventarioCreate
    ) -> Dict:
        inv = db.query(InventarioModel).filter(InventarioModel.id == inventario_id).first()
        if not inv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de inventario no encontrado")

        tipo = data.tipomovimiento.strip().capitalize()
        cant = data.cantidad

        if tipo == "Entrada":
            inv.stockfisico += cant
        elif tipo == "Salida":
            if inv.stockfisico < cant:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente. Stock actual: {inv.stockfisico}, cantidad a retirar: {cant}"
                )
            inv.stockfisico -= cant
        elif tipo == "Ajuste":
            inv.stockfisico = cant
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de movimiento inválido. Use 'Entrada', 'Salida' o 'Ajuste'."
            )

        inv.fechaactualizacion = datetime.utcnow()

        movimiento = MovimientoInventarioModel(
            tipomovimiento=tipo,
            cantidad=cant,
            motivo=data.motivo or f"Operación manual de {tipo}",
            referencia=data.referencia,
            fecha=datetime.utcnow(),
            inventarioid=inv.id,
            usuarioid=current_user.id
        )
        db.add(movimiento)
        db.commit()
        db.refresh(inv)

        return {
            "mensaje": f"Movimiento de {tipo} registrado exitosamente",
            "stock_actual": inv.stockfisico,
            "inventario_id": inv.id
        }

    @staticmethod
    def actualizar_stock_minimo(db: Session, inventario_id: int, data: StockMinimoUpdate) -> Dict:
        inv = db.query(InventarioModel).filter(InventarioModel.id == inventario_id).first()
        if not inv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de inventario no encontrado")

        inv.stockminimo = data.stockminimo
        inv.fechaactualizacion = datetime.utcnow()
        db.commit()
        db.refresh(inv)

        return {"mensaje": "Nivel de stock mínimo actualizado", "stockminimo": inv.stockminimo}

    @staticmethod
    def obtener_kardex(db: Session, inventario_id: int, limit: int = 50) -> List[Dict]:
        inv = db.query(InventarioModel).filter(InventarioModel.id == inventario_id).first()
        if not inv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de inventario no encontrado")

        movimientos = db.query(MovimientoInventarioModel).filter(
            MovimientoInventarioModel.inventarioid == inventario_id
        ).order_by(MovimientoInventarioModel.id.desc()).limit(limit).all()

        resultado = []
        for m in movimientos:
            resultado.append({
                "id": m.id,
                "tipomovimiento": m.tipomovimiento,
                "cantidad": m.cantidad,
                "motivo": m.motivo,
                "referencia": m.referencia,
                "fecha": m.fecha,
                "usuario_nombre": f"{m.usuario.nombre} {m.usuario.apellido or ''}".strip() if m.usuario else "Sistema"
            })
        return resultado
