# ==============================================================================
# CU08 - CONSULTAR CATÁLOGO Y DISPONIBILIDAD -> CAPA SERVICIO (MVC - SERVICE)
# Arquitectura: Multi-Tenant SaaS con Auditoría Bitácora (CU26)
# Ubicación: backend/app/services/cu8_consultar_catalogo_disponibilidad/catalogo_service.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
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
from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController


class CatalogoService:
    """
    Servicio de dominio para la consulta del catálogo y disponibilidad multitienda.
    Implementa aislamiento estricto por tenant, cálculo de stock disponible en tiempo real
    por sucursal física y auditoría de modificaciones de existencias.
    """

    @staticmethod
    def consultar_catalogo(
        db: Session,
        tenant_id: int = 1,
        sucursal_id: Optional[int] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        search: Optional[str] = None,
        solo_disponibles: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductoCatalogoItem]:
        """
        Obtiene el catálogo de productos con stock en tiempo real filtrado por tenant y sucursal.
        """
        query = db.query(ProductoModel).options(
            joinedload(ProductoModel.categoria),
            joinedload(ProductoModel.variantes).joinedload(VarianteProductoModel.color),
            joinedload(ProductoModel.variantes).joinedload(VarianteProductoModel.talla)
        ).filter(
            ProductoModel.activo == True
        )

        if tenant_id is not None:
            query = query.filter(ProductoModel.tenant_id == tenant_id)

        if categoria_id:
            query = query.filter(ProductoModel.categoriaid == categoria_id)

        if genero and genero.strip().upper() != "TODOS":
            query = query.filter(func.lower(ProductoModel.genero) == genero.strip().lower())

        if search:
            search_term = f"%{search.strip().lower()}%"
            query = query.filter(
                or_(
                    func.lower(ProductoModel.nombre).like(search_term),
                    func.lower(ProductoModel.marca).like(search_term),
                    func.lower(ProductoModel.descripcion).like(search_term)
                )
            )

        productos = query.order_by(ProductoModel.id.desc()).offset(skip).limit(limit).all()
        resultado: List[ProductoCatalogoItem] = []

        for p in productos:
            variantes_resp: List[DisponibilidadVarianteResponse] = []
            stock_sucursal_acumulado = 0
            stock_total_acumulado = 0

            for v in p.variantes:
                if not v.activo:
                    continue

                # Consultar stock de esta variante con aislamiento por tenant
                inv_query = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == v.id
                )
                if tenant_id is not None:
                    inv_query = inv_query.filter(InventarioSucursalModel.tenant_id == tenant_id)

                inventarios = inv_query.all()

                stock_total_var = sum(max(0, inv.cantidad - (inv.stockreservado or 0)) for inv in inventarios)
                stock_sucursal_var = 0

                if sucursal_id:
                    for inv in inventarios:
                        if inv.sucursalid == sucursal_id:
                            stock_sucursal_var = max(0, inv.cantidad - (inv.stockreservado or 0))
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

            # Filtrar si solo se piden con existencias
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
    def obtener_disponibilidad_producto(
        db: Session,
        producto_id: int,
        tenant_id: int = 1
    ) -> DisponibilidadProductoResponse:
        """
        Obtiene la disponibilidad de un producto desglosada por cada sucursal física del tenant.
        """
        query = db.query(ProductoModel).options(
            joinedload(ProductoModel.variantes).joinedload(VarianteProductoModel.color),
            joinedload(ProductoModel.variantes).joinedload(VarianteProductoModel.talla)
        ).filter(
            ProductoModel.id == producto_id,
            ProductoModel.activo == True
        )

        if tenant_id is not None:
            query = query.filter(ProductoModel.tenant_id == tenant_id)

        producto = query.first()

        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado o no pertenece a este tenant"
            )

        # Consultar sucursales activas del tenant
        sucursales_query = db.query(SucursalModel).filter(SucursalModel.activo == True)
        if tenant_id is not None:
            sucursales_query = sucursales_query.filter(SucursalModel.tenant_id == tenant_id)
        sucursales = sucursales_query.all()

        sucursales_detalle: List[DisponibilidadSucursalDetalle] = []

        for suc in sucursales:
            variantes_sucursal: List[DisponibilidadVarianteResponse] = []
            stock_total_sucursal = 0

            for v in producto.variantes:
                if not v.activo:
                    continue

                inv_query = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == v.id,
                    InventarioSucursalModel.sucursalid == suc.id
                )
                if tenant_id is not None:
                    inv_query = inv_query.filter(InventarioSucursalModel.tenant_id == tenant_id)

                inv = inv_query.first()

                stock_cant = max(0, inv.cantidad - (inv.stockreservado or 0)) if inv else 0
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
    def listar_sucursales_activas(
        db: Session,
        tenant_id: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Lista las sucursales físicas activas del tenant.
        """
        query = db.query(SucursalModel).filter(SucursalModel.activo == True)
        if tenant_id is not None:
            query = query.filter(SucursalModel.tenant_id == tenant_id)

        sucursales = query.order_by(SucursalModel.id.asc()).all()
        return [
            {
                "id": s.id,
                "nombre": s.nombre,
                "ciudad": s.ciudad,
                "direccion": s.direccion,
                "telefono": s.telefono
            }
            for s in sucursales
        ]

    @staticmethod
    def actualizar_stock_sucursal(
        db: Session,
        datos: ActualizarStockRequest,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None,
        ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Actualiza o registra el stock físico de una variante en una sucursal con validación multitenant y Bitácora (CU26).
        """
        # Validar que la sucursal exista y pertenezca al tenant
        sucursal = db.query(SucursalModel).filter(
            SucursalModel.id == datos.sucursal_id
        )
        if tenant_id is not None:
            sucursal = sucursal.filter(SucursalModel.tenant_id == tenant_id)
        sucursal = sucursal.first()

        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sucursal con ID {datos.sucursal_id} no encontrada en este tenant"
            )

        # Validar que la variante exista y pertenezca al tenant
        variante = db.query(VarianteProductoModel).join(ProductoModel).filter(
            VarianteProductoModel.id == datos.variante_id
        )
        if tenant_id is not None:
            variante = variante.filter(ProductoModel.tenant_id == tenant_id)
        variante = variante.first()

        if not variante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Variante con ID {datos.variante_id} no encontrada en este tenant"
            )

        inv_query = db.query(InventarioSucursalModel).filter(
            InventarioSucursalModel.varianteid == datos.variante_id,
            InventarioSucursalModel.sucursalid == datos.sucursal_id
        )
        if tenant_id is not None:
            inv_query = inv_query.filter(InventarioSucursalModel.tenant_id == tenant_id)

        inv = inv_query.first()
        cant_previa = inv.cantidad if inv else 0

        if inv:
            inv.cantidad = datos.cantidad
            if datos.stock_minimo is not None:
                inv.stockminimo = datos.stock_minimo
        else:
            inv = InventarioSucursalModel(
                varianteid=datos.variante_id,
                sucursalid=datos.sucursal_id,
                cantidad=datos.cantidad,
                stockminimo=datos.stock_minimo or 5,
                tenant_id=tenant_id
            )
            db.add(inv)

        db.commit()
        db.refresh(inv)

        # Auditoría en Bitácora (CU26)
        try:
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR",
                modulo="CU08_CATALOGO_DISPONIBILIDAD",
                usuario_id=usuario_id,
                detalle=(
                    f"Actualización de stock físico para variante {datos.variante_id} "
                    f"en sucursal '{sucursal.nombre}': {cant_previa} -> {datos.cantidad} unidades."
                ),
                ip=ip,
                datos_previos={"cantidad": cant_previa, "variante_id": datos.variante_id, "sucursal_id": datos.sucursal_id},
                datos_nuevos={"cantidad": datos.cantidad, "variante_id": datos.variante_id, "sucursal_id": datos.sucursal_id, "stockminimo": inv.stockminimo}
            )
        except Exception as audit_err:
            print(f"[AUDITORIA WARN] Error al registrar en bitácora para CU08: {audit_err}")

        return {
            "mensaje": "Stock actualizado correctamente",
            "variante_id": datos.variante_id,
            "sucursal_id": datos.sucursal_id,
            "cantidad": datos.cantidad
        }
