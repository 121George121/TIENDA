# ==============================================================================
# CU08 - CONSULTAR CATÁLOGO Y DISPONIBILIDAD -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu8_consultar_catalogo_disponibilidad/inventario_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from fastapi import HTTPException, status

from app.models.models import (
    ProductoModel, VarianteProductoModel, SucursalModel,
    InventarioSucursalModel, CategoriaModel, ColorModel, TallaModel
)
from app.schemas.inventario_schema import (
    ProductoCatalogoItem, DisponibilidadVarianteResponse,
    DisponibilidadProductoResponse, DisponibilidadSucursalDetalle,
    ActualizarStockRequest
)

class InventarioController:

    @staticmethod
    def listar_catalogo(
        db: Session,
        sucursal_id: Optional[int] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        search: Optional[str] = None,
        solo_disponibles: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductoCatalogoItem]:
        """Obtiene el catálogo de productos con stock en tiempo real por sucursal"""

        query = db.query(ProductoModel).filter(ProductoModel.activo == True)

        if categoria_id:
            query = query.filter(ProductoModel.categoriaid == categoria_id)

        if genero:
            query = query.filter(func.lower(ProductoModel.genero) == genero.lower())

        if search:
            search_term = f"%{search.strip().lower()}%"
            query = query.filter(
                or_(
                    func.lower(ProductoModel.nombre).like(search_term),
                    func.lower(ProductoModel.marca).like(search_term),
                    func.lower(ProductoModel.descripcion).like(search_term)
                )
            )

        productos = query.offset(skip).limit(limit).all()
        resultado: List[ProductoCatalogoItem] = []

        for p in productos:
            variantes_resp: List[DisponibilidadVarianteResponse] = []
            stock_sucursal_acumulado = 0
            stock_total_acumulado = 0

            for v in p.variantes:
                if not v.activo:
                    continue

                # Consultar stock de esta variante en todas las sucursales
                inventarios = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == v.id
                ).all()

                stock_total_var = sum(inv.cantidad for inv in inventarios)
                stock_sucursal_var = 0

                if sucursal_id:
                    for inv in inventarios:
                        if inv.sucursalid == sucursal_id:
                            stock_sucursal_var = inv.cantidad
                            break
                else:
                    stock_sucursal_var = stock_total_var

                stock_sucursal_acumulado += stock_sucursal_var
                stock_total_acumulado += stock_total_var

                variantes_resp.append(
                    DisponibilidadVarianteResponse(
                        variante_id=v.id,
                        sku=v.sku,
                        talla=v.talla.nombre if v.talla else None,
                        color=v.color.nombre if v.color else None,
                        codigohex=v.color.codigohex if v.color else None,
                        precio=v.precioventa if v.precioventa is not None else p.preciobase,
                        stock=stock_sucursal_var,
                        disponible=(stock_sucursal_var > 0)
                    )
                )

            # Filtrar si solo se piden disponibles
            if solo_disponibles and stock_sucursal_acumulado <= 0:
                continue

            categoria_nombre = p.categoria.nombre if p.categoria else None

            resultado.append(
                ProductoCatalogoItem(
                    id=p.id,
                    nombre=p.nombre,
                    descripcion=p.descripcion,
                    marca=p.marca,
                    genero=p.genero,
                    preciobase=p.preciobase,
                    imagenprincipal=p.imagenprincipal,
                    categoria_id=p.categoriaid,
                    categoria_nombre=categoria_nombre,
                    stock_sucursal=stock_sucursal_acumulado,
                    stock_total=stock_total_acumulado,
                    disponible=(stock_sucursal_acumulado > 0),
                    variantes=variantes_resp
                )
            )

        return resultado

    @staticmethod
    def obtener_disponibilidad_producto(db: Session, producto_id: int) -> DisponibilidadProductoResponse:
        """Obtiene la disponibilidad de un producto desglosada por cada sucursal física"""
        producto = db.query(ProductoModel).filter(
            ProductoModel.id == producto_id,
            ProductoModel.activo == True
        ).first()

        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        sucursales = db.query(SucursalModel).filter(SucursalModel.activo == True).all()
        sucursales_detalle: List[DisponibilidadSucursalDetalle] = []

        for suc in sucursales:
            variantes_sucursal: List[DisponibilidadVarianteResponse] = []
            stock_total_sucursal = 0

            for v in producto.variantes:
                if not v.activo:
                    continue

                inv = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == v.id,
                    InventarioSucursalModel.sucursalid == suc.id
                ).first()

                stock_cant = inv.cantidad if inv else 0
                stock_total_sucursal += stock_cant

                variantes_sucursal.append(
                    DisponibilidadVarianteResponse(
                        variante_id=v.id,
                        sku=v.sku,
                        talla=v.talla.nombre if v.talla else None,
                        color=v.color.nombre if v.color else None,
                        codigohex=v.color.codigohex if v.color else None,
                        precio=v.precioventa if v.precioventa is not None else producto.preciobase,
                        stock=stock_cant,
                        disponible=(stock_cant > 0)
                    )
                )

            sucursales_detalle.append(
                DisponibilidadSucursalDetalle(
                    sucursal_id=suc.id,
                    sucursal_nombre=suc.nombre,
                    ciudad=suc.ciudad,
                    direccion=suc.direccion,
                    telefono=suc.telefono,
                    stock_total=stock_total_sucursal,
                    variantes=variantes_sucursal
                )
            )

        return DisponibilidadProductoResponse(
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            marca=producto.marca,
            preciobase=producto.preciobase,
            imagenprincipal=producto.imagenprincipal,
            sucursales=sucursales_detalle
        )

    @staticmethod
    def actualizar_stock(db: Session, datos: ActualizarStockRequest) -> dict:
        """Actualiza o registra el stock de una variante en una sucursal"""
        inv = db.query(InventarioSucursalModel).filter(
            InventarioSucursalModel.varianteid == datos.variante_id,
            InventarioSucursalModel.sucursalid == datos.sucursal_id
        ).first()

        if inv:
            inv.cantidad = datos.cantidad
            if datos.stock_minimo is not None:
                inv.stockminimo = datos.stock_minimo
        else:
            inv = InventarioSucursalModel(
                varianteid=datos.variante_id,
                sucursalid=datos.sucursal_id,
                cantidad=datos.cantidad,
                stockminimo=datos.stock_minimo or 5
            )
            db.add(inv)

        db.commit()
        return {
            "mensaje": "Stock actualizado correctamente",
            "variante_id": datos.variante_id,
            "sucursal_id": datos.sucursal_id,
            "cantidad": datos.cantidad
        }
