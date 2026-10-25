# ==============================================================================
# CAPA CONTROLADOR (MVC - CONTROLLER)
# Módulo: CU2 - Gestionar Usuarios y Roles (Multi-Tenant SaaS)
# Ubicación: backend/app/controllers/cu2_gestionar_usuarios_roles/user_controller.py
# ==============================================================================

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.models import (
    Usuario, Rol, Cliente, Venta, 
    MovimientoInventario, Reserva, ReservaDetalle, 
    Carrito, CarritoItem, Notificacion,
    Tenant, PlanSuscripcion
)
from app.schemas.schemas import UsuarioAdminCreate, UsuarioUpdate
from app.core.security import get_password_hash


class UsuarioController:
    """
    Controlador MVC para la gestión de usuarios, asignación de roles,
    control de estado y validación de límites de suscripción por Tenant.
    """

    @staticmethod
    def listar_usuarios(
        db: Session,
        tenant_id: Optional[int] = None,
        search: Optional[str] = None,
        rol_id: Optional[int] = None,
        activo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Usuario]:
        """
        Lista usuarios filtrando por el tenant asignado y criterios opcionales de búsqueda.
        """
        query = db.query(Usuario)

        # Aislamiento por Tenant
        if tenant_id is not None:
            query = query.filter(Usuario.tenant_id == tenant_id)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                (Usuario.nombre.ilike(search_pattern)) |
                (Usuario.apellido.ilike(search_pattern)) |
                (Usuario.email.ilike(search_pattern))
            )

        if rol_id is not None:
            query = query.filter(Usuario.rolid == rol_id)

        if activo is not None:
            query = query.filter(Usuario.activo == activo)

        return query.order_by(Usuario.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_usuario_por_id(
        db: Session,
        user_id: int,
        tenant_id: Optional[int] = None
    ) -> Usuario:
        """
        Obtiene el detalle de un usuario validando pertenencia al tenant.
        """
        query = db.query(Usuario).filter(Usuario.id == user_id)
        if tenant_id is not None:
            query = query.filter(Usuario.tenant_id == tenant_id)

        usuario = query.first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado en este comercio"
            )
        return usuario

    @staticmethod
    def crear_usuario(
        db: Session,
        user_data: UsuarioAdminCreate,
        tenant_id: int = 1,
        operador_id: Optional[int] = None
    ) -> Usuario:
        """
        Registra un nuevo usuario/empleado validando la cuota máxima permitida por el plan del Tenant.
        """
        clean_email = user_data.email.strip().lower()

        # 1. Validar cuota de usuarios según el Plan de Suscripción del Tenant
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant and tenant.plan_id:
            plan = db.query(PlanSuscripcion).filter(PlanSuscripcion.id == tenant.plan_id).first()
            if plan and plan.limite_usuarios:
                # En SaaS comercial, el límite de usuarios aplica a colaboradores y personal administrativo del sistema
                es_colaborador = (user_data.rol_id is None or user_data.rol_id != 2)
                if es_colaborador:
                    total_colaboradores = db.query(Usuario).filter(
                        Usuario.tenant_id == tenant_id,
                        Usuario.activo == True,
                        Usuario.rolid != 2
                    ).count()
                    if total_colaboradores >= plan.limite_usuarios:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=(
                                f"Límite de colaboradores alcanzado: su plan '{plan.nombre}' permite un máximo de "
                                f"{plan.limite_usuarios} usuarios internos/empleados. Actualice su suscripción para registrar más personal."
                            )
                        )
                else:
                    # Límite general de cuentas por tenant si correspondiera
                    total_usuarios = db.query(Usuario).filter(
                        Usuario.tenant_id == tenant_id,
                        Usuario.activo == True
                    ).count()
                    if plan.limite_usuarios and total_usuarios >= (plan.limite_usuarios * 50): # Cap de seguridad clientes
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Límite global alcanzado para el plan '{plan.nombre}'."
                        )

        # 2. Comprobar que el correo no esté duplicado en este Tenant
        existente = db.query(Usuario).filter(
            func.lower(Usuario.email) == clean_email,
            Usuario.tenant_id == tenant_id
        ).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado en este comercio"
            )

        # 3. Hash de contraseña
        password_plano = user_data.password.strip() if (user_data.password and user_data.password.strip()) else "usuario123."
        hashed_pwd = get_password_hash(password_plano)

        nuevo_usuario = Usuario(
            tenant_id=tenant_id,
            nombre=user_data.nombre.strip(),
            apellido=user_data.apellido.strip() if user_data.apellido else None,
            email=clean_email,
            passwordhash=hashed_pwd,
            telefono=user_data.telefono.strip() if user_data.telefono else None,
            rolid=user_data.rol_id,
            activo=user_data.activo if user_data.activo is not None else True,
            verificado=True
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # 4. Si el rol es 'Cliente', crear automáticamente perfil en Cliente
        if nuevo_usuario.rolid == 2:
            try:
                perfil_existente = db.query(Cliente).filter(Cliente.usuarioid == nuevo_usuario.id).first()
                if not perfil_existente:
                    nuevo_cliente = Cliente(
                        tenant_id=tenant_id,
                        usuarioid=nuevo_usuario.id,
                        nombre=nuevo_usuario.nombre,
                        apellido=nuevo_usuario.apellido or "",
                        email=nuevo_usuario.email,
                        telefono=nuevo_usuario.telefono or "",
                        activo=True
                    )
                    db.add(nuevo_cliente)
                    db.commit()
            except Exception:
                pass

        # 5. Registro de auditoría en Bitácora
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CREAR",
                modulo="USUARIOS",
                usuario_id=operador_id or nuevo_usuario.id,
                detalle=f"Creación de usuario: {nuevo_usuario.nombre} ({nuevo_usuario.email}) en tenant #{tenant_id}",
                datos_nuevos={
                    "nombre": nuevo_usuario.nombre,
                    "email": nuevo_usuario.email,
                    "rol_id": nuevo_usuario.rolid,
                    "tenant_id": tenant_id
                }
            )
        except Exception:
            pass

        return nuevo_usuario

    @staticmethod
    def actualizar_usuario(
        db: Session,
        user_id: int,
        user_data: UsuarioUpdate,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Usuario:
        """
        Actualiza los datos personales, rol o estado del usuario.
        """
        usuario = UsuarioController.obtener_usuario_por_id(db, user_id=user_id, tenant_id=tenant_id)

        if user_data.email:
            nuevo_email = user_data.email.strip().lower()
            if nuevo_email != usuario.email.lower():
                existente = db.query(Usuario).filter(
                    func.lower(Usuario.email) == nuevo_email,
                    Usuario.tenant_id == usuario.tenant_id,
                    Usuario.id != usuario.id
                ).first()
                if existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El correo ya se encuentra en uso por otro usuario de este comercio"
                    )
                usuario.email = nuevo_email

        if user_data.nombre is not None:
            usuario.nombre = user_data.nombre.strip()
        if user_data.apellido is not None:
            usuario.apellido = user_data.apellido.strip()
        if user_data.telefono is not None:
            usuario.telefono = user_data.telefono.strip()
        if user_data.rol_id is not None:
            usuario.rolid = user_data.rol_id
        if user_data.activo is not None:
            usuario.activo = user_data.activo

        db.commit()
        db.refresh(usuario)

        # Auditoría
        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="MODIFICAR",
                modulo="USUARIOS",
                usuario_id=operador_id or usuario.id,
                detalle=f"Actualización de usuario: {usuario.nombre} ({usuario.email})",
                datos_nuevos={
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "rol_id": usuario.rolid,
                    "activo": usuario.activo
                }
            )
        except Exception:
            pass

        return usuario

    @staticmethod
    def cambiar_estado_usuario(
        db: Session,
        user_id: int,
        activo: bool,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Usuario:
        """
        Activa o suspende el acceso de un usuario al sistema.
        """
        usuario = UsuarioController.obtener_usuario_por_id(db, user_id=user_id, tenant_id=tenant_id)

        # Evitar suspenderse a sí mismo si es el operador actual
        if operador_id and operador_id == user_id and not activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puede suspender su propia cuenta de usuario activa."
            )

        usuario.activo = activo
        db.commit()
        db.refresh(usuario)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ESTADO",
                modulo="USUARIOS",
                usuario_id=operador_id or usuario.id,
                detalle=f"Cambio de estado del usuario {usuario.email} a {'Activo' if activo else 'Suspendido'}",
                datos_nuevos={"activo": activo}
            )
        except Exception:
            pass

        return usuario

    @staticmethod
    def asignar_rol_usuario(
        db: Session,
        user_id: int,
        rol_id: int,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Usuario:
        """
        Asigna o reasigna el rol de acceso a un usuario.
        """
        usuario = UsuarioController.obtener_usuario_por_id(db, user_id=user_id, tenant_id=tenant_id)

        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El rol seleccionado no existe")

        usuario.rolid = rol_id
        db.commit()
        db.refresh(usuario)

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="CAMBIO_ROL",
                modulo="USUARIOS",
                usuario_id=operador_id or usuario.id,
                detalle=f"Asignación de nuevo rol [{rol.nombre}] a {usuario.email}",
                datos_nuevos={"rol_id": rol_id, "rol_nombre": rol.nombre}
            )
        except Exception:
            pass

        return usuario

    @staticmethod
    def eliminar_usuario(
        db: Session,
        user_id: int,
        tenant_id: Optional[int] = None,
        operador_id: Optional[int] = None
    ) -> Dict[str, str]:
        """
        Elimina de forma segura un usuario si no posee registros transaccionales vinculados.
        """
        usuario = UsuarioController.obtener_usuario_por_id(db, user_id=user_id, tenant_id=tenant_id)

        if operador_id and operador_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar tu propia cuenta mientras estás en sesión."
            )

        # 1. Verificar ventas como cajero/vendedor o como cliente
        cliente = db.query(Cliente).filter(Cliente.usuarioid == user_id).first()
        cliente_id = cliente.id if cliente else -1

        ventas_count = db.query(Venta).filter(
            (Venta.usuarioid == user_id) | (Venta.clienteid == cliente_id)
        ).count()
        if ventas_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar permanentemente este usuario porque tiene ventas o compras registradas. Se recomienda desactivar su acceso."
            )

        # 2. Verificar movimientos de inventario
        movs_count = db.query(MovimientoInventario).filter(MovimientoInventario.usuarioid == user_id).count()
        if movs_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar este usuario porque tiene movimientos de inventario registrados para auditoría. Se recomienda desactivar su acceso."
            )

        # 3. Limpiar reservas vinculadas
        reservas = db.query(Reserva).filter(
            (Reserva.clienteid == user_id) | ((Reserva.clienteid == cliente_id) if cliente else False)
        ).all()
        for res in reservas:
            db.query(ReservaDetalle).filter(ReservaDetalle.reservaid == res.id).delete()
            db.delete(res)

        # 4. Limpiar carritos
        carritos = db.query(Carrito).filter(Carrito.clienteid == user_id).all()
        for car in carritos:
            db.query(CarritoItem).filter(CarritoItem.carritoid == car.id).delete()
            db.delete(car)

        # 5. Limpiar notificaciones
        db.query(Notificacion).filter(Notificacion.usuario_id == user_id).delete()

        # 6. Eliminar perfil cliente si existía
        if cliente:
            db.delete(cliente)

        email_borrado = usuario.email
        db.delete(usuario)
        db.commit()

        try:
            from app.controllers.cu20_gestionar_bitacora.bitacora_controller import BitacoraController
            BitacoraController.registrar_evento(
                db=db,
                accion="ELIMINAR",
                modulo="USUARIOS",
                usuario_id=operador_id or 1,
                detalle=f"Eliminación definitiva del usuario {email_borrado}",
                datos_nuevos={"email": email_borrado}
            )
        except Exception:
            pass

        return {"mensaje": f"Usuario {email_borrado} eliminado correctamente"}


# ==============================================================================
# ALIASES DE RETROCOMPATIBILIDAD (EVITA REGRESIONES)
# ==============================================================================
UserController = UsuarioController

UsuarioController.get_all = UsuarioController.listar_usuarios
UsuarioController.get_by_id = UsuarioController.obtener_usuario_por_id
UsuarioController.create = UsuarioController.crear_usuario
UsuarioController.update = UsuarioController.actualizar_usuario
UsuarioController.toggle_status = UsuarioController.cambiar_estado_usuario
UsuarioController.assign_role = UsuarioController.asignar_rol_usuario
UsuarioController.delete = UsuarioController.eliminar_usuario
