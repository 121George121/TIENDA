# ==============================================================================
# SEEDER AUTOMATIZADO: VARIANTES DE COLOR, TALLA Y STOCK DIFERENCIADO POR SUCURSAL
# Proyecto: ECOMMERCE_TIENDA
# Ubicación: backend/app/core/seeder_variantes.py
# ==============================================================================

import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import (
    ColorModel, TallaModel, ProductoModel,
    VarianteProductoModel, SucursalModel, InventarioModel
)

logger = logging.getLogger("seeder_variantes")

# Definición de paleta de colores base
COLORES_DATA = [
    {"id": 1, "nombre": "Verde Oriente", "codigohex": "#007A3D"},
    {"id": 2, "nombre": "Blanco Tajibo", "codigohex": "#FFFFFF"},
    {"id": 3, "nombre": "Negro Azabache", "codigohex": "#111827"},
    {"id": 4, "nombre": "Azul Marino Camba", "codigohex": "#1E3A8A"},
    {"id": 5, "nombre": "Beige Chiquitano", "codigohex": "#D4B996"},
    {"id": 6, "nombre": "Terracota Guarayos", "codigohex": "#B45309"},
    {"id": 7, "nombre": "Gris Melange Urbano", "codigohex": "#64748B"},
    {"id": 8, "nombre": "Amarillo Patujú", "codigohex": "#F59E0B"},
    {"id": 9, "nombre": "Verde Olivo Chaco", "codigohex": "#556B2F"},
    {"id": 10, "nombre": "Rojo Borgoña", "codigohex": "#991B1B"},
]

TALLAS_DATA = [
    {"id": 1, "nombre": "S", "orden": 1},
    {"id": 2, "nombre": "M", "orden": 2},
    {"id": 3, "nombre": "L", "orden": 3},
    {"id": 4, "nombre": "XL", "orden": 4},
]

