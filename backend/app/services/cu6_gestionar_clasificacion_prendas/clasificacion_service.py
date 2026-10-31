# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: CU6 - Gestionar Clasificación de Prendas (Categorías, Temporadas, Colecciones)
# Arquitectura: Multi-Tenant SaaS con Auditoría Bitácora (CU20)
# Ubicación: backend/app/services/cu6_gestionar_clasificacion_prendas/clasificacion_service.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.models import Categoria, Temporada, Coleccion, Producto
from app.schemas.clasificacion_schema import (
    CategoriaCreate, CategoriaUpdate,
    TemporadaCreate, TemporadaUpdate,
    ColeccionCreate, ColeccionUpdate
)


class CategoriaService:
    """
    Servicio de dominio para la gestión de Categorías de prendas,
    con aislamiento por tenant, validación de unicidad y registro de auditoría.
    """

    @staticmethod
    def listar_categorias(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[Categoria]:
        query = db.query(Categoria)
        if tenant_id is not None:
            query = query.filter(Categoria.tenant_id == tenant_id)
        if search:
            query = query.filter(Categoria.nombre.ilike(f"%{search.strip()}%"))
        if activo is not None:
            query = query.filter(Categoria.activo == activo)
        return query.order_by(Categoria.id.desc()).all()

    @staticmethod
    def obtener_categoria_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Categoria:
        query = db.query(Categoria).filter(Categoria.id == id)
        if tenant_id is not None:
            query = query.filter(Categoria.tenant_id == tenant_id)
        cat = query.first()
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {id} no encontrada"
            )
        return cat

    @staticmethod
    def crear_categoria(
        db: Session,
        data: CategoriaCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Categoria:
        clean_nombre = data.nombre.strip()
        # Verificar duplicados dentro del mismo tenant
        existente = db.query(Categoria).filter(
            Categoria.tenant_id == tenant_id,
            Categoria.nombre.ilike(clean_nombre)
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una categoría registrada con el nombre '{clean_nombre}'"
            )

        nueva = Categoria(
            tenant_id=tenant_id,
            nombre=clean_nombre,
            descripcion=data.descripcion.strip() if data.descripcion else None,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_CATEGORIA",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Registro de nueva categoría: '{nueva.nombre}' (ID: {nueva.id}) en tenant #{tenant_id}"
            )
        except Exception:
            pass

        return nueva

    @staticmethod
    def actualizar_categoria(
        db: Session,
        id: int,
        data: CategoriaUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Categoria:
        cat = CategoriaService.obtener_categoria_por_id(db, id=id, tenant_id=tenant_id)

        update_dict = data.dict(exclude_unset=True)
        if "nombre" in update_dict and update_dict["nombre"]:
            nuevo_nombre = update_dict["nombre"].strip()
            duplicado = db.query(Categoria).filter(
                Categoria.tenant_id == cat.tenant_id,
                Categoria.nombre.ilike(nuevo_nombre),
                Categoria.id != id
            ).first()
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otra categoría con el nombre '{nuevo_nombre}'"
                )
            cat.nombre = nuevo_nombre

        if "descripcion" in update_dict:
            cat.descripcion = update_dict["descripcion"].strip() if update_dict["descripcion"] else None
        if "activo" in update_dict and update_dict["activo"] is not None:
            cat.activo = update_dict["activo"]

        db.commit()
        db.refresh(cat)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR_CATEGORIA",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Actualización de categoría ID={id} ('{cat.nombre}')"
            )
        except Exception:
            pass

        return cat

    @staticmethod
    def cambiar_estado_categoria(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Categoria:
        cat = CategoriaService.obtener_categoria_por_id(db, id=id, tenant_id=tenant_id)
        cat.activo = activo
        db.commit()
        db.refresh(cat)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO_CATEGORIA",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Cambio de estado categoría ID={id} a {'Activo' if activo else 'Inactivo'}"
            )
        except Exception:
            pass

        return cat

    @staticmethod
    def eliminar_categoria(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        cat = CategoriaService.obtener_categoria_por_id(db, id=id, tenant_id=tenant_id)

        # Verificar si posee productos asignados
        total_productos = db.query(Producto).filter(Producto.categoriaid == id).count()
        if total_productos > 0:
            cat.activo = False
            db.commit()
            return {
                "message": f"Categoría '{cat.nombre}' desactivada porque tiene {total_productos} productos vinculados",
                "id": id,
                "desactivado": True
            }

        try:
            nombre_cat = cat.nombre
            db.delete(cat)
            db.commit()

            # Auditoría en Bitácora (CU20)
            try:
                from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
                BitacoraController.registrar_evento(
                    db=db,
                    accion="ELIMINAR_CATEGORIA",
                    modulo="CLASIFICACION",
                    usuario_id=usuario_id or 1,
                    detalle=f"Eliminación definitiva de categoría '{nombre_cat}' (ID: {id})"
                )
            except Exception:
                pass

            return {"message": f"Categoría '{nombre_cat}' eliminada definitivamente", "id": id, "desactivado": False}
        except Exception:
            db.rollback()
            cat.activo = False
            db.commit()
            return {"message": "Categoría desactivada por restricciones de integridad", "id": id, "desactivado": True}


class TemporadaService:
    """
    Servicio de dominio para la gestión de Temporadas comerciales (Otoño-Invierno, Primavera-Verano),
    aislamiento multi-tenant y auditoría.
    """

    @staticmethod
    def listar_temporadas(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[Temporada]:
        query = db.query(Temporada)
        if tenant_id is not None:
            query = query.filter(Temporada.tenant_id == tenant_id)
        if search:
            query = query.filter(Temporada.nombre.ilike(f"%{search.strip()}%"))
        if activo is not None:
            query = query.filter(Temporada.activo == activo)
        return query.order_by(Temporada.id.desc()).all()

    @staticmethod
    def obtener_temporada_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Temporada:
        query = db.query(Temporada).filter(Temporada.id == id)
        if tenant_id is not None:
            query = query.filter(Temporada.tenant_id == tenant_id)
        temp = query.first()
        if not temp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Temporada con ID {id} no encontrada"
            )
        return temp

    @staticmethod
    def crear_temporada(
        db: Session,
        data: TemporadaCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Temporada:
        clean_nombre = data.nombre.strip()
        existente = db.query(Temporada).filter(
            Temporada.tenant_id == tenant_id,
            Temporada.nombre.ilike(clean_nombre)
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una temporada registrada con el nombre '{clean_nombre}'"
            )

        nueva = Temporada(
            tenant_id=tenant_id,
            nombre=clean_nombre,
            descripcion=data.descripcion.strip() if data.descripcion else None,
            fechainicio=data.fechainicio,
            fechafin=data.fechafin,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_TEMPORADA",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Registro de nueva temporada: '{nueva.nombre}' (ID: {nueva.id}) en tenant #{tenant_id}"
            )
        except Exception:
            pass

        return nueva

    @staticmethod
    def actualizar_temporada(
        db: Session,
        id: int,
        data: TemporadaUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Temporada:
        temp = TemporadaService.obtener_temporada_por_id(db, id=id, tenant_id=tenant_id)
        update_dict = data.dict(exclude_unset=True)

        if "nombre" in update_dict and update_dict["nombre"]:
            nuevo_nombre = update_dict["nombre"].strip()
            duplicado = db.query(Temporada).filter(
                Temporada.tenant_id == temp.tenant_id,
                Temporada.nombre.ilike(nuevo_nombre),
                Temporada.id != id
            ).first()
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otra temporada con el nombre '{nuevo_nombre}'"
                )
            temp.nombre = nuevo_nombre

        if "descripcion" in update_dict:
            temp.descripcion = update_dict["descripcion"].strip() if update_dict["descripcion"] else None
        if "fechainicio" in update_dict:
            temp.fechainicio = update_dict["fechainicio"]
        if "fechafin" in update_dict:
            temp.fechafin = update_dict["fechafin"]
        if "activo" in update_dict and update_dict["activo"] is not None:
            temp.activo = update_dict["activo"]

        db.commit()
        db.refresh(temp)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR_TEMPORADA",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Actualización de temporada ID={id} ('{temp.nombre}')"
            )
        except Exception:
            pass

        return temp

    @staticmethod
    def cambiar_estado_temporada(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Temporada:
        temp = TemporadaService.obtener_temporada_por_id(db, id=id, tenant_id=tenant_id)
        temp.activo = activo
        db.commit()
        db.refresh(temp)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO_TEMPORADA",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Cambio de estado temporada ID={id} a {'Activo' if activo else 'Inactivo'}"
            )
        except Exception:
            pass

        return temp

    @staticmethod
    def eliminar_temporada(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        temp = TemporadaService.obtener_temporada_por_id(db, id=id, tenant_id=tenant_id)

        # Verificar colecciones asociadas
        total_colecciones = db.query(Coleccion).filter(Coleccion.temporadaid == id).count()
        if total_colecciones > 0:
            temp.activo = False
            db.commit()
            return {
                "message": f"Temporada '{temp.nombre}' desactivada porque tiene {total_colecciones} colecciones asociadas",
                "id": id,
                "desactivado": True
            }

        try:
            nombre_temp = temp.nombre
            db.delete(temp)
            db.commit()

            # Auditoría en Bitácora (CU20)
            try:
                from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
                BitacoraController.registrar_evento(
                    db=db,
                    accion="ELIMINAR_TEMPORADA",
                    modulo="CLASIFICACION",
                    usuario_id=usuario_id or 1,
                    detalle=f"Eliminación definitiva de temporada '{nombre_temp}' (ID: {id})"
                )
            except Exception:
                pass

            return {"message": f"Temporada '{nombre_temp}' eliminada definitivamente", "id": id, "desactivado": False}
        except Exception:
            db.rollback()
            temp.activo = False
            db.commit()
            return {"message": "Temporada desactivada por restricciones de integridad", "id": id, "desactivado": True}


class ColeccionService:
    """
    Servicio de dominio para la gestión de Colecciones de moda y catálogo,
    aislamiento multi-tenant y auditoría.
    """

    @staticmethod
    def listar_colecciones(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        temporada_id: Optional[int] = None,
        activo: Optional[bool] = None
    ) -> List[Coleccion]:
        query = db.query(Coleccion).options(joinedload(Coleccion.temporada))
        if tenant_id is not None:
            query = query.filter(Coleccion.tenant_id == tenant_id)
        if search:
            query = query.filter(Coleccion.nombre.ilike(f"%{search.strip()}%"))
        if temporada_id is not None:
            query = query.filter(Coleccion.temporadaid == temporada_id)
        if activo is not None:
            query = query.filter(Coleccion.activo == activo)
        return query.order_by(Coleccion.id.desc()).all()

    @staticmethod
    def obtener_coleccion_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Coleccion:
        query = db.query(Coleccion).options(joinedload(Coleccion.temporada)).filter(Coleccion.id == id)
        if tenant_id is not None:
            query = query.filter(Coleccion.tenant_id == tenant_id)
        col = query.first()
        if not col:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Colección con ID {id} no encontrada"
            )
        return col

    @staticmethod
    def crear_coleccion(
        db: Session,
        data: ColeccionCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Coleccion:
        clean_nombre = data.nombre.strip()
        existente = db.query(Coleccion).filter(
            Coleccion.tenant_id == tenant_id,
            Coleccion.nombre.ilike(clean_nombre)
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una colección registrada con el nombre '{clean_nombre}'"
            )

        # Si especifica temporada, verificar que exista en el tenant
        if data.temporadaid:
            temp = db.query(Temporada).filter(
                Temporada.id == data.temporadaid,
                Temporada.tenant_id == tenant_id
            ).first()
            if not temp:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La temporada ID {data.temporadaid} no existe en este tenant"
                )

        nueva = Coleccion(
            tenant_id=tenant_id,
            nombre=clean_nombre,
            descripcion=data.descripcion.strip() if data.descripcion else None,
            imagenurl=data.imagenurl,
            temporadaid=data.temporadaid,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_COLECCION",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Registro de nueva colección: '{nueva.nombre}' (ID: {nueva.id}) en tenant #{tenant_id}"
            )
        except Exception:
            pass

        return nueva

    @staticmethod
    def actualizar_coleccion(
        db: Session,
        id: int,
        data: ColeccionUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Coleccion:
        col = ColeccionService.obtener_coleccion_por_id(db, id=id, tenant_id=tenant_id)
        update_dict = data.dict(exclude_unset=True)

        if "nombre" in update_dict and update_dict["nombre"]:
            nuevo_nombre = update_dict["nombre"].strip()
            duplicado = db.query(Coleccion).filter(
                Coleccion.tenant_id == col.tenant_id,
                Coleccion.nombre.ilike(nuevo_nombre),
                Coleccion.id != id
            ).first()
            if duplicado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otra colección con el nombre '{nuevo_nombre}'"
                )
            col.nombre = nuevo_nombre

        if "descripcion" in update_dict:
            col.descripcion = update_dict["descripcion"].strip() if update_dict["descripcion"] else None
        if "imagenurl" in update_dict:
            col.imagenurl = update_dict["imagenurl"]
        if "temporadaid" in update_dict:
            col.temporadaid = update_dict["temporadaid"]
        if "activo" in update_dict and update_dict["activo"] is not None:
            col.activo = update_dict["activo"]

        db.commit()
        db.refresh(col)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR_COLECCION",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Actualización de colección ID={id} ('{col.nombre}')"
            )
        except Exception:
            pass

        return col

    @staticmethod
    def cambiar_estado_coleccion(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Coleccion:
        col = ColeccionService.obtener_coleccion_por_id(db, id=id, tenant_id=tenant_id)
        col.activo = activo
        db.commit()
        db.refresh(col)

        # Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO_COLECCION",
                modulo="CLASIFICACION",
                usuario_id=usuario_id or 1,
                detalle=f"Cambio de estado colección ID={id} a {'Activo' if activo else 'Inactivo'}"
            )
        except Exception:
            pass

        return col

    @staticmethod
    def eliminar_coleccion(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        col = ColeccionService.obtener_coleccion_por_id(db, id=id, tenant_id=tenant_id)
        nombre_col = col.nombre
        try:
            db.delete(col)
            db.commit()

            # Auditoría en Bitácora (CU20)
            try:
                from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
                BitacoraController.registrar_evento(
                    db=db,
                    accion="ELIMINAR_COLECCION",
                    modulo="CLASIFICACION",
                    usuario_id=usuario_id or 1,
                    detalle=f"Eliminación definitiva de colección '{nombre_col}' (ID: {id})"
                )
            except Exception:
                pass

            return {"message": f"Colección '{nombre_col}' eliminada definitivamente", "id": id, "desactivado": False}
        except Exception:
            db.rollback()
            col.activo = False
            db.commit()
            return {"message": "Colección desactivada por restricciones de integridad", "id": id, "desactivado": True}


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
# Categoría
CategoriaService.get_all = CategoriaService.listar_categorias
CategoriaService.get_by_id = CategoriaService.obtener_categoria_por_id
CategoriaService.create = CategoriaService.crear_categoria
CategoriaService.update = CategoriaService.actualizar_categoria
CategoriaService.delete = CategoriaService.eliminar_categoria
CategoriaService.toggle_status = CategoriaService.cambiar_estado_categoria

# Temporada
TemporadaService.get_all = TemporadaService.listar_temporadas
TemporadaService.get_by_id = TemporadaService.obtener_temporada_por_id
TemporadaService.create = TemporadaService.crear_temporada
TemporadaService.update = TemporadaService.actualizar_temporada
TemporadaService.delete = TemporadaService.eliminar_temporada
TemporadaService.toggle_status = TemporadaService.cambiar_estado_temporada

# Colección
ColeccionService.get_all = ColeccionService.listar_colecciones
ColeccionService.get_by_id = ColeccionService.obtener_coleccion_por_id
ColeccionService.create = ColeccionService.crear_coleccion
ColeccionService.update = ColeccionService.actualizar_coleccion
ColeccionService.delete = ColeccionService.eliminar_coleccion
ColeccionService.toggle_status = ColeccionService.cambiar_estado_coleccion
