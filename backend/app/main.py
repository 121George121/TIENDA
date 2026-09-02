# ==============================================================================
# ENTRY POINT - FASTAPI APPLICATION
# Proyecto: ECOMMERCE_TIENDA (Arquitectura MVC)
# ==============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.views import product_views, order_views, auth_views

# Crear tablas en la BD PostgreSQL si no existen al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful siguiendo el patrón de arquitectura Modelo-Vista-Controlador (MVC)"
)

# Configuración de CORS para permitir conexiones desde Angular y Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las Vistas (Routers / API Endpoints)
app.include_router(auth_views.router, prefix=settings.API_V1_STR)
app.include_router(product_views.router, prefix=settings.API_V1_STR)
app.include_router(order_views.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "mensaje": "¡Bienvenido a la API E-Commerce Tienda!",
        "documentacion": "/docs",
        "arquitectura": "MVC (Modelo-Vista-Controlador)"
    }
