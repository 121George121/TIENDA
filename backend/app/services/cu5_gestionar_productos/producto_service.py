# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: Productos y Catálogo Retail (CU05)
# Ubicación: backend/app/services/producto_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import ProductoModel, VarianteProductoModel
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate
from fastapi import HTTPException, status
from typing import Optional, List

class ProductoService:

    @staticmethod
    def get_all(
        db: Session,
        search: Optional[str] = None,
        categoria_id: Optional[int] = None,
        genero: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductoModel]:
        query = db.query(ProductoModel)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (ProductoModel.nombre.ilike(pattern)) |
                (ProductoModel.marca.ilike(pattern)) |
                (ProductoModel.descripcion.ilike(pattern))
            )

        if categoria_id:
            query = query.filter(ProductoModel.categoriaid == categoria_id)

        if genero:
            query = query.filter(ProductoModel.genero.ilike(f"%{genero}%"))

        if activo is not None:
            query = query.filter(ProductoModel.activo == activo)

        return query.order_by(ProductoModel.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, id: int) -> ProductoModel:
        producto = db.query(ProductoModel).filter(ProductoModel.id == id).first()
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return producto

    @staticmethod
    def create(db: Session, data: ProductoCreate) -> ProductoModel:
        nuevo = ProductoModel(
            nombre=data.nombre,
            descripcion=data.descripcion,
            marca=data.marca,
            genero=data.genero,
            grupoedad=data.grupoedad,
            preciobase=data.preciobase,
            imagenprincipal=data.imagenprincipal,
            categoriaid=data.categoriaid,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def update(db: Session, id: int, data: ProductoUpdate) -> ProductoModel:
        producto = db.query(ProductoModel).filter(ProductoModel.id == id).first()
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        for key, value in data.dict(exclude_unset=True).items():
            setattr(producto, key, value)

        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def toggle_status(db: Session, id: int, activo: bool) -> ProductoModel:
        producto = db.query(ProductoModel).filter(ProductoModel.id == id).first()
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        producto.activo = activo
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def delete(db: Session, id: int) -> dict:
        producto = db.query(ProductoModel).filter(ProductoModel.id == id).first()
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        nombre_prod = producto.nombre

        # 1. Obtener variantes asociadas al producto
        variantes = db.query(VarianteProductoModel).filter(VarianteProductoModel.productoid == id).all()
        var_ids = [v.id for v in variantes]

        if var_ids:
            v_ids_str = ",".join(str(i) for i in var_ids)

            # 2. Verificar si tiene ventas registradas en detalle_venta
            try:
                ventas_count = db.execute(
                    text(f"SELECT count(*) FROM detalle_venta WHERE varianteid IN ({v_ids_str})")
                ).scalar() or 0
                if ventas_count > 0:
                    producto.activo = False
                    db.commit()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"No se puede eliminar permanentemente '{nombre_prod}' porque tiene {ventas_count} venta(s) en historial. Ha sido desactivado del catálogo."
                    )
            except HTTPException:
                raise
            except Exception:
                pass

            # 3. Limpiar dependencias en carritos y reservas
            try:
                db.execute(text(f"DELETE FROM carrito_item WHERE varianteid IN ({v_ids_str})"))
            except Exception:
                pass

            try:
                db.execute(text(f"DELETE FROM reserva_detalle WHERE varianteid IN ({v_ids_str})"))
            except Exception:
                pass

            # 4. Limpiar inventarios y movimientos
            try:
                inv_ids = db.execute(text(f"SELECT id FROM inventario WHERE varianteid IN ({v_ids_str})")).fetchall()
                if inv_ids:
                    inv_ids_str = ",".join(str(row[0]) for row in inv_ids)
                    db.execute(text(f"DELETE FROM movimiento_inventario WHERE inventarioid IN ({inv_ids_str})"))
                db.execute(text(f"DELETE FROM inventario WHERE varianteid IN ({v_ids_str})"))
            except Exception:
                pass

            try:
                db.execute(text(f"DELETE FROM inventario_sucursal WHERE varianteid IN ({v_ids_str})"))
            except Exception:
                pass

            # 5. Eliminar variantes
            db.execute(text(f"DELETE FROM variante_producto WHERE id IN ({v_ids_str})"))

        # 6. Eliminar asociaciones de proveedores si existieran
        try:
            db.execute(text("DELETE FROM producto_proveedor WHERE idproducto = :pid"), {"pid": id})
        except Exception:
            pass

        # 7. Eliminar producto definitivamente
        db.delete(producto)
        db.commit()
        return {"message": f"Producto '{nombre_prod}' eliminado definitivamente de la base de datos", "id": id}

    @staticmethod
    def logical_delete(db: Session, id: int) -> dict:
        return ProductoService.delete(db=db, id=id)
