# ==============================================================================
# CAPA SERVICIO (MVC - SERVICE)
# Módulo: CU3 - Gestionar Clientes (Multi-Tenant SaaS)
# Ubicación: backend/app/services/cu3_gestionar_clientes/cliente_service.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.models import Usuario, Rol, Cliente, Venta, Reserva, Bitacora
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate
from app.core.security import get_password_hash


class ClienteService:
    """
    Servicio de dominio para la gestión del ciclo de vida del Cliente,
    aislamiento estricto por Tenant, métricas comerciales y auditoría.
    """

    @staticmethod
    def _obtener_perfil(db: Session, usuario_id: int, tenant_id: Optional[int] = None) -> Optional[Cliente]:
        """Obtiene la fila de perfil extendido en la tabla 'cliente'"""
        query = db.query(Cliente).filter(Cliente.usuarioid == usuario_id)
        if tenant_id is not None:
            query = query.filter(Cliente.tenant_id == tenant_id)
        return query.first()

    @staticmethod
    def _to_dict(usuario: Usuario, perfil: Optional[Cliente], db: Optional[Session] = None, tenant_id: Optional[int] = None) -> Dict[str, Any]:
        """Convierte las entidades Usuario y Cliente al formato estructurado de respuesta con métricas"""
        total_ordenes = 0
        total_gastado = Decimal('0.00')

        if db:
            query_ventas = db.query(
                func.count(Venta.id),
                func.coalesce(func.sum(Venta.total), Decimal('0.00'))
            ).filter(
                (Venta.usuarioid == usuario.id) | 
                (Venta.clienteid == (perfil.id if perfil else -1))
            )
            if tenant_id is not None:
                query_ventas = query_ventas.filter(Venta.tenant_id == tenant_id)

            ventas_agg = query_ventas.first()
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
    def _obtener_rol_cliente_id(db: Session) -> int:
        """Obtiene el ID del rol 'Cliente', asegurando su existencia en la base de datos"""
        rol_cliente = db.query(Rol).filter(Rol.nombre.ilike("Cliente")).first()
        if rol_cliente:
            return rol_cliente.id
        rol_cliente = Rol(nombre="Cliente", descripcion="Compra en tienda, visualiza catálogo y reserva prendas")
        db.add(rol_cliente)
        db.commit()
        db.refresh(rol_cliente)
        return rol_cliente.id

    @staticmethod
    def listar_clientes(
        db: Session,
        tenant_id: int = 1,
        search: Optional[str] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Lista clientes pertenecientes al tenant aplicando filtros de búsqueda y estado.
        Garantiza el aislamiento de clientes por comercio (Multi-Tenant).
        """
        rol_cliente_id = ClienteService._obtener_rol_cliente_id(db)
        query = db.query(Usuario).filter(
            Usuario.tenant_id == tenant_id,
            Usuario.rolid == rol_cliente_id
        )

        if search:
            clean_search = f"%{search.strip()}%"
            query = query.filter(
                (Usuario.nombre.ilike(clean_search)) |
                (Usuario.apellido.ilike(clean_search)) |
                (Usuario.email.ilike(clean_search)) |
                (Usuario.telefono.ilike(clean_search))
            )

        if activo is not None:
            query = query.filter(Usuario.activo == activo)

        clientes = query.order_by(Usuario.id.desc()).offset(skip).limit(limit).all()

        return [
            ClienteService._to_dict(
                c, 
                ClienteService._obtener_perfil(db, c.id, tenant_id=tenant_id), 
                db=db, 
                tenant_id=tenant_id
            )
            for c in clientes
        ]

    @staticmethod
    def obtener_cliente_por_id(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene el detalle de un cliente validando el aislamiento por Tenant.
        Permite buscar por el ID de Usuario o por el ID de la tabla Cliente.
        """
        query_usuario = db.query(Usuario).filter(Usuario.id == cliente_id)
        if tenant_id is not None:
            query_usuario = query_usuario.filter(Usuario.tenant_id == tenant_id)
        cliente = query_usuario.first()

        # Si no se encuentra como Usuario.id, intentar buscar por Cliente.id
        if not cliente:
            query_perfil = db.query(Cliente).filter(Cliente.id == cliente_id)
            if tenant_id is not None:
                query_perfil = query_perfil.filter(Cliente.tenant_id == tenant_id)
            perfil_encontrado = query_perfil.first()
            if perfil_encontrado:
                cliente = db.query(Usuario).filter(Usuario.id == perfil_encontrado.usuarioid).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Cliente no encontrado en este comercio"
            )

        perfil = ClienteService._obtener_perfil(db, cliente.id, tenant_id=tenant_id)
        return ClienteService._to_dict(cliente, perfil, db=db, tenant_id=tenant_id)

    @staticmethod
    def crear_cliente(
        db: Session,
        cliente_data: ClienteCreate,
        tenant_id: int = 1,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Registra un nuevo cliente con aislamiento de Tenant, creando su cuenta de acceso
        y su perfil extendido para registro de compras y reservas.
        """
        clean_email = cliente_data.email.strip().lower()

        # Unicidad de correo por Tenant
        existente = db.query(Usuario).filter(
            func.lower(Usuario.email) == clean_email,
            Usuario.tenant_id == tenant_id
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado en este comercio"
            )

        rol_cliente_id = ClienteService._obtener_rol_cliente_id(db)
        hashed_pwd = get_password_hash(cliente_data.password.strip())

        # 1. Crear registro en Usuario
        nuevo_usuario = Usuario(
            tenant_id=tenant_id,
            nombre=cliente_data.nombre.strip(),
            apellido=cliente_data.apellido.strip() if cliente_data.apellido else None,
            email=clean_email,
            passwordhash=hashed_pwd,
            telefono=cliente_data.telefono.strip() if cliente_data.telefono else None,
            rolid=rol_cliente_id,
            activo=True,
            verificado=True
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # 2. Crear registro en Cliente (perfil extendido)
        nuevo_perfil = Cliente(
            tenant_id=tenant_id,
            usuarioid=nuevo_usuario.id,
            nombre=nuevo_usuario.nombre,
            apellido=nuevo_usuario.apellido or "",
            email=nuevo_usuario.email,
            telefono=nuevo_usuario.telefono or "",
            activo=True
        )
        db.add(nuevo_perfil)
        db.commit()
        db.refresh(nuevo_perfil)

        # 3. Auditoría en Bitácora (CU20)
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR_CLIENTE",
                modulo="CLIENTES",
                usuario_id=operador_id or nuevo_usuario.id,
                detalle=f"Registro de nuevo cliente: {nuevo_usuario.nombre} {nuevo_usuario.apellido or ''} ({nuevo_usuario.email}) en tenant #{tenant_id}",
                datos_nuevos={
                    "usuario_id": nuevo_usuario.id,
                    "cliente_id": nuevo_perfil.id,
                    "nombre": nuevo_usuario.nombre,
                    "email": nuevo_usuario.email,
                    "tenant_id": tenant_id
                }
            )
        except Exception:
            pass

        return ClienteService._to_dict(nuevo_usuario, nuevo_perfil, db=db, tenant_id=tenant_id)

    @staticmethod
    def _sincronizar_perfil(db: Session, usuario: Usuario, cliente_data: ClienteUpdate, tenant_id: int) -> Cliente:
        """Sincroniza y mantiene coherente el perfil de cliente asociado"""
        perfil = ClienteService._obtener_perfil(db, usuario.id, tenant_id=tenant_id)
        if not perfil:
            perfil = Cliente(
                tenant_id=tenant_id,
                usuarioid=usuario.id,
                nombre=usuario.nombre,
                apellido=usuario.apellido or "",
                email=usuario.email,
                telefono=usuario.telefono or "",
                activo=usuario.activo
            )
            db.add(perfil)

        perfil.nombre = usuario.nombre
        perfil.apellido = usuario.apellido or ""
        perfil.email = usuario.email
        perfil.telefono = usuario.telefono or ""
        if cliente_data.activo is not None:
            perfil.activo = cliente_data.activo
        if cliente_data.fechanac is not None:
            perfil.fechanac = cliente_data.fechanac
        if cliente_data.genero is not None:
            perfil.genero = cliente_data.genero
        return perfil

    @staticmethod
    def actualizar_cliente(
        db: Session,
        cliente_id: int,
        cliente_data: ClienteUpdate,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Actualiza los datos personales, de contacto y perfil de un cliente"""
        query = db.query(Usuario).filter(Usuario.id == cliente_id)
        if tenant_id is not None:
            query = query.filter(Usuario.tenant_id == tenant_id)
        cliente = query.first()

        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        if cliente_data.email:
            clean_email = cliente_data.email.strip().lower()
            if clean_email != cliente.email.lower():
                existente = db.query(Usuario).filter(
                    func.lower(Usuario.email) == clean_email,
                    Usuario.tenant_id == cliente.tenant_id,
                    Usuario.id != cliente.id
                ).first()
                if existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El correo electrónico ya pertenece a otro usuario de este comercio"
                    )
                cliente.email = clean_email

        if cliente_data.nombre is not None:
            cliente.nombre = cliente_data.nombre.strip()
        if cliente_data.apellido is not None:
            cliente.apellido = cliente_data.apellido.strip()
        if cliente_data.telefono is not None:
            cliente.telefono = cliente_data.telefono.strip()
        if cliente_data.activo is not None:
            cliente.activo = cliente_data.activo

        perfil = ClienteService._sincronizar_perfil(db, cliente, cliente_data, tenant_id=cliente.tenant_id)

        db.commit()
        db.refresh(cliente)
        db.refresh(perfil)

        # Auditoría
        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ACTUALIZAR_CLIENTE",
                modulo="CLIENTES",
                usuario_id=operador_id or cliente.id,
                detalle=f"Actualización de datos del cliente {cliente.email}",
                datos_nuevos={"nombre": cliente.nombre, "email": cliente.email, "activo": cliente.activo}
            )
        except Exception:
            pass

        return ClienteService._to_dict(cliente, perfil, db=db, tenant_id=cliente.tenant_id)

    @staticmethod
    def cambiar_estado_cliente(
        db: Session,
        cliente_id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Activa o suspende el acceso del cliente en el tenant"""
        query = db.query(Usuario).filter(Usuario.id == cliente_id)
        if tenant_id is not None:
            query = query.filter(Usuario.tenant_id == tenant_id)
        cliente = query.first()

        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        cliente.activo = activo
        perfil = ClienteService._obtener_perfil(db, cliente.id, tenant_id=cliente.tenant_id)
        if perfil:
            perfil.activo = activo

        db.commit()
        db.refresh(cliente)

        try:
            from app.controllers.cu26_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO_CLIENTE",
                modulo="CLIENTES",
                usuario_id=operador_id or cliente.id,
                detalle=f"Cambio de estado del cliente {cliente.email} a {'Activo' if activo else 'Inactivo'}",
                datos_nuevos={"activo": activo}
            )
        except Exception:
            pass

        return ClienteService._to_dict(cliente, perfil, db=db, tenant_id=cliente.tenant_id)

    @staticmethod
    def dar_baja_logica_cliente(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Realiza la baja lógica (activo = False) preservando historial de ventas y reservas"""
        resultado = ClienteService.cambiar_estado_cliente(
            db=db,
            cliente_id=cliente_id,
            activo=False,
            tenant_id=tenant_id,
            operador_id=operador_id
        )
        return {
            "message": f"Cliente {resultado['nombre']} dado de baja lógicamente de forma exitosa",
            "id": cliente_id,
            "activo": False
        }

    @staticmethod
    def obtener_historial_compras(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene el historial de compras u órdenes realizadas por el cliente en el Tenant"""
        perfil = db.query(Cliente).filter(
            (Cliente.usuarioid == cliente_id) | (Cliente.id == cliente_id)
        )
        if tenant_id is not None:
            perfil = perfil.filter(Cliente.tenant_id == tenant_id)
        perfil_obj = perfil.first()
        perfil_id = perfil_obj.id if perfil_obj else -1

        query = db.query(Venta).filter(
            (Venta.usuarioid == cliente_id) | (Venta.clienteid == perfil_id)
        )
        if tenant_id is not None:
            query = query.filter(Venta.tenant_id == tenant_id)

        ventas = query.order_by(Venta.id.desc()).all()
        resultado = []
        for v in ventas:
            detalles_list = []
            for d in v.detalles:
                detalles_list.append({
                    "id": d.ventaid,
                    "producto_id": d.variante.productoid if (hasattr(d, 'variante') and d.variante) else 0,
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
    def obtener_historial_reservas(
        db: Session,
        cliente_id: int,
        tenant_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene el historial de reservas de prendas del cliente en las sucursales del Tenant"""
        perfil = db.query(Cliente).filter(
            (Cliente.usuarioid == cliente_id) | (Cliente.id == cliente_id)
        )
        if tenant_id is not None:
            perfil = perfil.filter(Cliente.tenant_id == tenant_id)
        perfil_obj = perfil.first()
        perfil_id = perfil_obj.id if perfil_obj else -1

        query = db.query(Reserva).filter(
            (Reserva.clienteid == perfil_id) | (Reserva.clienteid == cliente_id)
        )
        if tenant_id is not None:
            query = query.filter(Reserva.tenant_id == tenant_id)

        reservas = query.order_by(Reserva.id.desc()).all()
        resultado = []
        for r in reservas:
            resultado.append({
                "id": r.id,
                "cliente_id": r.clienteid,
                "codigo_reserva": r.codigoreserva,
                "fecha_reserva": r.fechareserva,
                "estado": r.estado,
                "total_estimado": Decimal('0.00'),
                "notas": r.observaciones or "Sin observaciones"
            })
        return resultado


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD
# ==============================================================================
ClienteService.get_all = ClienteService.listar_clientes
ClienteService.get_by_id = ClienteService.obtener_cliente_por_id
ClienteService.create = ClienteService.crear_cliente
ClienteService.update = ClienteService.actualizar_cliente
ClienteService.toggle_status = ClienteService.cambiar_estado_cliente
ClienteService.logical_delete = ClienteService.dar_baja_logica_cliente
ClienteService.get_historial_compras = ClienteService.obtener_historial_compras
ClienteService.get_historial_reservas = ClienteService.obtener_historial_reservas
