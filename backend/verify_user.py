import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.models import UsuarioModel
from app.core.security import verify_password, get_password_hash

db = SessionLocal()
try:
    user = db.query(UsuarioModel).filter(UsuarioModel.email == "diogomars2026@gmail.com").first()
    if user:
        print(f"Usuario encontrado: ID={user.id}, Email={user.email}, Activo={user.activo}")
        match = verify_password("Admin123.", user.passwordhash)
        print(f"¿La contraseña 'Admin123.' coincide con el hash almacenado?: {match}")
        if not match:
            print("Re-hasheando contraseña a 'Admin123.'...")
            user.passwordhash = get_password_hash("Admin123.")
            db.commit()
            print("Contraseña actualizada correctamente.")
    else:
        print("Usuario 'diogomars2026@gmail.com' no encontrado en la base de datos.")
finally:
    db.close()