# Configuración realista de 3 variantes por producto con stock por sucursal
# Formato: [color_id, talla_id, stock_suc_1 (Equipetrol), stock_suc_2 (Ventura), stock_suc_3 (Brisas)]
PRODUCTO_VARIANTES_CONFIG = {
    1: [  # Canguro
        {"cid": 3, "tid": 2, "s1": 8, "s2": 4, "s3": 2},   # Negro - M
        {"cid": 7, "tid": 3, "s1": 6, "s2": 3, "s3": 1},   # Gris Melange - L
        {"cid": 4, "tid": 4, "s1": 4, "s2": 2, "s3": 0},   # Azul Marino - XL
    ],
    2: [  # Polera Deportiva
        {"cid": 4, "tid": 2, "s1": 10, "s2": 5, "s3": 3},  # Azul Marino - M
        {"cid": 3, "tid": 1, "s1": 7, "s2": 4, "s3": 2},   # Negro - S
        {"cid": 2, "tid": 3, "s1": 5, "s2": 2, "s3": 0},   # Blanco - L
    ],
    3: [  # Polera Gradientes
        {"cid": 8, "tid": 2, "s1": 6, "s2": 3, "s3": 1},   # Amarillo - M
        {"cid": 6, "tid": 3, "s1": 5, "s2": 2, "s3": 1},   # Terracota - L
        {"cid": 3, "tid": 1, "s1": 4, "s2": 2, "s3": 0},   # Negro - S
    ],
    4: [  # Polera Gradientes Cuello V
        {"cid": 1, "tid": 2, "s1": 7, "s2": 4, "s3": 2},   # Verde Oriente - M
        {"cid": 3, "tid": 3, "s1": 5, "s2": 3, "s3": 1},   # Negro - L
        {"cid": 2, "tid": 1, "s1": 4, "s2": 1, "s3": 0},   # Blanco - S
    ],
    5: [  # Dynamic Stroke V-Neck
        {"cid": 4, "tid": 2, "s1": 9, "s2": 4, "s3": 2},   # Azul Marino - M
        {"cid": 10, "tid": 3, "s1": 6, "s2": 3, "s3": 1},  # Rojo Borgoña - L
        {"cid": 3, "tid": 4, "s1": 4, "s2": 2, "s3": 0},   # Negro - XL
    ],
    6: [  # Polera Mangas Negras
        {"cid": 2, "tid": 2, "s1": 12, "s2": 6, "s3": 3},  # Blanco - M
        {"cid": 7, "tid": 3, "s1": 8, "s2": 4, "s3": 2},   # Gris Melange - L
        {"cid": 5, "tid": 1, "s1": 5, "s2": 2, "s3": 1},   # Beige - S
    ],
    7: [  # Polera Rosa Floral Degradé
        {"cid": 2, "tid": 1, "s1": 7, "s2": 3, "s3": 1},   # Blanco - S
        {"cid": 5, "tid": 2, "s1": 9, "s2": 4, "s3": 2},   # Beige - M
        {"cid": 3, "tid": 2, "s1": 4, "s2": 2, "s3": 0},   # Negro - M
    ],
    8: [  # Polera Estampada
        {"cid": 2, "tid": 2, "s1": 8, "s2": 5, "s3": 2},   # Blanco - M
        {"cid": 3, "tid": 3, "s1": 6, "s2": 3, "s3": 1},   # Negro - L
        {"cid": 10, "tid": 1, "s1": 4, "s2": 2, "s3": 0},  # Rojo Borgoña - S
    ],
    9: [  # Polera con diseño de mano
        {"cid": 3, "tid": 2, "s1": 7, "s2": 4, "s3": 2},   # Negro - M
        {"cid": 2, "tid": 1, "s1": 5, "s2": 2, "s3": 1},   # Blanco - S
        {"cid": 6, "tid": 3, "s1": 4, "s2": 1, "s3": 0},   # Terracota - L
    ],
    10: [  # Polera Negra Estampado Leopardo
        {"cid": 3, "tid": 2, "s1": 10, "s2": 5, "s3": 3},  # Negro - M
        {"cid": 5, "tid": 3, "s1": 6, "s2": 3, "s3": 1},   # Beige - L
        {"cid": 2, "tid": 1, "s1": 4, "s2": 1, "s3": 0},   # Blanco - S
    ],
    11: [  # Polera Estilista
        {"cid": 2, "tid": 2, "s1": 8, "s2": 4, "s3": 2},   # Blanco - M
        {"cid": 3, "tid": 1, "s1": 6, "s2": 3, "s3": 1},   # Negro - S
        {"cid": 7, "tid": 2, "s1": 4, "s2": 2, "s3": 0},   # Gris Melange - M
    ],
    12: [  # Filipina Estética Manicura
        {"cid": 2, "tid": 2, "s1": 9, "s2": 5, "s3": 2},   # Blanco - M
        {"cid": 4, "tid": 3, "s1": 6, "s2": 3, "s3": 1},   # Azul Marino - L
        {"cid": 3, "tid": 1, "s1": 5, "s2": 2, "s3": 0},   # Negro - S
    ],
    13: [  # Polera Negra Corazón Pincelada
        {"cid": 3, "tid": 2, "s1": 8, "s2": 4, "s3": 2},   # Negro - M
        {"cid": 2, "tid": 1, "s1": 6, "s2": 3, "s3": 1},   # Blanco - S
        {"cid": 10, "tid": 2, "s1": 4, "s2": 1, "s3": 0},  # Rojo Borgoña - M
    ],
    14: [  # Polera Básica Bicolor Verde Olivo
        {"cid": 9, "tid": 2, "s1": 11, "s2": 6, "s3": 3},  # Verde Olivo - M
        {"cid": 5, "tid": 3, "s1": 7, "s2": 4, "s3": 2},   # Beige - L
        {"cid": 2, "tid": 1, "s1": 5, "s2": 2, "s3": 1},   # Blanco - S
    ],
    15: [  # Polera Básica Verde Militar
        {"cid": 9, "tid": 2, "s1": 10, "s2": 5, "s3": 2},  # Verde Olivo - M
        {"cid": 3, "tid": 3, "s1": 7, "s2": 3, "s3": 1},   # Negro - L
        {"cid": 7, "tid": 1, "s1": 4, "s2": 2, "s3": 0},   # Gris Melange - S
    ],
    16: [  # Crop Top Negro
        {"cid": 3, "tid": 1, "s1": 5, "s2": 3, "s3": 1},   # Negro - S
        {"cid": 2, "tid": 2, "s1": 4, "s2": 2, "s3": 0},   # Blanco - M
        {"cid": 10, "tid": 1, "s1": 3, "s2": 1, "s3": 0},  # Rojo Borgoña - S
    ],
    17: [  # Polera Negra Harley Quinn
        {"cid": 3, "tid": 2, "s1": 8, "s2": 4, "s3": 2},   # Negro - M
        {"cid": 2, "tid": 1, "s1": 5, "s2": 2, "s3": 1},   # Blanco - S
        {"cid": 10, "tid": 3, "s1": 4, "s2": 1, "s3": 0},  # Rojo Borgoña - L
    ],
    18: [  # Institucional Artesanal
        {"cid": 5, "tid": 2, "s1": 9, "s2": 5, "s3": 2},   # Beige - M
        {"cid": 2, "tid": 3, "s1": 7, "s2": 3, "s3": 1},   # Blanco - L
        {"cid": 1, "tid": 1, "s1": 5, "s2": 2, "s3": 0},   # Verde Oriente - S
    ],
    19: [  # Polera Rústica con Bordado Tradicional
        {"cid": 5, "tid": 2, "s1": 12, "s2": 6, "s3": 3},  # Beige - M
        {"cid": 1, "tid": 1, "s1": 8, "s2": 4, "s3": 1},   # Verde Oriente - S
        {"cid": 2, "tid": 3, "s1": 6, "s2": 2, "s3": 0},   # Blanco - L
    ],
    20: [  # Camisa Patujú Santa Cruz
        {"cid": 2, "tid": 2, "s1": 14, "s2": 7, "s3": 3},  # Blanco - M
        {"cid": 1, "tid": 3, "s1": 9, "s2": 5, "s3": 2},   # Verde Oriente - L
        {"cid": 5, "tid": 4, "s1": 6, "s2": 2, "s3": 1},   # Beige - XL
    ],
    21: [  # Camisa Típica Blanca Bordado Ángel Chiquitano
        {"cid": 2, "tid": 2, "s1": 15, "s2": 8, "s3": 4},  # Blanco - M
        {"cid": 5, "tid": 3, "s1": 8, "s2": 4, "s3": 2},   # Beige - L
        {"cid": 2, "tid": 1, "s1": 6, "s2": 3, "s3": 1},   # Blanco - S
    ],
    22: [  # Polera Típica Beige Cordón Barroco
        {"cid": 5, "tid": 2, "s1": 11, "s2": 5, "s3": 2},  # Beige - M
        {"cid": 2, "tid": 3, "s1": 7, "s2": 3, "s3": 1},   # Blanco - L
        {"cid": 6, "tid": 1, "s1": 4, "s2": 2, "s3": 0},   # Terracota - S
    ],
    23: [  # Polera Básica Roja Cuello Redondo
        {"cid": 10, "tid": 2, "s1": 13, "s2": 7, "s3": 3}, # Rojo Borgoña - M
        {"cid": 3, "tid": 3, "s1": 8, "s2": 4, "s3": 2},   # Negro - L
        {"cid": 2, "tid": 1, "s1": 6, "s2": 3, "s3": 1},   # Blanco - S
    ],
}


