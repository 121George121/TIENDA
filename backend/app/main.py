# ==============================================================================
# ENTRY POINT - FASTAPI APPLICATION
# Proyecto: ECOMMERCE_TIENDA (Arquitectura MVC)
# ==============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import models  # Registra todos los modelos ORM
from app.views.cu1_gestionar_autenticacion import auth_views
from app.views.cu2_gestionar_usuarios_roles import user_views, role_views
from app.views.cu3_gestionar_clientes import cliente_views
from app.views.cu4_gestionar_sucursales import sucursal_views
from app.views.cu5_gestionar_productos import producto_views
from app.views.cu6_gestionar_clasificacion_prendas import clasificacion_views
from app.views.cu7_gestionar_proveedores_productos_suministrados import proveedor_views
from app.views.cu8_consultar_catalogo_disponibilidad import catalogo_views
from app.views.cu9_gestionar_carrito_compras import carrito_views
from app.views.cu10_gestionar_reservas_prendas import reserva_views
from app.views.cu11_atender_reservas_sucursal import atender_reserva_views
from app.views.cu12_vestidor_virtual_ia import vestidor_ia_views
from app.views.cu13_gestionar_inventario_movimientos import inventario_views
from app.views.cu14_registrar_ventas_presenciales import venta_presencial_views
from app.views.cu15_realizar_compras_digitales import compra_digital_views
from app.views.cu16_gestionar_pagos_comprobantes import pago_views
from app.views.cu17_consultar_historial_compras_reservas import historial_views
from app.views.cu18_gestionar_recomendaciones_ia import recomendacion_views
from app.views.cu19_gestionar_notificaciones import notificacion_views
from app.views.cu20_generar_reportes_dashboards import reporte_views
from app.views.cu20_gestionar_bitacora import bitacora_views

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful siguiendo el patrón de arquitectura Modelo-Vista-Controlador (MVC)"
)

def sync_db_sequences():
    """Sincroniza automáticamente las secuencias seriales de PostgreSQL con el MAX(id) real"""
    try:
        with engine.begin() as conn:
            from sqlalchemy import text
            import re
            query = text("""
                SELECT table_name, column_name, column_default 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND column_default LIKE 'nextval%'
            """)
            cols = conn.execute(query).fetchall()
            for table_name, column_name, column_default in cols:
                match = re.search(r"nextval\('([^']+)'", column_default)
                if match:
                    seq_name = match.group(1)
                    try:
                        max_id = conn.execute(text(f'SELECT COALESCE(MAX("{column_name}"), 0) FROM "{table_name}"')).scalar()
                        if max_id > 0:
                            conn.execute(text(f"SELECT setval('{seq_name}', {max_id}, true)"))
                        else:
                            conn.execute(text(f"SELECT setval('{seq_name}', 1, false)"))
                    except Exception:
                        pass
        print("[DB] Secuencias PostgreSQL resincronizadas automáticamente.")
    except Exception as e:
        print(f"[DB WARN] No se pudieron sincronizar secuencias: {e}")

@app.on_event("startup")
def on_startup():
    try:
        # Crear automáticamente las tablas en PostgreSQL si aún no existen
        Base.metadata.create_all(bind=engine)
        print("[DB] Tablas de la base de datos sincronizadas correctamente.")
        sync_db_sequences()
    except Exception as e:
        print(f"[DB WARN] Advertencia al conectar con la base de datos: {e}")

# Configuración de CORS para permitir conexiones desde Angular y Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las Vistas / Rutas (Routers / API Endpoints en Capa Vista - MVC)
app.include_router(auth_views.router, prefix=settings.API_V1_STR)
app.include_router(user_views.router, prefix=settings.API_V1_STR)
app.include_router(role_views.router, prefix=settings.API_V1_STR)
app.include_router(cliente_views.router, prefix=settings.API_V1_STR)
app.include_router(sucursal_views.router, prefix=settings.API_V1_STR)
app.include_router(clasificacion_views.router, prefix=settings.API_V1_STR)
app.include_router(producto_views.router, prefix=settings.API_V1_STR)
app.include_router(proveedor_views.router, prefix=settings.API_V1_STR)
app.include_router(catalogo_views.router, prefix=settings.API_V1_STR)
app.include_router(carrito_views.router, prefix=settings.API_V1_STR)
app.include_router(vestidor_ia_views.router, prefix=settings.API_V1_STR)
app.include_router(atender_reserva_views.router, prefix=settings.API_V1_STR)
app.include_router(reserva_views.router, prefix=settings.API_V1_STR)
app.include_router(inventario_views.router, prefix=settings.API_V1_STR)
app.include_router(venta_presencial_views.router, prefix=settings.API_V1_STR)
app.include_router(compra_digital_views.router, prefix=settings.API_V1_STR)
app.include_router(pago_views.router, prefix=settings.API_V1_STR)
app.include_router(historial_views.router, prefix=settings.API_V1_STR)
app.include_router(recomendacion_views.router, prefix=settings.API_V1_STR)
app.include_router(notificacion_views.router, prefix=settings.API_V1_STR)
app.include_router(reporte_views.router, prefix=settings.API_V1_STR)
app.include_router(bitacora_views.router, prefix=settings.API_V1_STR)



@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "mensaje": "¡Bienvenido a la API Shopyn Golden Store!",
        "documentacion": "/docs",
        "arquitectura": "MVC (Modelo-Vista-Controlador)"
    }
