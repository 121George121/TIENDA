# ==============================================================================
# ENTRY POINT - FASTAPI APPLICATION
# Proyecto: ECOMMERCE_TIENDA (Arquitectura MVC)
# ==============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.views.cu1_gestionar_autenticacion import auth_views
from app.views.cu2_gestionar_usuarios_roles import user_views, role_views
from app.views.cu3_gestionar_clientes import cliente_views
from app.views.cu4_gestionar_sucursales import sucursal_views
from app.views.cu5_gestionar_productos import producto_views
from app.views.cu6_gestionar_clasificacion_prendas import clasificacion_views
from app.views.cu7_gestionar_proveedores_productos_suministrados import proveedor_views
from app.views.cu13_gestionar_inventario_movimientos import inventario_views
from app.views.cu14_registrar_ventas_presenciales import venta_presencial_views
from app.views.cu15_realizar_compras_digitales import compra_digital_views

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful siguiendo el patrón de arquitectura Modelo-Vista-Controlador (MVC)"
)

# Configuración de CORS para permitir conexiones desde Angular y Flutter (Web / Móvil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200", 
        "http://127.0.0.1:4200", 
        "http://localhost:5050", 
        "http://127.0.0.1:5050",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
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
