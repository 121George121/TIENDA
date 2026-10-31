# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU2 - Gestionar Usuarios y Roles
# Ubicación: backend/app/controllers/cu2_gestionar_usuarios_roles/role_controller.py
# ==============================================================================

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import Rol
from app.schemas.schemas import RolCreate

# Catálogo predeterminado de permisos por rol
PERMISOS_PREDETERMINADOS: Dict[str, List[str]] = {
    "ADMIN": [
        "USUARIOS_LISTAR", "USUARIOS_CREAR", "USUARIOS_EDITAR", "USUARIOS_ESTADO", "USUARIOS_ROL",
        "ROLES_LISTAR", "ROLES_CREAR", "ROLES_EDITAR", "ROLES_PERMISOS",
        "PRODUCTOS_LISTAR", "PRODUCTOS_CREAR", "PRODUCTOS_EDITAR", "PRODUCTOS_ELIMINAR",
        "ORDENES_LISTAR", "ORDENES_GESTIONAR",
        "BITACORA_LISTAR", "BITACORA_EXPORTAR"
    ],
    "ADMINISTRADOR": [
        "USUARIOS_LISTAR", "USUARIOS_CREAR", "USUARIOS_EDITAR", "USUARIOS_ESTADO", "USUARIOS_ROL",
        "ROLES_LISTAR", "ROLES_CREAR", "ROLES_EDITAR", "ROLES_PERMISOS",
        "PRODUCTOS_LISTAR", "PRODUCTOS_CREAR", "PRODUCTOS_EDITAR", "PRODUCTOS_ELIMINAR",
        "ORDENES_LISTAR", "ORDENES_GESTIONAR",
        "BITACORA_LISTAR", "BITACORA_EXPORTAR"
    ],
    "SUPERVISOR": [
        "USUARIOS_LISTAR", "PRODUCTOS_LISTAR", "PRODUCTOS_CREAR", "PRODUCTOS_EDITAR",
        "ORDENES_LISTAR", "ORDENES_GESTIONAR", "BITACORA_LISTAR"
    ],
    "CAJERO": [
        "PRODUCTOS_LISTAR", "ORDENES_LISTAR", "ORDENES_GESTIONAR"
    ],
    "CLIENTE": [
        "PRODUCTOS_LISTAR", "ORDENES_CREAR", "ORDENES_LISTAR_PROPIAS"
    ]
}

CACHE_PERMISOS_ROL: Dict[int, List[str]] = {}


class RolController:
    """
    Controlador MVC para la administración de roles y matriz de permisos.
    """

    @staticmethod
    def obtener_permisos_rol(rol: Rol) -> List[str]:
        """Obtiene la lista de permisos asignados a un rol"""
        if rol.id in CACHE_PERMISOS_ROL:
            return CACHE_PERMISOS_ROL[rol.id]
        
        nombre_upper = (rol.nombre or "").upper()
        if nombre_upper in PERMISOS_PREDETERMINADOS:
            return PERMISOS_PREDETERMINADOS[nombre_upper]
            
        return ["PRODUCTOS_LISTAR"]

    @staticmethod
    def listar_roles(db: Session) -> List[Dict[str, Any]]:
        """Obtiene el listado de todos los roles disponibles"""
        roles = db.query(Rol).order_by(Rol.id.asc()).all()
        resultado = []
        for r in roles:
            permisos = RolController.obtener_permisos_rol(r)
            resultado.append({
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "permisos": permisos
            })
        return resultado

    @staticmethod
    def obtener_rol_por_id(db: Session, rol_id: int) -> Dict[str, Any]:
        """Obtiene el detalle de un rol por su ID"""
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        permisos = RolController.obtener_permisos_rol(rol)
        return {
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": permisos
        }

    @staticmethod
    def crear_rol(db: Session, rol_data: RolCreate, operador_id: Optional[int] = None) -> Dict[str, Any]:
        """Crea un nuevo rol en el sistema"""
        clean_name = rol_data.nombre.strip()
        existente = db.query(Rol).filter(Rol.nombre.ilike(clean_name)).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del rol ya existe")

        nuevo_rol = Rol(
            nombre=clean_name,
            descripcion=rol_data.descripcion.strip() if rol_data.descripcion else None
        )
        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)

        # Asignar permisos enviados o predeterminados
        permisos = rol_data.permisos if rol_data.permisos else ["PRODUCTOS_LISTAR"]
        CACHE_PERMISOS_ROL[nuevo_rol.id] = permisos

        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_ROL",
                modulo="ROLES",
                usuario_id=operador_id or 1,
                detalle=f"Creación del rol {nuevo_rol.nombre}",
                datos_nuevos={"nombre": nuevo_rol.nombre, "permisos": permisos}
            )
        except Exception:
            pass

        return {
            "id": nuevo_rol.id,
            "nombre": nuevo_rol.nombre,
            "descripcion": nuevo_rol.descripcion,
            "permisos": permisos
        }

    @staticmethod
    def actualizar_rol(db: Session, rol_id: int, rol_data: RolCreate, operador_id: Optional[int] = None) -> Dict[str, Any]:
        """Edita nombre y descripción de un rol"""
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        if rol_id in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No se puede modificar el rol principal del sistema"
            )

        clean_name = rol_data.nombre.strip()
        existente = db.query(Rol).filter(Rol.nombre.ilike(clean_name), Rol.id != rol_id).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe otro rol con ese nombre")

        rol.nombre = clean_name
        if rol_data.descripcion is not None:
            rol.descripcion = rol_data.descripcion.strip()
        db.commit()
        db.refresh(rol)

        permisos = RolController.obtener_permisos_rol(rol)
        return {
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": permisos
        }

    @staticmethod
    def actualizar_permisos_rol(db: Session, rol_id: int, permisos: List[str], operador_id: Optional[int] = None) -> Dict[str, Any]:
        """Actualiza la lista de permisos asignados a un rol"""
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        CACHE_PERMISOS_ROL[rol_id] = list(set(permisos))

        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="MODIFICAR_PERMISOS",
                modulo="ROLES",
                usuario_id=operador_id or 1,
                detalle=f"Actualización de permisos para el rol {rol.nombre}",
                datos_nuevos={"rol": rol.nombre, "permisos": permisos}
            )
        except Exception:
            pass

        return {
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": CACHE_PERMISOS_ROL[rol_id]
        }

    @staticmethod
    def eliminar_rol(db: Session, rol_id: int, operador_id: Optional[int] = None) -> Dict[str, str]:
        """Elimina un rol si no tiene usuarios vinculados"""
        if rol_id in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No se pueden eliminar los roles base del sistema (Admin / Cliente)"
            )

        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        if rol.usuarios and len(rol.usuarios) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar el rol porque tiene usuarios asignados. Reasigne los usuarios primero."
            )

        nombre_rol = rol.nombre
        db.delete(rol)
        db.commit()
        CACHE_PERMISOS_ROL.pop(rol_id, None)

        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ELIMINAR_ROL",
                modulo="ROLES",
                usuario_id=operador_id or 1,
                detalle=f"Eliminación del rol {nombre_rol}",
                datos_nuevos={"nombre": nombre_rol}
            )
        except Exception:
            pass

        return {"mensaje": f"Rol {nombre_rol} eliminado correctamente"}


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD (EVITA REGRESIONES)
# ==============================================================================
RoleController = RolController

RolController.get_all = RolController.listar_roles
RolController.get_by_id = RolController.obtener_rol_por_id
RolController.create = RolController.crear_rol
RolController.update = RolController.actualizar_rol
RolController.update_permissions = RolController.actualizar_permisos_rol
RolController.delete = RolController.eliminar_rol
