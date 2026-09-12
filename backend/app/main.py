# ==============================================================================
# ENTRY POINT - FASTAPI APPLICATION
# Proyecto: ECOMMERCE_TIENDA (Arquitectura MVC)
# ==============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import models # Registra todos los modelos ORM
from app.views import auth_views, user_views, role_views
from app.routes import cliente_routes, sucursal_routes, clasificacion_routes, producto_routes, proveedor_routes, inventario_routes, carrito_routes

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
    allow_origins=["*"], # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las Vistas / Rutas (Routers / API Endpoints)
app.include_router(auth_views.router, prefix=settings.API_V1_STR)
app.include_router(user_views.router, prefix=settings.API_V1_STR)
app.include_router(role_views.router, prefix=settings.API_V1_STR)
app.include_router(cliente_routes.router, prefix=settings.API_V1_STR)
app.include_router(sucursal_routes.router, prefix=settings.API_V1_STR)
app.include_router(clasificacion_routes.router, prefix=settings.API_V1_STR)
app.include_router(producto_routes.router, prefix=settings.API_V1_STR)
app.include_router(proveedor_routes.router, prefix=settings.API_V1_STR)
app.include_router(inventario_routes.router, prefix=settings.API_V1_STR)
app.include_router(carrito_routes.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "mensaje": "¡Bienvenido a la API E-Commerce Tienda!",
        "documentacion": "/docs",
        "arquitectura": "MVC (Modelo-Vista-Controlador)"
    }
