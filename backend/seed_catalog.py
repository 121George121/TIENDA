from app.core.database import SessionLocal
from app.models.models import (
    SucursalModel, CategoriaModel, TallaModel, ColorModel,
    ProductoModel, VarianteProductoModel, InventarioSucursalModel
)

db = SessionLocal()
try:
    # 1. Sucursales Físicas
    sucursales_data = [
        {"nombre": "Sucursal Central (Centro)", "ciudad": "La Paz", "direccion": "Av. 16 de Julio #1420 (El Prado)", "telefono": "+591 2 2445566"},
        {"nombre": "Sucursal Zona Sur (San Miguel)", "ciudad": "La Paz", "direccion": "Calle 21 de Calacoto #850", "telefono": "+591 2 2778899"},
        {"nombre": "Sucursal Equipetrol (Santa Cruz)", "ciudad": "Santa Cruz", "direccion": "Av. San Martín #450", "telefono": "+591 3 3334455"}
    ]

    sucursales = []
    for s in sucursales_data:
        exist = db.query(SucursalModel).filter(SucursalModel.nombre == s["nombre"]).first()
        if not exist:
            exist = SucursalModel(**s)
            db.add(exist)
            db.flush()
        sucursales.append(exist)

    # 2. Categorías
    categorias_data = [
        {"nombre": "Poleras Graphic & Art", "descripcion": "Poleras con estampados artísticos y urbanos"},
        {"nombre": "Poleras Oversize", "descripcion": "Corte holgado estilo streetwear contemporáneo"},
        {"nombre": "Poleras Polo Classic", "descripcion": "Polos de algodón pima cuello camisero"},
        {"nombre": "Hoodies & Polerones", "descripcion": "Buzos y sudaderas confortables"}
    ]

    categorias = []
    for c in categorias_data:
        exist = db.query(CategoriaModel).filter(CategoriaModel.nombre == c["nombre"]).first()
        if not exist:
            exist = CategoriaModel(**c)
            db.add(exist)
            db.flush()
        categorias.append(exist)

    # 3. Tallas
    tallas_data = [
        {"nombre": "S", "orden": 1},
        {"nombre": "M", "orden": 2},
        {"nombre": "L", "orden": 3},
        {"nombre": "XL", "orden": 4}
    ]

    tallas = []
    for t in tallas_data:
        exist = db.query(TallaModel).filter(TallaModel.nombre == t["nombre"]).first()
        if not exist:
            exist = TallaModel(**t)
            db.add(exist)
            db.flush()
        tallas.append(exist)

    # 4. Colores
    colores_data = [
        {"nombre": "Negro Midnight", "codigohex": "#111111"},
        {"nombre": "Blanco Puro", "codigohex": "#FFFFFF"},
        {"nombre": "Azul Navy", "codigohex": "#1B2A4A"},
        {"nombre": "Verde Oliva", "codigohex": "#4B5320"},
        {"nombre": "Beige Sand", "codigohex": "#D8C7A5"}
    ]

    colores = []
    for col in colores_data:
        exist = db.query(ColorModel).filter(ColorModel.nombre == col["nombre"]).first()
        if not exist:
            exist = ColorModel(**col)
            db.add(exist)
            db.flush()
        colores.append(exist)

    # 5. Productos con Variantes e Inventario por Sucursal
    productos_data = [
        {
            "nombre": "Polera Oversize Minimalist 'Origins'",
            "descripcion": "Polera de corte oversize en 100% algodón pesado de 240 GSM. Acabado suave y cuello rib reforzado.",
            "marca": "Aura Studio",
            "genero": "Unisex",
            "preciobase": 149.00,
            "imagenprincipal": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80",
            "categoria": categorias[1],
            "variantes": [
                {"color": colores[0], "talla": tallas[1], "sku": "AURA-BLK-M", "stock_s1": 8, "stock_s2": 4, "stock_s3": 0},
                {"color": colores[0], "talla": tallas[2], "sku": "AURA-BLK-L", "stock_s1": 5, "stock_s2": 2, "stock_s3": 3},
                {"color": colores[4], "talla": tallas[1], "sku": "AURA-BEI-M", "stock_s1": 10, "stock_s2": 6, "stock_s3": 5},
                {"color": colores[4], "talla": tallas[2], "sku": "AURA-BEI-L", "stock_s1": 0, "stock_s2": 3, "stock_s3": 4}
            ]
        },
        {
            "nombre": "Polera Graphic 'Tokyo Neon Cyberpunk'",
            "descripcion": "Estampado en serigrafía de alta densidad con diseño neo-tokyo en la espalda. Tela fresca transpirable.",
            "marca": "Urban Pulse",
            "genero": "Caballeros",
            "preciobase": 129.00,
            "imagenprincipal": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80",
            "categoria": categorias[0],
            "variantes": [
                {"color": colores[0], "talla": tallas[0], "sku": "TOKYO-BLK-S", "stock_s1": 3, "stock_s2": 0, "stock_s3": 2},
                {"color": colores[0], "talla": tallas[1], "sku": "TOKYO-BLK-M", "stock_s1": 12, "stock_s2": 8, "stock_s3": 4},
                {"color": colores[1], "talla": tallas[2], "sku": "TOKYO-WHT-L", "stock_s1": 6, "stock_s2": 5, "stock_s3": 1}
            ]
        },
        {
            "nombre": "Polo Classic Piqué 'Riviera'",
            "descripcion": "Cuello camisero estructurado, botones en nácar grabado y bordado discreto en el pecho. Algodón pima peinado.",
            "marca": "Heritage Club",
            "genero": "Caballeros",
            "preciobase": 189.00,
            "imagenprincipal": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=800&auto=format&fit=crop&q=80",
            "categoria": categorias[2],
            "variantes": [
                {"color": colores[2], "talla": tallas[1], "sku": "RIVIERA-NVY-M", "stock_s1": 7, "stock_s2": 0, "stock_s3": 4},
                {"color": colores[2], "talla": tallas[2], "sku": "RIVIERA-NVY-L", "stock_s1": 4, "stock_s2": 3, "stock_s3": 0},
                {"color": colores[1], "talla": tallas[1], "sku": "RIVIERA-WHT-M", "stock_s1": 9, "stock_s2": 7, "stock_s3": 6}
            ]
        },
        {
            "nombre": "Cropped Tee Feminine 'Botanical'",
            "descripcion": "Corte cropped casual con bordado botánico minimalista. Tacto extrasuave, silueta favorecedora.",
            "marca": "Aura Studio",
            "genero": "Damas",
            "preciobase": 119.00,
            "imagenprincipal": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80",
            "categoria": categorias[0],
            "variantes": [
                {"color": colores[4], "talla": tallas[0], "sku": "BOTA-BEI-S", "stock_s1": 5, "stock_s2": 4, "stock_s3": 2},
                {"color": colores[4], "talla": tallas[1], "sku": "BOTA-BEI-M", "stock_s1": 8, "stock_s2": 0, "stock_s3": 3},
                {"color": colores[3], "talla": tallas[1], "sku": "BOTA-OLV-M", "stock_s1": 4, "stock_s2": 5, "stock_s3": 0}
            ]
        },
        {
            "nombre": "Heavyweight Hoodie 'Nomad Essential'",
            "descripcion": "Sudadera con capucha premium en felpa perchada de 400 GSM. Cordones de algodón grueso y bolsillo canguro.",
            "marca": "Aura Studio",
            "genero": "Unisex",
            "preciobase": 249.00,
            "imagenprincipal": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=80",
            "categoria": categorias[3],
            "variantes": [
                {"color": colores[0], "talla": tallas[1], "sku": "HOOD-BLK-M", "stock_s1": 6, "stock_s2": 2, "stock_s3": 5},
                {"color": colores[0], "talla": tallas[2], "sku": "HOOD-BLK-L", "stock_s1": 4, "stock_s2": 0, "stock_s3": 2},
                {"color": colores[3], "talla": tallas[2], "sku": "HOOD-OLV-L", "stock_s1": 3, "stock_s2": 3, "stock_s3": 1}
            ]
        }
    ]

    for pdata in productos_data:
        prod = db.query(ProductoModel).filter(ProductoModel.nombre == pdata["nombre"]).first()
        if not prod:
            prod = ProductoModel(
                nombre=pdata["nombre"],
                descripcion=pdata["descripcion"],
                marca=pdata["marca"],
                genero=pdata["genero"],
                preciobase=pdata["preciobase"],
                imagenprincipal=pdata["imagenprincipal"],
                categoriaid=pdata["categoria"].id
            )
            db.add(prod)
            db.flush()

        for vdata in pdata["variantes"]:
            var = db.query(VarianteProductoModel).filter(VarianteProductoModel.sku == vdata["sku"]).first()
            if not var:
                var = VarianteProductoModel(
                    productoid=prod.id,
                    colorid=vdata["color"].id,
                    tallaid=vdata["talla"].id,
                    sku=vdata["sku"],
                    precioventa=pdata["preciobase"]
                )
                db.add(var)
                db.flush()

            # Asignar stock en las 3 sucursales
            stocks = [vdata["stock_s1"], vdata["stock_s2"], vdata["stock_s3"]]
            for i, sucursal in enumerate(sucursales):
                inv = db.query(InventarioSucursalModel).filter(
                    InventarioSucursalModel.varianteid == var.id,
                    InventarioSucursalModel.sucursalid == sucursal.id
                ).first()
                if not inv:
                    inv = InventarioSucursalModel(
                        varianteid=var.id,
                        sucursalid=sucursal.id,
                        cantidad=stocks[i]
                    )
                    db.add(inv)
                else:
                    inv.cantidad = stocks[i]

    db.commit()
    print("OK: Catalogo e inventario por sucursales sembrado exitosamente.")
finally:
    db.close()
