# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Gestión de Roles y Permisos
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import RolModel
from app.schemas.schemas import RolCreate
from fastapi import HTTPException, status
from typing import List, Dict

# Simulación de almacenamiento/asociación de permisos por rol sin alterar la BD existente
# (se persiste en el campo descripcion o diccionario en memoria con defaults)
DEFAULT_PERMISSIONS: Dict[str, List[str]] = {
    "ADMIN": [
        "USUARIOS_LISTAR", "USUARIOS_CREAR", "USUARIOS_EDITAR", "USUARIOS_ESTADO", "USUARIOS_ROL",
        "ROLES_LISTAR", "ROLES_CREAR", "ROLES_EDITAR", "ROLES_PERMISOS",
        "PRODUCTOS_LISTAR", "PRODUCTOS_CREAR", "PRODUCTOS_EDITAR", "PRODUCTOS_ELIMINAR",
        "ORDENES_LISTAR", "ORDENES_GESTIONAR"
    ],
    "CLIENTE": [
        "PRODUCTOS_LISTAR", "ORDENES_CREAR", "ORDENES_LISTAR_PROPIAS"
    ]
}

ROLE_PERMISSIONS_CACHE: Dict[int, List[str]] = {}

class RoleController:

    @staticmethod
    def get_permissions_for_role(rol: RolModel) -> List[str]:
        if rol.id in ROLE_PERMISSIONS_CACHE:
            return ROLE_PERMISSIONS_CACHE[rol.id]
        
        nombre_upper = (rol.nombre or "").upper()
        if nombre_upper in DEFAULT_PERMISSIONS:
            return DEFAULT_PERMISSIONS[nombre_upper]
            
        # Si no tiene permisos asignados previamente, retornamos permisos básicos de lectura
        return ["PRODUCTOS_LISTAR"]

    @staticmethod
    def get_all(db: Session):
        roles = db.query(RolModel).order_by(RolModel.id.asc()).all()
        result = []
        for r in roles:
            permisos = RoleController.get_permissions_for_role(r)
            result.append({
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "permisos": permisos
            })
        return result

    @staticmethod
    def get_by_id(db: Session, rol_id: int):
        rol = db.query(RolModel).filter(RolModel.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        permisos = RoleController.get_permissions_for_role(rol)
        return {
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": permisos
        }

    @staticmethod
    def create(db: Session, rol_data: RolCreate):
        existente = db.query(RolModel).filter(RolModel.nombre == rol_data.nombre).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del rol ya existe")

        nuevo_rol = RolModel(
            nombre=rol_data.nombre,
            descripcion=rol_data.descripcion
        )
        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)

        if rol_data.permisos is not None:
            ROLE_PERMISSIONS_CACHE[nuevo_rol.id] = rol_data.permisos
        else:
            ROLE_PERMISSIONS_CACHE[nuevo_rol.id] = ["PRODUCTOS_LISTAR"]

        return {
            "id": nuevo_rol.id,
            "nombre": nuevo_rol.nombre,
            "descripcion": nuevo_rol.descripcion,
            "permisos": ROLE_PERMISSIONS_CACHE[nuevo_rol.id]
        }

    @staticmethod
    def update(db: Session, rol_id: int, rol_data: RolCreate):
        rol = db.query(RolModel).filter(RolModel.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        if rol_data.nombre and rol_data.nombre != rol.nombre:
            existente = db.query(RolModel).filter(RolModel.nombre == rol_data.nombre).first()
            if existente:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del rol ya existe")
            rol.nombre = rol_data.nombre

        if rol_data.descripcion is not None:
            rol.descripcion = rol_data.descripcion

        db.commit()
        db.refresh(rol)

        if rol_data.permisos is not None:
            ROLE_PERMISSIONS_CACHE[rol.id] = rol_data.permisos

        permisos = RoleController.get_permissions_for_role(rol)
        return {
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": permisos
        }

    @staticmethod
    def update_permissions(db: Session, rol_id: int, permisos: List[str]):
        rol = db.query(RolModel).filter(RolModel.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

        ROLE_PERMISSIONS_CACHE[rol.id] = permisos
        return {
            "id": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": permisos
        }

    @staticmethod
    def delete(db: Session, rol_id: int):
        rol = db.query(RolModel).filter(RolModel.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        db.delete(rol)
        db.commit()
        if rol_id in ROLE_PERMISSIONS_CACHE:
            del ROLE_PERMISSIONS_CACHE[rol_id]
        return {"message": "Rol eliminado correctamente"}