def aplicar_seeder_variantes_y_stock(db: Session) -> dict:
    """
    Crea las variantes de múltiples colores y tallas para cada producto,
    y asigna stock diferenciado para cada sucursal física.
    """
    logger.info("[SEEDER] Iniciando actualización de variantes y stock multitienda...")

    # 1. Asegurar colores
    for c in COLORES_DATA:
        col = db.query(ColorModel).filter(ColorModel.id == c["id"]).first()
        if not col:
            col = ColorModel(id=c["id"], nombre=c["nombre"], codigohex=c["codigohex"], activo=True)
            db.add(col)
        else:
            col.nombre = c["nombre"]
            col.codigohex = c["codigohex"]
            col.activo = True
    db.commit()

    # 2. Asegurar tallas
    for t in TALLAS_DATA:
        talla = db.query(TallaModel).filter(TallaModel.id == t["id"]).first()
        if not talla:
            talla = TallaModel(id=t["id"], nombre=t["nombre"], orden=t["orden"], activo=True)
            db.add(talla)
        else:
            talla.nombre = t["nombre"]
            talla.orden = t["orden"]
            talla.activo = True
    db.commit()

    total_variantes_procesadas = 0
    total_inventarios_actualizados = 0

    # 3. Procesar cada producto
    productos = db.query(ProductoModel).all()
    prod_map = {p.id: p for p in productos}

    for prod_id, cfg_list in PRODUCTO_VARIANTES_CONFIG.items():
        if prod_id not in prod_map:
            continue

        prod = prod_map[prod_id]

        for idx, var_cfg in enumerate(cfg_list):
            cid = var_cfg["cid"]
            tid = var_cfg["tid"]
            s1_stock = var_cfg["s1"]
            s2_stock = var_cfg["s2"]
            s3_stock = var_cfg["s3"]

            sku = f"POL-{prod_id}-{cid}-{tid}"

            # La primera variante usa el slot existente de variante (para preservar integridad de FKs)
            var_record = None
            if idx == 0:
                var_record = db.query(VarianteProductoModel).filter(
                    VarianteProductoModel.productoid == prod_id
                ).first()

            if not var_record:
                # Buscar si ya existe la combinación producto + color + talla
                var_record = db.query(VarianteProductoModel).filter(
                    VarianteProductoModel.productoid == prod_id,
                    VarianteProductoModel.colorid == cid,
                    VarianteProductoModel.tallaid == tid
                ).first()

            if not var_record:
                var_record = VarianteProductoModel(
                    productoid=prod_id,
                    colorid=cid,
                    tallaid=tid,
                    sku=sku,
                    precioventa=prod.preciobase,
                    activo=True
                )
                db.add(var_record)
                db.flush()
            else:
                var_record.colorid = cid
                var_record.tallaid = tid
                var_record.sku = sku
                var_record.precioventa = prod.preciobase
                var_record.activo = True
                db.flush()

            total_variantes_procesadas += 1

            # 4. Asignar inventario para cada una de las 3 sucursales
            stocks = {1: s1_stock, 2: s2_stock, 3: s3_stock}
            for suc_id, stock_cant in stocks.items():
                inv = db.query(InventarioModel).filter(
                    InventarioModel.varianteid == var_record.id,
                    InventarioModel.sucursalid == suc_id
                ).first()

                if not inv:
                    inv = InventarioModel(
                        sucursalid=suc_id,
                        varianteid=var_record.id,
                        stockfisico=stock_cant,
                        stockreservado=0,
                        stockminimo=3
                    )
                    db.add(inv)
                else:
                    inv.stockfisico = stock_cant
                    inv.stockminimo = 3

                total_inventarios_actualizados += 1

    db.commit()

    return {
        "status": "success",
        "mensaje": "Variantes de colores y stock diferenciado por sucursal actualizados exitosamente.",
        "variantes_procesadas": total_variantes_procesadas,
        "registros_inventario": total_inventarios_actualizados
    }
