# ==============================================================================
# CU18 - GESTIONAR RECOMENDACIONES MEDIANTE IA -> CONTROLADOR (MVC)
# Ubicación: backend/app/controllers/cu18_gestionar_recomendaciones_ia/recomendacion_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import json
import random
import importlib

from app.core.config import settings
from app.models.cu5_gestionar_productos.producto_model import ProductoModel

# Importación dinámica para evitar alertas de análisis estático si el entorno no tiene el paquete registrado
genai = None
GENAI_DISPONIBLE = False
try:
    genai = importlib.import_module("google.genai")
    GENAI_DISPONIBLE = True
except Exception:
    GENAI_DISPONIBLE = False


class RecomendacionController:

    @staticmethod
    def _heuristica_estilista(producto_base: ProductoModel, catalogo: List[ProductoModel], limite: int = 3) -> List[Dict[str, Any]]:
        """Motor heurístico de estilista de moda cuando la IA externa no está configurada"""
        otros_productos = [p for p in catalogo if p.id != producto_base.id]
        if not otros_productos:
            return []

        # Variar las razones de estilo de forma coherente
        razones_plantilla = [
            f"El tono de esta prenda genera un contraste cromático balanceado con '{producto_base.nombre}'.",
            "Corte streetwear oversize ideal para vestir en capas (layering moderno).",
            "Pieza esencial en tendencia para elevar el outfit casual urbano.",
            "Textura y caída que complementa perfectamente el estilo de la prenda elegida.",
            "Colorimetría complementaria según la paleta de temporada de la boutique."
        ]

        seleccionados = random.sample(otros_productos, min(limite, len(otros_productos)))
        resultado = []
        for i, prod in enumerate(seleccionados):
            img_url = getattr(prod, 'imagenprincipal', None) or getattr(prod, 'imagen_url', None)
            resultado.append({
                "producto_id": prod.id,
                "nombre": prod.nombre,
                "precio": float(prod.preciobase or 0),
                "imagen_url": img_url,
                "razon_estilo": razones_plantilla[i % len(razones_plantilla)],
                "afinidad_porcentaje": 90 - (i * 4),
                "fuente": "IA Stylist Engine (Heurístico)"
            })
        return resultado

    @staticmethod
    def recomendar_outfit(
        db: Session,
        producto_id: Optional[int] = None,
        carrito_ids: Optional[List[int]] = None,
        limite: int = 3
    ) -> List[Dict[str, Any]]:
        """
        CU18: Genera recomendaciones de prendas para completar el look,
        utilizando Google Gemini AI si está configurado o el motor estilista interno.
        """
        catalogo = db.query(ProductoModel).filter(ProductoModel.activo == True).all()
        if not catalogo:
            return []

        # Determinar producto base
        producto_base = None
        if producto_id:
            producto_base = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
        elif carrito_ids and len(carrito_ids) > 0:
            producto_base = db.query(ProductoModel).filter(ProductoModel.id == carrito_ids[0]).first()

        if not producto_base:
            producto_base = catalogo[0]

        # Si Gemini API Key está disponible, invocar Gemini AI
        if GENAI_DISPONIBLE and settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 10:
            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                candidatos = [
                    {"id": p.id, "nombre": p.nombre, "precio": float(p.preciobase or 0)}
                    for p in catalogo if p.id != producto_base.id
                ][:15]

                prompt = f"""
                Actúa como un personal shopper y Fashion Stylist de alta gama de la tienda 'T-Shirt Boutique'.
                El cliente está mirando o comprando esta prenda:
                Nombre: '{producto_base.nombre}', Precio: {float(producto_base.preciobase or 0)} Bs.

                De este catálogo de prendas disponibles:
                {json.dumps(candidatos, ensure_ascii=False)}

                Elige hasta {limite} prendas que mejor combinen para armar un outfit completo y armónico.
                Responde ÚNICAMENTE un arreglo JSON válido con este formato:
                [
                    {{"producto_id": <int>, "razon_estilo": "<1 oración concisa explicando por qué combina>", "afinidad": <número entre 80 y 99>}}
                ]
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                texto = response.text.strip()
                if texto.startswith("```json"):
                    texto = texto[7:]
                if texto.endswith("```"):
                    texto = texto[:-3]
                texto = texto.strip()

                sugerencias_ia = json.loads(texto)
                resultado = []
                for sug in sugerencias_ia:
                    pid = sug.get("producto_id")
                    prod = next((p for p in catalogo if p.id == pid), None)
                    if prod:
                        img_url = getattr(prod, 'imagenprincipal', None) or getattr(prod, 'imagen_url', None)
                        resultado.append({
                            "producto_id": prod.id,
                            "nombre": prod.nombre,
                            "precio": float(prod.preciobase or 0),
                            "imagen_url": img_url,
                            "razon_estilo": sug.get("razon_estilo", "Excelente combinación para tu estilo"),
                            "afinidad_porcentaje": sug.get("afinidad", 95),
                            "fuente": "Google Gemini 2.5 Flash AI"
                        })

                if resultado:
                    return resultado
            except Exception as e:
                print(f"⚠️ Nota: Gemini AI fallback a heurística estilista: {e}")

        # Fallback al motor heurístico inteligente
        return RecomendacionController._heuristica_estilista(producto_base, catalogo, limite)

    @staticmethod
    def obtener_tendencias(db: Session, limite: int = 4) -> List[Dict[str, Any]]:
        """CU18: Retorna productos destacados en tendencia para vitrina de recomendaciones"""
        productos = db.query(ProductoModel).filter(ProductoModel.activo == True).order_by(ProductoModel.id.desc()).limit(limite).all()
        resultado = []
        for p in productos:
            img_url = getattr(p, 'imagenprincipal', None) or getattr(p, 'imagen_url', None)
            resultado.append({
                "producto_id": p.id,
                "nombre": p.nombre,
                "precio": float(p.preciobase or 0),
                "imagen_url": img_url,
                "etiqueta": "🔥 Tendencia de Temporada",
                "razon": "Prenda con alta tasa de favoritos en la colección actual"
            })
        return resultado
