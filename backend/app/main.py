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
from app.views.cu13_gestionar_inventario_movimientos import inventario_views
from app.views.cu14_registrar_ventas_presenciales import venta_presencial_views
from app.views.cu15_realizar_compras_digitales import compra_digital_views

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful siguiendo el patrón de arquitectura Modelo-Vista-Controlador (MVC)"
)

@app.on_event("startup")
def on_startup():
    try:
        # Crear automáticamente las tablas en PostgreSQL si aún no existen
        Base.metadata.create_all(bind=engine)
        print("✓ Tablas de la base de datos sincronizadas correctamente.")
    except Exception as e:
        print(f"⚠️ Advertencia al conectar con la base de datos: {e}")

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
app.include_router(atender_reserva_views.router, prefix=settings.API_V1_STR)
app.include_router(reserva_views.router, prefix=settings.API_V1_STR)
app.include_router(inventario_views.router, prefix=settings.API_V1_STR)
app.include_router(venta_presencial_views.router, prefix=settings.API_V1_STR)
app.include_router(compra_digital_views.router, prefix=settings.API_V1_STR)



@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "mensaje": "¡Bienvenido a la API E-Commerce Tienda!",
        "documentacion": "/docs",
        "arquitectura": "MVC (Modelo-Vista-Controlador)"
    }
