# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: CU7 - Gestionar Proveedores y Productos Suministrados
# Arquitectura: Multi-Tenant SaaS con Auditoría Bitácora (CU20)
# Ubicación: backend/app/services/cu7_gestionar_proveedores_productos_suministrados/proveedor_service.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.models import Proveedor, ProductoProveedor, Producto
from app.schemas.proveedor_schema import (
    ProveedorCreate, ProveedorUpdate, ProductoProveedorCreate
)


class ProveedorService:
    """
    Servicio de dominio para la gestión integral de Proveedores de insumos y prendas,
    con control de productos suministrados, costos de compra, aislamiento por tenant y auditoría.
    """

    @staticmethod
    def listar_proveedores(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Proveedor]:
        """Lista los proveedores registrados para el tenant con filtros y búsqueda"""
        query = db.query(Proveedor).options(
            joinedload(Proveedor.productos_suministrados).joinedload(ProductoProveedor.producto)
        )

        if tenant_id is not None:
            query = query.filter(Proveedor.tenant_id == tenant_id)

        if search:
            clean_search = f"%{search.strip()}%"
            query = query.filter(
                (Proveedor.nombre.ilike(clean_search)) |
                (Proveedor.razonsocial.ilike(clean_search)) |
                (Proveedor.nit.ilike(clean_search)) |
                (Proveedor.contacto.ilike(clean_search)) |
                (Proveedor.email.ilike(clean_search))
            )

        if activo is not None:
            query = query.filter(Proveedor.activo == activo)

        return query.order_by(Proveedor.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_proveedor_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Proveedor:
        """Obtiene el detalle completo de un proveedor verificando aislamiento por tenant"""
        query = db.query(Proveedor).options(
            joinedload(Proveedor.productos_suministrados).joinedload(ProductoProveedor.producto)
        ).filter(Proveedor.id == id)

        if tenant_id is not None:
            query = query.filter(Proveedor.tenant_id == tenant_id)

        prov = query.first()
        if not prov:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {id} no encontrado"
            )
        return prov

    @staticmethod
    def crear_proveedor(
        db: Session,
        data: ProveedorCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Proveedor:
        """Registra un nuevo proveedor en el tenant validando unicidad"""
        clean_nombre = data.nombre.strip()

        # Validar duplicados de nombre en el mismo tenant
        existente = db.query(Proveedor).filter(
            Proveedor.tenant_id == tenant_id,
            Proveedor.nombre.ilike(clean_nombre)
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un proveedor registrado con el nombre '{clean_nombre}'"
            )

        # Si especifica NIT, verificar que no esté repetido en el tenant
        if data.nit and data.nit.strip():
            nit_clean = data.nit.strip()
            dup_nit = db.query(Proveedor).filter(
                Proveedor.tenant_id == tenant_id,
                Proveedor.nit == nit_clean
            ).first()
            if dup_nit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un proveedor registrado con el NIT '{nit_clean}' ({dup_nit.nombre})"
                )

        nuevo = Proveedor(
            tenant_id=tenant_id,
            nombre=clean_nombre,
            razonsocial=data.razonsocial.strip() if data.razonsocial else None,
            nit=data.nit.strip() if data.nit else None,
            contacto=data.contacto.strip() if data.contacto else None,
            telefono=data.telefono.strip() if data.telefono else None,
            email=data.email.strip().lower() if data.email else None,
            direccion=data.direccion.strip() if data.direccion else None,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_PROVEEDOR",
                modulo="PROVEEDORES",
                usuario_id=usuario_id or 1,
                detalle=f"Registro de nuevo proveedor: '{nuevo.nombre}' (NIT: {nuevo.nit or 'S/N'}, ID: {nuevo.id}) en tenant #{tenant_id}"
            )
        except Exception:
            pass

        return nuevo

    @staticmethod
    def actualizar_proveedor(
        db: Session,
        id: int,
        data: ProveedorUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Proveedor:
        """Actualiza los datos comerciales y de contacto del proveedor"""
        prov = ProveedorService.obtener_proveedor_por_id(db, id=id, tenant_id=tenant_id)
        update_dict = data.dict(exclude_unset=True)

        if "nombre" in update_dict and update_dict["nombre"]:
            nuevo_nombre = update_dict["nombre"].strip()
            duplicado = db.query(Proveedor).filter(
                Proveedor.tenant_id == prov.tenant_id,
                Proveedor.nombre.ilike(nuevo_nombre),
                Proveedor.id != id
            ).first()
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro proveedor con el nombre '{nuevo_nombre}'"
                )
            prov.nombre = nuevo_nombre

        if "nit" in update_dict and update_dict["nit"]:
            nuevo_nit = update_dict["nit"].strip()
            dup_nit = db.query(Proveedor).filter(
                Proveedor.tenant_id == prov.tenant_id,
                Proveedor.nit == nuevo_nit,
                Proveedor.id != id
            ).first()
            if dup_nit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro proveedor con el NIT '{nuevo_nit}'"
                )
            prov.nit = nuevo_nit

        if "razonsocial" in update_dict:
            prov.razonsocial = update_dict["razonsocial"].strip() if update_dict["razonsocial"] else None
        if "contacto" in update_dict:
            prov.contacto = update_dict["contacto"].strip() if update_dict["contacto"] else None
        if "telefono" in update_dict:
            prov.telefono = update_dict["telefono"].strip() if update_dict["telefono"] else None
        if "email" in update_dict:
            prov.email = update_dict["email"].strip().lower() if update_dict["email"] else None
        if "direccion" in update_dict:
            prov.direccion = update_dict["direccion"].strip() if update_dict["direccion"] else None
        if "activo" in update_dict and update_dict["activo"] is not None:
            prov.activo = update_dict["activo"]

        db.commit()
        db.refresh(prov)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR_PROVEEDOR",
                modulo="PROVEEDORES",
                usuario_id=usuario_id or 1,
                detalle=f"Actualización de proveedor ID={id} ('{prov.nombre}')"
            )
        except Exception:
            pass

        return prov

    @staticmethod
    def cambiar_estado_proveedor(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Proveedor:
        """Activa o suspende el estado comercial del proveedor"""
        prov = ProveedorService.obtener_proveedor_por_id(db, id=id, tenant_id=tenant_id)
        prov.activo = activo
        db.commit()
        db.refresh(prov)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO_PROVEEDOR",
                modulo="PROVEEDORES",
                usuario_id=usuario_id or 1,
                detalle=f"Cambio de estado proveedor ID={id} a {'Activo' if activo else 'Inactivo'}"
            )
        except Exception:
            pass

        return prov

    @staticmethod
    def eliminar_proveedor(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Elimina definitivamente o aplica baja lógica si posee suministros vinculados"""
        prov = ProveedorService.obtener_proveedor_por_id(db, id=id, tenant_id=tenant_id)

        # Verificar si tiene productos suministrados vinculados
        suministros_count = db.query(ProductoProveedor).filter(ProductoProveedor.idproveedor == id).count()
        if suministros_count > 0:
            prov.activo = False
            db.commit()
            return {
                "message": f"Proveedor '{prov.nombre}' desactivado (baja lógica) porque posee {suministros_count} productos suministrados asociados",
                "id": id,
                "desactivado": True
            }

        try:
            nombre_prov = prov.nombre
            db.delete(prov)
            db.commit()

            # Auditoría en Bitácora (CU20)
            try:
                from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
                BitacoraController.registrar_evento(
                    db=db,
                    accion="ELIMINAR_PROVEEDOR",
                    modulo="PROVEEDORES",
                    usuario_id=usuario_id or 1,
                    detalle=f"Eliminación definitiva de proveedor '{nombre_prov}' (ID: {id})"
                )
            except Exception:
                pass

            return {"message": f"Proveedor '{nombre_prov}' eliminado definitivamente", "id": id, "desactivado": False}
        except Exception:
            db.rollback()
            prov.activo = False
            db.commit()
            return {"message": "Proveedor desactivado por restricciones de integridad", "id": id, "desactivado": True}

    # ==========================================================================
    # SECCIÓN PRODUCTOS SUMINISTRADOS
    # ==========================================================================
    @staticmethod
    def vincular_producto_suministrado(
        db: Session,
        data: ProductoProveedorCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> ProductoProveedor:
        """Asocia un producto del catálogo con un proveedor suministrador e indica costo de compra"""
        # Verificar que el proveedor exista y pertenezca al tenant
        prov = ProveedorService.obtener_proveedor_por_id(db, id=data.idproveedor, tenant_id=tenant_id)

        # Verificar que el producto exista y pertenezca al tenant
        prod = db.query(Producto).filter(Producto.id == data.idproducto, Producto.tenant_id == tenant_id).first()
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {data.idproducto} no existe en este tenant"
            )

        rel = db.query(ProductoProveedor).filter(
            ProductoProveedor.idproducto == data.idproducto,
            ProductoProveedor.idproveedor == data.idproveedor
        ).first()

        if rel:
            rel.costocompra = data.costocompra
            rel.cantidad = data.cantidad
        else:
            rel = ProductoProveedor(
                idproducto=data.idproducto,
                idproveedor=data.idproveedor,
                costocompra=data.costocompra,
                cantidad=data.cantidad
            )
            db.add(rel)

        db.commit()
        db.refresh(rel)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="VINCULAR_SUMINISTRO",
                modulo="PROVEEDORES",
                usuario_id=usuario_id or 1,
                detalle=f"Vinculación de suministro: Producto '{prod.nombre}' (ID: {prod.id}) con Proveedor '{prov.nombre}' (Costo: {data.costocompra})"
            )
        except Exception:
            pass

        return rel

    @staticmethod
    def listar_productos_suministrados(
        db: Session,
        proveedor_id: int,
        tenant_id: int = 1
    ) -> List[ProductoProveedor]:
        """Lista los productos suministrados por un proveedor específico"""
        # Validar proveedor
        ProveedorService.obtener_proveedor_por_id(db, id=proveedor_id, tenant_id=tenant_id)

        return db.query(ProductoProveedor).options(
            joinedload(ProductoProveedor.producto)
        ).filter(ProductoProveedor.idproveedor == proveedor_id).all()


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
ProveedorService.get_all = ProveedorService.listar_proveedores
ProveedorService.get_by_id = ProveedorService.obtener_proveedor_por_id
ProveedorService.create = ProveedorService.crear_proveedor
ProveedorService.update = ProveedorService.actualizar_proveedor
ProveedorService.delete = ProveedorService.eliminar_proveedor
ProveedorService.toggle_status = ProveedorService.cambiar_estado_proveedor
ProveedorService.vincular_producto = ProveedorService.vincular_producto_suministrado
