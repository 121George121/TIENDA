from app.core.database import SessionLocal
from app.models.models import UsuarioModel, RolModel
from app.core.security import get_password_hash

db = SessionLocal()
try:
    admin_rol = db.query(RolModel).filter(RolModel.nombre == 'ADMIN').first()
    cliente_rol = db.query(RolModel).filter(RolModel.nombre == 'CLIENTE').first()
    cajero_rol = db.query(RolModel).filter(RolModel.nombre.ilike('%CAJERO%')).first()

    users_to_create = [
        {
            'email': 'admin@tienda.com',
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'password': 'Admin123.',
            'rolid': admin_rol.id if admin_rol else 1,
            'sucursalid': None,
            'activo': True,
            'verificado': True
        },
        {
            'email': 'diogomars2026@gmail.com',
            'nombre': 'Diogo',
            'apellido': 'Mars',
            'password': 'Admin123.',
            'rolid': admin_rol.id if admin_rol else 1,
            'sucursalid': None,
            'activo': True,
            'verificado': True
        },
        {
            'email': 'jorgealanoca2005@gmail.com',
            'nombre': 'Jorge',
            'apellido': 'Alanoca',
            'password': 'Admin123.',
            'rolid': admin_rol.id if admin_rol else 1,
            'sucursalid': None,
            'activo': True,
            'verificado': True
        },
        {
            'email': 'cajero@tienda.com',
            'nombre': 'Carlos',
            'apellido': 'Cajero',
            'password': 'Cajero123.',
            'rolid': cajero_rol.id if cajero_rol else 3,
            'sucursalid': 1,
            'activo': True,
            'verificado': True
        },
        {
            'email': 'cliente@tienda.com',
            'nombre': 'Cliente',
            'apellido': 'Prueba',
            'password': 'Cliente123.',
            'rolid': cliente_rol.id if cliente_rol else 2,
            'sucursalid': None,
            'activo': True,
            'verificado': True
        }
    ]

    for u in users_to_create:
        exist = db.query(UsuarioModel).filter(UsuarioModel.email == u['email']).first()
        if not exist:
            new_u = UsuarioModel(
                email=u['email'],
                nombre=u['nombre'],
                apellido=u['apellido'],
                passwordhash=get_password_hash(u['password']),
                rolid=u['rolid'],
                sucursalid=u.get('sucursalid'),
                activo=u['activo'],
                verificado=u['verificado']
            )
            db.add(new_u)
            print(f"Usuario creado exitosamente: {u['email']}")
        else:
            exist.passwordhash = get_password_hash(u['password'])
            if u.get('sucursalid') is not None:
                exist.sucursalid = u['sucursalid']
            exist.activo = True
            exist.verificado = True
            print(f"Usuario actualizado exitosamente: {u['email']}")

    db.commit()
    print("OK: Todos los usuarios iniciales han sido registrados y activados.")
finally:
    db.close()
