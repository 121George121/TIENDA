# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: Clientes (CU03)
# Ubicación: backend/app/services/cliente_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from app.models.models import UsuarioModel, RolModel
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from typing import Optional, List, Dict
from decimal import Decimal

class ClienteService:

    @staticmethod
    def _get_cliente_role_id(db: Session) -> int:
        """Obtiene el ID del rol CLIENTE de la base de datos o retorna 2 por defecto"""
        rol_cliente = db.query(RolModel).filter(RolModel.nombre.ilike("CLIENTE")).first()
        if rol_cliente:
            return rol_cliente.id
        return 2

    @staticmethod
    def get_all(
        db: Session, 
        search: Optional[str] = None, 
        activo: Optional[bool] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict]:
        """Listar clientes con opción de búsqueda por nombre, correo o teléfono y filtro de estado"""
        rol_cliente_id = ClienteService._get_cliente_role_id(db)
        
        query = db.query(UsuarioModel).filter(UsuarioModel.rolid == rol_cliente_id)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (UsuarioModel.nombre.ilike(pattern)) |
                (UsuarioModel.apellido.ilike(pattern)) |
                (UsuarioModel.email.ilike(pattern)) |
                (UsuarioModel.telefono.ilike(pattern))
            )

        if activo is not None:
            query = query.filter(UsuarioModel.activo == activo)

        clientes = query.order_by(UsuarioModel.id.desc()).offset(skip).limit(limit).all()

        resultado = []
        for c in clientes:
            resultado.append({
                "id": c.id,
                "nombre": c.nombre,
                "apellido": c.apellido,
                "email": c.email,
                "telefono": c.telefono,
                "activo": c.activo,
                "rol_id": c.rolid,
                "created_at": c.fechacreacion,
                "total_ordenes": 0,
                "total_gastado": Decimal('0.00')
            })

        return resultado

    @staticmethod
    def get_by_id(db: Session, cliente_id: int) -> Dict:
        """Obtener detalle completo de un cliente por ID"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        return {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "email": cliente.email,
            "telefono": cliente.telefono,
            "activo": cliente.activo,
            "rol_id": cliente.rolid,
            "created_at": cliente.fechacreacion,
            "total_ordenes": 0,
            "total_gastado": Decimal('0.00')
        }

    @staticmethod
    def create(db: Session, cliente_data: ClienteCreate) -> UsuarioModel:
        """Registrar un nuevo cliente en el sistema"""
        existente = db.query(UsuarioModel).filter(UsuarioModel.email == cliente_data.email).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El correo electrónico ya se encuentra registrado"
            )

        rol_cliente_id = ClienteService._get_cliente_role_id(db)
        hashed_pwd = get_password_hash(cliente_data.password)

        nuevo_cliente = UsuarioModel(
            nombre=cliente_data.nombre,
            apellido=cliente_data.apellido,
            email=cliente_data.email,
            passwordhash=hashed_pwd,
            telefono=cliente_data.telefono,
            rolid=rol_cliente_id,
            activo=True
        )

        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente

    @staticmethod
    def update(db: Session, cliente_id: int, cliente_data: ClienteUpdate) -> UsuarioModel:
        """Actualizar información de un cliente existente"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        if cliente_data.email and cliente_data.email != cliente.email:
            existente = db.query(UsuarioModel).filter(UsuarioModel.email == cliente_data.email).first()
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="El correo ya pertenece a otro usuario"
                )
            cliente.email = cliente_data.email

        if cliente_data.nombre is not None:
            cliente.nombre = cliente_data.nombre
        if cliente_data.apellido is not None:
            cliente.apellido = cliente_data.apellido
        if cliente_data.telefono is not None:
            cliente.telefono = cliente_data.telefono
        if cliente_data.activo is not None:
            cliente.activo = cliente_data.activo

        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def toggle_status(db: Session, cliente_id: int, activo: bool) -> UsuarioModel:
        """Activar o desactivar estado de cuenta del cliente"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        cliente.activo = activo
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def logical_delete(db: Session, cliente_id: int) -> Dict:
        """Realizar baja lógica de un cliente (activo = False)"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        cliente.activo = False
        db.commit()
        return {"message": f"Cliente {cliente.nombre} dado de baja lógicamente de forma exitosa", "id": cliente_id}

    @staticmethod
    def get_historial_compras(db: Session, cliente_id: int) -> List[Dict]:
        """Obtener el historial de compras del cliente"""
        return []

    @staticmethod
    def get_historial_reservas(db: Session, cliente_id: int) -> List[Dict]:
        """Obtener historial de reservas del cliente"""
        return []
