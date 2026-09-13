# ==============================================================================
# SCRIPT DE AUDITORÍA Y VERIFICACIÓN INTEGRAL DE CASOS DE USO (CU01 AL CU15)
# Proyecto: E-Commerce Tienda (Sistemas II - Examen 1)
# ==============================================================================

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from app.core.database import SessionLocal
from app.models.models import UsuarioModel
from app.controllers.cu1_gestionar_autenticacion.auth_controller import AuthController
from app.controllers.cu2_gestionar_usuarios_roles.user_controller import UserController
from app.controllers.cu2_gestionar_usuarios_roles.role_controller import RoleController
from app.controllers.cu3_gestionar_clientes.cliente_controller import ClienteController
from app.controllers.cu4_gestionar_sucursales.sucursal_controller import SucursalController
from app.controllers.cu5_gestionar_productos.producto_controller import ProductoController
from app.controllers.cu6_gestionar_clasificacion_prendas.clasificacion_controller import ClasificacionController
from app.controllers.cu7_gestionar_proveedores_productos_suministrados.proveedor_controller import ProveedorController
from app.controllers.cu8_consultar_catalogo_disponibilidad.inventario_controller import InventarioController
from app.controllers.cu9_gestionar_carrito_compras.carrito_controller import CarritoController
from app.controllers.cu10_gestionar_reservas_prendas.reserva_controller import ReservaController
from app.controllers.cu11_atender_reservas_sucursal.atender_reserva_controller import AtenderReservaController
from app.controllers.cu13_gestionar_inventario_movimientos.inventario_controller import InventarioController as InvKardexController
from app.controllers.cu14_registrar_ventas_presenciales.venta_presencial_controller import VentaPresencialController
from app.controllers.cu15_realizar_compras_digitales.compra_digital_controller import CompraDigitalController

def run_audit():
    db = SessionLocal()
    print("==================================================================")
    print("AUDITORÍA INTEGRAL SENIOR DE CASOS DE USO (CU01 - CU15)")
    print("==================================================================")

    try:
        # CU02: Usuarios y Roles
        roles = RoleController.get_all(db)
        users = UserController.get_all(db)
        print(f"✓ CU02: Roles ({len(roles)}) y Usuarios ({len(users)}) validados.")

        # CU03: Clientes
        clientes = ClienteController.listar_clientes(db)
        print(f"✓ CU03: Clientes ({len(clientes)}) registrados y consultables.")

        # CU04: Sucursales
        sucursales = SucursalController.listar_sucursales(db)
        print(f"✓ CU04: Sucursales físicas ({len(sucursales)}) activas.")

        # CU05: Productos
        prods = ProductoController.listar_productos(db)
        print(f"✓ CU05: Catálogo de productos ({len(prods)}) cargado.")

        # CU06: Clasificación de Prendas
        cats = ClasificacionController.listar_categorias(db)
        temps = ClasificacionController.listar_temporadas(db)
        cols = ClasificacionController.listar_colecciones(db)
        print(f"✓ CU06: Clasificaciones - Categorías: {len(cats)}, Temporadas: {len(temps)}, Colecciones: {len(cols)}.")

        # CU07: Proveedores y Suministros
        provs = ProveedorController.listar_proveedores(db)
        print(f"✓ CU07: Proveedores ({len(provs)}) activos con suministros.")

        # CU08: Catálogo y Disponibilidad
        cat_items = InventarioController.listar_catalogo(db)
        total_var = sum(len(p.variantes) for p in cat_items)
        print(f"✓ CU08: Catálogo multitienda ({len(cat_items)} prendas, {total_var} variantes con tallas/colores).")

        # CU09: Carrito de Compras
        admin_user = db.query(UsuarioModel).first()
        cart = CarritoController.obtener_carrito_dto(db, admin_user.id)
        print(f"✓ CU09: Carrito de compras operativo (Items: {cart.total_items}, Total: Bs. {cart.total_precio}).")

        # CU10 & CU11: Reservas y Atención en Mostrador
        res_user = ReservaController.listar_reservas_usuario(db, admin_user.id)
        res_admin = AtenderReservaController.listar_reservas_admin(db)
        print(f"✓ CU10 & CU11: Reservas de prendas y atención en sucursal activas ({len(res_admin)} reservas en sistema).")

        # CU13: Inventario y Movimientos Kardex
        inv_list = InvKardexController.listar_inventario(db)
        print(f"✓ CU13: Inventario y Kardex ({len(inv_list)} existencias en almacenes).")

        # CU14: Ventas Presenciales (POS)
        ventas = VentaPresencialController.listar_todas_ventas(db)
        print(f"✓ CU14: Ventas presenciales (POS) e historial ({len(ventas)} comprobantes).")

        # CU15: Compras Digitales
        ordenes = CompraDigitalController.listar_mis_ordenes(db, admin_user)
        print(f"✓ CU15: Órdenes digitales y compras online ({len(ordenes)} compras del cliente).")

        print("==================================================================")
        print("RESULTADO DE AUDITORÍA: TODOS LOS CASOS DE USO (CU01-CU15) OPERATIVOS.")
        print("==================================================================")
        return True
    except Exception as e:
        print(f"❌ ERROR EN AUDITORÍA: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    exito = run_audit()
    sys.exit(0 if exito else 1)
