# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU6 - Gestionar Clasificación de Prendas (Categorías, Temporadas, Colecciones)
# Arquitectura: Multi-Tenant SaaS con Funciones en Español
# Ubicación: backend/app/controllers/cu6_gestionar_clasificacion_prendas/clasificacion_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import Categoria, Temporada, Coleccion
from app.services.cu6_gestionar_clasificacion_prendas.clasificacion_service import (
    CategoriaService, TemporadaService, ColeccionService
)
from app.schemas.clasificacion_schema import (
    CategoriaCreate, CategoriaUpdate,
    TemporadaCreate, TemporadaUpdate,
    ColeccionCreate, ColeccionUpdate
)


class ClasificacionController:
    """
    Controlador MVC para la clasificación comercial del catálogo de prendas:
    Categorías, Temporadas y Colecciones de Moda.
    """

    # ==========================================================================
    # SECCIÓN CATEGORÍAS
    # ==========================================================================
    @staticmethod
    def listar_categorias(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[Categoria]:
        """Lista las categorías disponibles para el tenant"""
        return CategoriaService.listar_categorias(
            db=db,
            tenant_id=tenant_id,
            search=search,
            activo=activo
        )

    @staticmethod
    def obtener_categoria_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Categoria:
        """Obtiene una categoría por su ID"""
        return CategoriaService.obtener_categoria_por_id(
            db=db,
            id=id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_categoria(
        db: Session,
        data: CategoriaCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Categoria:
        """Crea una nueva categoría en el catálogo"""
        return CategoriaService.crear_categoria(
            db=db,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def actualizar_categoria(
        db: Session,
        id: int,
        data: CategoriaUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Categoria:
        """Actualiza los datos de una categoría"""
        return CategoriaService.actualizar_categoria(
            db=db,
            id=id,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def cambiar_estado_categoria(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Categoria:
        """Activa o suspende una categoría"""
        return CategoriaService.cambiar_estado_categoria(
            db=db,
            id=id,
            activo=activo,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def eliminar_categoria(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Elimina definitivamente o desactiva la categoría si contiene productos"""
        return CategoriaService.eliminar_categoria(
            db=db,
            id=id,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    # ==========================================================================
    # SECCIÓN TEMPORADAS
    # ==========================================================================
    @staticmethod
    def listar_temporadas(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[Temporada]:
        """Lista las temporadas comerciales del tenant"""
        return TemporadaService.listar_temporadas(
            db=db,
            tenant_id=tenant_id,
            search=search,
            activo=activo
        )

    @staticmethod
    def obtener_temporada_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Temporada:
        """Obtiene una temporada por su ID"""
        return TemporadaService.obtener_temporada_por_id(
            db=db,
            id=id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_temporada(
        db: Session,
        data: TemporadaCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Temporada:
        """Registra una nueva temporada de moda"""
        return TemporadaService.crear_temporada(
            db=db,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def actualizar_temporada(
        db: Session,
        id: int,
        data: TemporadaUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Temporada:
        """Actualiza una temporada comercial"""
        return TemporadaService.actualizar_temporada(
            db=db,
            id=id,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def cambiar_estado_temporada(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Temporada:
        """Activa o suspende una temporada"""
        return TemporadaService.cambiar_estado_temporada(
            db=db,
            id=id,
            activo=activo,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def eliminar_temporada(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Elimina o desactiva la temporada si posee colecciones"""
        return TemporadaService.eliminar_temporada(
            db=db,
            id=id,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    # ==========================================================================
    # SECCIÓN COLECCIONES
    # ==========================================================================
    @staticmethod
    def listar_colecciones(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        temporada_id: Optional[int] = None,
        activo: Optional[bool] = None
    ) -> List[Coleccion]:
        """Lista las colecciones de prendas del tenant"""
        return ColeccionService.listar_colecciones(
            db=db,
            tenant_id=tenant_id,
            search=search,
            temporada_id=temporada_id,
            activo=activo
        )

    @staticmethod
    def obtener_coleccion_por_id(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None
    ) -> Coleccion:
        """Obtiene una colección por su ID"""
        return ColeccionService.obtener_coleccion_por_id(
            db=db,
            id=id,
            tenant_id=tenant_id
        )

    @staticmethod
    def crear_coleccion(
        db: Session,
        data: ColeccionCreate,
        tenant_id: int = 1,
        usuario_id: Optional[int] = None
    ) -> Coleccion:
        """Registra una nueva colección de prendas"""
        return ColeccionService.crear_coleccion(
            db=db,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def actualizar_coleccion(
        db: Session,
        id: int,
        data: ColeccionUpdate,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Coleccion:
        """Actualiza una colección"""
        return ColeccionService.actualizar_coleccion(
            db=db,
            id=id,
            data=data,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def cambiar_estado_coleccion(
        db: Session,
        id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Coleccion:
        """Activa o suspende una colección"""
        return ColeccionService.cambiar_estado_coleccion(
            db=db,
            id=id,
            activo=activo,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )

    @staticmethod
    def eliminar_coleccion(
        db: Session,
        id: int,
        tenant_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Elimina o desactiva la colección"""
        return ColeccionService.eliminar_coleccion(
            db=db,
            id=id,
            tenant_id=tenant_id,
            usuario_id=usuario_id
        )


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
ClasificacionController.baja_categoria = ClasificacionController.eliminar_categoria
ClasificacionController.baja_temporada = ClasificacionController.eliminar_temporada
ClasificacionController.baja_coleccion = ClasificacionController.eliminar_coleccion

ClassificationController = ClasificacionController
