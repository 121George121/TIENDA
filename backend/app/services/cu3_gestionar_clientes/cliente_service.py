# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: Clientes (CU03)
# Ubicación: backend/app/services/cliente_service.py
# ==============================================================================

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import UsuarioModel, RolModel, ClienteModel, VentaModel
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from typing import Optional, List, Dict
from decimal import Decimal

class ClienteService:

    @staticmethod
    def _get_perfil(db: Session, usuario_id: int) -> Optional[ClienteModel]:
        """Fila de perfil extendido (fechanac, genero) en la tabla `cliente`, creada
        automaticamente por el evento after_insert de UsuarioModel (ver models.py)"""
        return db.query(ClienteModel).filter(ClienteModel.usuarioid == usuario_id).first()

    @staticmethod
    def _to_dict(usuario: UsuarioModel, perfil: Optional[ClienteModel], db: Optional[Session] = None) -> Dict:
        total_ordenes = 0
        total_gastado = Decimal('0.00')
        if db:
            ventas_agg = db.query(
                func.count(VentaModel.id),
                func.coalesce(func.sum(VentaModel.total), Decimal('0.00'))
            ).filter(
                (VentaModel.usuarioid == usuario.id) | 
                (VentaModel.clienteid == (perfil.id if perfil else -1))
            ).first()
            if ventas_agg:
                total_ordenes = ventas_agg[0] or 0
                total_gastado = Decimal(str(ventas_agg[1] or '0.00'))

        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "activo": usuario.activo,
            "rol_id": usuario.rolid,
            "created_at": usuario.fechacreacion,
            "fechanac": perfil.fechanac if perfil else None,
            "genero": perfil.genero if perfil else None,
            "total_ordenes": total_ordenes,
            "total_gastado": total_gastado
        }

    @staticmethod
    def _get_cliente_role_id(db: Session) -> int:
        """Obtiene el ID del rol Cliente, creandolo si aun no existe (igual que auth_controller.register_user)"""
        rol_cliente = db.query(RolModel).filter(RolModel.nombre.ilike("Cliente")).first()
        if rol_cliente:
            return rol_cliente.id
        rol_cliente = RolModel(nombre="Cliente", descripcion="Compra en tienda, visualiza catálogo")
        db.add(rol_cliente)
        db.commit()
        db.refresh(rol_cliente)
        return rol_cliente.id

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

        return [
            ClienteService._to_dict(c, ClienteService._get_perfil(db, c.id), db=db)
            for c in clientes
        ]

    @staticmethod
    def get_by_id(db: Session, cliente_id: int) -> Dict:
        """Obtener detalle completo de un cliente por ID"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        return ClienteService._to_dict(cliente, ClienteService._get_perfil(db, cliente.id), db=db)


    @staticmethod
    def create(db: Session, cliente_data: ClienteCreate) -> Dict:
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
        # El evento after_insert de UsuarioModel (models.py) ya creo la fila
        # en `cliente`; solo falta leerla para la respuesta.
        return ClienteService._to_dict(nuevo_cliente, ClienteService._get_perfil(db, nuevo_cliente.id))

    @staticmethod
    def _sync_perfil(db: Session, usuario: UsuarioModel, cliente_data: ClienteUpdate) -> ClienteModel:
        """Crea el perfil si aun no existe (clientes de antes de este cambio) y
        lo mantiene en sincronia con los datos de contacto de `usuario`."""
        perfil = ClienteService._get_perfil(db, usuario.id)
        if not perfil:
            perfil = ClienteModel(usuarioid=usuario.id)
            db.add(perfil)

        perfil.nombre = usuario.nombre
        perfil.apellido = usuario.apellido
        perfil.email = usuario.email
        perfil.telefono = usuario.telefono
        if cliente_data.activo is not None:
            perfil.activo = cliente_data.activo
        if cliente_data.fechanac is not None:
            perfil.fechanac = cliente_data.fechanac
        if cliente_data.genero is not None:
            perfil.genero = cliente_data.genero
        return perfil

    @staticmethod
    def update(db: Session, cliente_id: int, cliente_data: ClienteUpdate) -> Dict:
        """Actualizar información de un cliente existente (cuenta + perfil extendido)"""
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

        perfil = ClienteService._sync_perfil(db, cliente, cliente_data)

        db.commit()
        db.refresh(cliente)
        db.refresh(perfil)
        return ClienteService._to_dict(cliente, perfil)

    @staticmethod
    def toggle_status(db: Session, cliente_id: int, activo: bool) -> Dict:
        """Activar o desactivar estado de cuenta del cliente"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        cliente.activo = activo
        perfil = ClienteService._get_perfil(db, cliente.id)
        if perfil:
            perfil.activo = activo

        db.commit()
        db.refresh(cliente)
        return ClienteService._to_dict(cliente, perfil)

    @staticmethod
    def logical_delete(db: Session, cliente_id: int) -> Dict:
        """Realizar baja lógica de un cliente (activo = False)"""
        cliente = db.query(UsuarioModel).filter(UsuarioModel.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        cliente.activo = False
        perfil = ClienteService._get_perfil(db, cliente.id)
        if perfil:
            perfil.activo = False

        db.commit()
        return {"message": f"Cliente {cliente.nombre} dado de baja lógicamente de forma exitosa", "id": cliente_id}

    @staticmethod
    def get_historial_compras(db: Session, cliente_id: int) -> List[Dict]:
        """Obtener el historial de compras del cliente desde la tabla venta"""
        # cliente_id puede ser usuario.id o perfil cliente.id
        perfil = db.query(ClienteModel).filter(
            (ClienteModel.usuarioid == cliente_id) | (ClienteModel.id == cliente_id)
        ).first()
        perfil_id = perfil.id if perfil else -1

        ventas = db.query(VentaModel).filter(
            (VentaModel.usuarioid == cliente_id) | (VentaModel.clienteid == perfil_id)
        ).order_by(VentaModel.id.desc()).all()

        resultado = []
        for v in ventas:
            detalles_list = []
            for d in v.detalles:
                detalles_list.append({
                    "id": d.ventaid,
                    "producto_id": d.variante.productoid if d.variante else 0,
                    "cantidad": d.cantidad,
                    "precio_unitario": d.preciounitario,
                    "subtotal": d.subtotal
                })
            resultado.append({
                "id": v.id,
                "usuario_id": v.usuarioid,
                "total": v.total,
                "estado": v.estado,
                "direccion_envio": "Entrega en Tienda / Dirección Registrada",
                "created_at": v.fecha,
                "detalles": detalles_list
            })
        return resultado

    @staticmethod
    def get_historial_reservas(db: Session, cliente_id: int) -> List[Dict]:
        """Obtener historial de reservas del cliente"""
        return []

