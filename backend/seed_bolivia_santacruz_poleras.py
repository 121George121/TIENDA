# ==============================================================================
# SCRIPT DE POBLADO DE BASE DE DATOS: POLERAS DE BOLIVIA - SANTA CRUZ (SENIOR)
# Plataforma E-Commerce Tienda (FashionStore)
# ==============================================================================

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from datetime import datetime
from decimal import Decimal
from app.core.database import SessionLocal
from app.models.models import (
    SucursalModel, CategoriaModel, TallaModel, ColorModel,
    TemporadaModel, ColeccionModel, ProveedorModel, ProductoProveedorModel,
    ProductoModel, VarianteProductoModel, InventarioModel, MovimientoInventarioModel,
    UsuarioModel
)

def seed_database():
    db = SessionLocal()
    print("==================================================================")
    print("INICIANDO POBLADO DE POLERAS: SANTA CRUZ - BOLIVIA (MODO SENIOR)")
    print("==================================================================")

    try:
        # 1. ACTUALIZAR / CREAR SUCURSALES EN SANTA CRUZ
        print("-> Configurando Sucursales comerciales en Santa Cruz...")
        sucursales_data = [
            {
                "id": 1,
                "nombre": "Boutique Central Equipetrol",
                "ciudad": "Santa Cruz de la Sierra",
                "direccion": "Av. San Martín esq. Calle 7 (Equipetrol)",
                "telefono": "+591 3 3421100"
            },
            {
                "id": 2,
                "nombre": "Boutique Mall Ventura",
                "ciudad": "Santa Cruz de la Sierra",
                "direccion": "4to Anillo y Av. San Martín, Nivel 1 Local 42",
                "telefono": "+591 3 3458890"
            },
            {
                "id": 3,
                "nombre": "Boutique Las Brisas",
                "ciudad": "Santa Cruz de la Sierra",
                "direccion": "Av. Cristo Redentor y 4to Anillo, PB Local 15",
                "telefono": "+591 3 3482210"
            }
        ]

        sucursales_obj = []
        for s_data in sucursales_data:
            s = db.query(SucursalModel).filter(SucursalModel.id == s_data["id"]).first()
            if s:
                s.nombre = s_data["nombre"]
                s.ciudad = s_data["ciudad"]
                s.direccion = s_data["direccion"]
                s.telefono = s_data["telefono"]
                s.activo = True
            else:
                s = SucursalModel(
                    id=s_data["id"],
                    nombre=s_data["nombre"],
                    ciudad=s_data["ciudad"],
                    direccion=s_data["direccion"],
                    telefono=s_data["telefono"],
                    activo=True
                )
                db.add(s)
            sucursales_obj.append(s)
        db.commit()

        # 2. CATEGORÍAS POPULARES EN SANTA CRUZ
        print("-> Configurando Categorías de Poleras...")
        categorias_data = [
            {"id": 1, "nombre": "Poleras Polo Piqué (Casual Cruceña)", "descripcion": "Clásicas poleras con cuello camisero en tejido piqué, ideales para clima cálido y reuniones sociales"},
            {"id": 2, "nombre": "Poleras Oversize Streetwear", "descripcion": "Corte amplio y moderno de alto gramaje, estilo juvenil urbano Equipetrol"},
            {"id": 3, "nombre": "Poleras Cuello Redondo Básicas", "descripcion": "Prendas esenciales confeccionadas en 100% algodón Pima boliviano peinado"},
            {"id": 4, "nombre": "Poleras Estampadas Tradición & Camba", "descripcion": "Diseños exclusivos con iconos, flores de patujú, tajibos y costumbres cruceñas"},
            {"id": 5, "nombre": "Poleras Deportivas Dry-Fit", "descripcion": "Tejido microperforado de secado ultra rápido para entrenamiento y calor tropical"},
            {"id": 6, "nombre": "Poleras Manga Larga & Protección UV", "descripcion": "Protección solar certificada y resguardo confortable contra los surazos"}
        ]

        categorias_map = {}
        for c_data in categorias_data:
            cat = db.query(CategoriaModel).filter(CategoriaModel.id == c_data["id"]).first()
            if cat:
                cat.nombre = c_data["nombre"]
                cat.descripcion = c_data["descripcion"]
                cat.activo = True
            else:
                cat = CategoriaModel(
                    id=c_data["id"],
                    nombre=c_data["nombre"],
                    descripcion=c_data["descripcion"],
                    activo=True
                )
                db.add(cat)
            categorias_map[c_data["id"]] = cat
        db.commit()

        # 3. TALLAS (S, M, L, XL, XXL)
        print("-> Configurando Tallas...")
        tallas_data = [
            {"id": 1, "nombre": "S", "grupoedad": "Adultos", "orden": 1},
            {"id": 2, "nombre": "M", "grupoedad": "Adultos", "orden": 2},
            {"id": 3, "nombre": "L", "grupoedad": "Adultos", "orden": 3},
            {"id": 4, "nombre": "XL", "grupoedad": "Adultos", "orden": 4},
            {"id": 5, "nombre": "XXL", "grupoedad": "Adultos", "orden": 5},
        ]
        tallas_map = {}
        for t_data in tallas_data:
            talla = db.query(TallaModel).filter(TallaModel.id == t_data["id"]).first()
            if talla:
                talla.nombre = t_data["nombre"]
                talla.grupoedad = t_data["grupoedad"]
                talla.orden = t_data["orden"]
                talla.activo = True
            else:
                talla = TallaModel(
                    id=t_data["id"],
                    nombre=t_data["nombre"],
                    grupoedad=t_data["grupoedad"],
                    orden=t_data["orden"],
                    activo=True
                )
                db.add(talla)
            tallas_map[t_data["nombre"]] = talla
        db.commit()

        # 4. COLORES INSPIRADOS EN BOLIVIA Y SANTA CRUZ
        print("-> Configurando Colores temáticos...")
        colores_data = [
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
        colores_map = {}
        for c_data in colores_data:
            color = db.query(ColorModel).filter(ColorModel.id == c_data["id"]).first()
            if color:
                color.nombre = c_data["nombre"]
                color.codigohex = c_data["codigohex"]
                color.activo = True
            else:
                color = ColorModel(
                    id=c_data["id"],
                    nombre=c_data["nombre"],
                    codigohex=c_data["codigohex"],
                    activo=True
                )
                db.add(color)
            colores_map[c_data["nombre"]] = color
        db.commit()

        # 5. TEMPORADAS Y COLECCIONES
        print("-> Configurando Temporadas y Colecciones...")
        temp1 = db.query(TemporadaModel).filter(TemporadaModel.id == 1).first()
        if not temp1:
            temp1 = TemporadaModel(id=1, nombre="Primavera - Verano Santa Cruz 2026", fechainicio=datetime(2026, 9, 1), fechafin=datetime(2027, 3, 31), activo=True)
            db.add(temp1)
        else:
            temp1.nombre = "Primavera - Verano Santa Cruz 2026"

        temp2 = db.query(TemporadaModel).filter(TemporadaModel.id == 2).first()
        if not temp2:
            temp2 = TemporadaModel(id=2, nombre="Temporada Fexpocruz / Feria 2026", fechainicio=datetime(2026, 9, 15), fechafin=datetime(2026, 10, 15), activo=True)
            db.add(temp2)
        else:
            temp2.nombre = "Temporada Fexpocruz / Feria 2026"
        db.commit()

        # 6. PROVEEDORES BOLIVIANOS
        print("-> Configurando Proveedores locales...")
        proveedores_data = [
            {
                "id": 1,
                "nombre": "Industrias Textiles Mitsuba S.A.",
                "razonsocial": "Mitsuba Bolivia Textiles S.A.",
                "nit": "1028374029",
                "contacto": "Lic. Carlos Banzer",
                "telefono": "+591 3 3467711",
                "email": "ventas@mitsuba.bo",
                "direccion": "Parque Industrial Manzana 14, Santa Cruz"
            },
            {
                "id": 2,
                "nombre": "Confecciones Textiles del Oriente S.R.L.",
                "razonsocial": "Textiles del Oriente Cruceño S.R.L.",
                "nit": "1049281033",
                "contacto": "Ing. Fernando Justiniano",
                "telefono": "+591 3 3529944",
                "email": "contacto@textilesoriente.bo",
                "direccion": "Av. Virgen de Cotoca Km 4.5, Santa Cruz"
            },
            {
                "id": 3,
                "nombre": "Algodonera Pima Bolivia & Co.",
                "razonsocial": "Algodones Finos Pima S.R.L.",
                "nit": "1083749012",
                "contacto": "Mariela Vaca",
                "telefono": "+591 3 3362288",
                "email": "info@pimabolivia.com",
                "direccion": "Calle Warnes #240, Santa Cruz de la Sierra"
            }
        ]
        proveedores_map = {}
        for p_data in proveedores_data:
            prov = db.query(ProveedorModel).filter(ProveedorModel.id == p_data["id"]).first()
            if prov:
                prov.nombre = p_data["nombre"]
                prov.razonsocial = p_data["razonsocial"]
                prov.nit = p_data["nit"]
                prov.contacto = p_data["contacto"]
                prov.telefono = p_data["telefono"]
                prov.email = p_data["email"]
                prov.direccion = p_data["direccion"]
                prov.activo = True
            else:
                prov = ProveedorModel(
                    id=p_data["id"],
                    nombre=p_data["nombre"],
                    razonsocial=p_data["razonsocial"],
                    nit=p_data["nit"],
                    contacto=p_data["contacto"],
                    telefono=p_data["telefono"],
                    email=p_data["email"],
                    direccion=p_data["direccion"],
                    activo=True
                )
                db.add(prov)
            proveedores_map[p_data["id"]] = prov
        db.commit()

        # 7. CATÁLOGO DE POLERAS EMBLEMÁTICAS DE SANTA CRUZ
        print("-> Configurando Catálogo de Poleras Santa Cruz...")
        admin_user = db.query(UsuarioModel).first()
        admin_id = admin_user.id if admin_user else 1

        poleras_data = [
            {
                "id": 1,
                "nombre": "Polera Polo Piqué Mitsuba Tradicional",
                "descripcion": "Clásica polera polo cruceña en tejido piqué 100% algodón boliviano. Cuello camisero acanalado, botones de ajuste y calce impecable para el clima tropical de Santa Cruz.",
                "marca": "Mitsuba Bolivia",
                "genero": "Caballeros",
                "grupoedad": "Adultos",
                "preciobase": Decimal("165.00"),
                "categoriaid": 1,
                "imagenprincipal": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=800",
                "proveedor_id": 1,
                "variantes": [
                    {"color": "Verde Oriente", "talla": "M", "sku": "POL-MIT-VOR-M"},
                    {"color": "Verde Oriente", "talla": "L", "sku": "POL-MIT-VOR-L"},
                    {"color": "Blanco Tajibo", "talla": "M", "sku": "POL-MIT-BLA-M"},
                    {"color": "Blanco Tajibo", "talla": "L", "sku": "POL-MIT-BLA-L"},
                    {"color": "Azul Marino Camba", "talla": "XL", "sku": "POL-MIT-AZU-XL"},
                ]
            },
            {
                "id": 2,
                "nombre": "Polera Oversize \"Santa Cruz de la Sierra\" Heavyweight",
                "descripcion": "Corte holgado oversize en algodón pesado 240g. Estampado tipográfico minimalista en espalda inspirado en el plano radial de los anillos de Santa Cruz.",
                "marca": "CambaWear SCZ",
                "genero": "Unisex",
                "grupoedad": "Adultos",
                "preciobase": Decimal("185.00"),
                "categoriaid": 2,
                "imagenprincipal": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800",
                "proveedor_id": 2,
                "variantes": [
                    {"color": "Negro Azabache", "talla": "M", "sku": "OVR-SCZ-NEG-M"},
                    {"color": "Negro Azabache", "talla": "L", "sku": "OVR-SCZ-NEG-L"},
                    {"color": "Beige Chiquitano", "talla": "M", "sku": "OVR-SCZ-BEI-M"},
                    {"color": "Beige Chiquitano", "talla": "XL", "sku": "OVR-SCZ-BEI-XL"},
                ]
            },
            {
                "id": 3,
                "nombre": "Polera Básica Cuello Redondo Algodón Pima Oriente",
                "descripcion": "Tacto sedoso ultra suave con hilado fino de algodón Pima boliviano. Cuello redondo reforzado y frescura garantizada para el calor de la tarde cruceña.",
                "marca": "Textilón Santa Cruz",
                "genero": "Damas",
                "grupoedad": "Adultos",
                "preciobase": Decimal("120.00"),
                "categoriaid": 3,
                "imagenprincipal": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800",
                "proveedor_id": 3,
                "variantes": [
                    {"color": "Blanco Tajibo", "talla": "S", "sku": "BAS-PIM-BLA-S"},
                    {"color": "Blanco Tajibo", "talla": "M", "sku": "BAS-PIM-BLA-M"},
                    {"color": "Negro Azabache", "talla": "M", "sku": "BAS-PIM-NEG-M"},
                    {"color": "Gris Melange Urbano", "talla": "L", "sku": "BAS-PIM-GRI-L"},
                ]
            },
            {
                "id": 4,
                "nombre": "Polera Estampada \"Flor de Patujú\" Edición Botánica",
                "descripcion": "Serigrafía textil al agua de la emblemática flor de Patujú sobre jersey de algodón puro. Colores vivos resistentes a los lavados frecuentes.",
                "marca": "Pima Oriente",
                "genero": "Unisex",
                "grupoedad": "Adultos",
                "preciobase": Decimal("145.00"),
                "categoriaid": 4,
                "imagenprincipal": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800",
                "proveedor_id": 2,
                "variantes": [
                    {"color": "Blanco Tajibo", "talla": "M", "sku": "EST-PAT-BLA-M"},
                    {"color": "Blanco Tajibo", "talla": "L", "sku": "EST-PAT-BLA-L"},
                    {"color": "Verde Oriente", "talla": "M", "sku": "EST-PAT-VOR-M"},
                    {"color": "Verde Oriente", "talla": "L", "sku": "EST-PAT-VOR-L"},
                ]
            },
            {
                "id": 5,
                "nombre": "Polera Deportiva Dry-Fit \"Guajojó Active\" Transpirable",
                "descripcion": "Tecnología de ventilación microperforada y expulsión rápida del sudor. Diseñada para trotes en el Cambódromo y entrenamientos bajo el sol cruceño.",
                "marca": "Mitsuba Bolivia",
                "genero": "Caballeros",
                "grupoedad": "Adultos",
                "preciobase": Decimal("135.00"),
                "categoriaid": 5,
                "imagenprincipal": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800",
                "proveedor_id": 1,
                "variantes": [
                    {"color": "Azul Marino Camba", "talla": "M", "sku": "DEP-GUA-AZU-M"},
                    {"color": "Azul Marino Camba", "talla": "L", "sku": "DEP-GUA-AZU-L"},
                    {"color": "Negro Azabache", "talla": "L", "sku": "DEP-GUA-NEG-L"},
                    {"color": "Gris Melange Urbano", "talla": "XL", "sku": "DEP-GUA-GRI-XL"},
                ]
            },
            {
                "id": 6,
                "nombre": "Polera Polo Dama Slim Fit Verde Oriente",
                "descripcion": "Corte entallado femenino en tonalidad verde bandera cruceña. Bordado sutil en pecho y tapeta con botones al tono.",
                "marca": "Almanza Casual",
                "genero": "Damas",
                "grupoedad": "Adultos",
                "preciobase": Decimal("175.00"),
                "categoriaid": 1,
                "imagenprincipal": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800",
                "proveedor_id": 2,
                "variantes": [
                    {"color": "Verde Oriente", "talla": "S", "sku": "POL-DAM-VOR-S"},
                    {"color": "Verde Oriente", "talla": "M", "sku": "POL-DAM-VOR-M"},
                    {"color": "Blanco Tajibo", "talla": "S", "sku": "POL-DAM-BLA-S"},
                    {"color": "Blanco Tajibo", "talla": "M", "sku": "POL-DAM-BLA-M"},
                ]
            },
            {
                "id": 7,
                "nombre": "Polera \"Tajibo en Flor\" Ilustrada en Acuarela",
                "descripcion": "Homenaje artístico a los tajibos rosados y amarillos que colorean las avenidas cruceñas en agosto y septiembre.",
                "marca": "CambaWear SCZ",
                "genero": "Damas",
                "grupoedad": "Adultos",
                "preciobase": Decimal("150.00"),
                "categoriaid": 4,
                "imagenprincipal": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800",
                "proveedor_id": 2,
                "variantes": [
                    {"color": "Blanco Tajibo", "talla": "S", "sku": "EST-TAJ-BLA-S"},
                    {"color": "Blanco Tajibo", "talla": "M", "sku": "EST-TAJ-BLA-M"},
                    {"color": "Beige Chiquitano", "talla": "M", "sku": "EST-TAJ-BEI-M"},
                ]
            },
            {
                "id": 8,
                "nombre": "Polera Manga Larga Protección Solar UV50+ \"Surazo\"",
                "descripcion": "Fibra técnica ultraliviana con filtro UV certificado para el mediodía soleado y confort térmico contra los vientos de surazo.",
                "marca": "Textilón Santa Cruz",
                "genero": "Unisex",
                "grupoedad": "Adultos",
                "preciobase": Decimal("195.00"),
                "categoriaid": 6,
                "imagenprincipal": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800",
                "proveedor_id": 3,
                "variantes": [
                    {"color": "Azul Marino Camba", "talla": "M", "sku": "MLG-SUR-AZU-M"},
                    {"color": "Azul Marino Camba", "talla": "L", "sku": "MLG-SUR-AZU-L"},
                    {"color": "Gris Melange Urbano", "talla": "L", "sku": "MLG-SUR-GRI-L"},
                    {"color": "Negro Azabache", "talla": "XL", "sku": "MLG-SUR-NEG-XL"},
                ]
            },
            {
                "id": 9,
                "nombre": "Polera Boxy Fit \"Chovoreca Desert Sand\"",
                "descripcion": "Silueta boxy moderna con hombros caídos en tono arena Chiquitana, cuello rib ancho de 3 cm y acabado prémium pre-encogido.",
                "marca": "CambaWear SCZ",
                "genero": "Caballeros",
                "grupoedad": "Adultos",
                "preciobase": Decimal("170.00"),
                "categoriaid": 2,
                "imagenprincipal": "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=800",
                "proveedor_id": 2,
                "variantes": [
                    {"color": "Beige Chiquitano", "talla": "M", "sku": "BOX-CHO-BEI-M"},
                    {"color": "Beige Chiquitano", "talla": "L", "sku": "BOX-CHO-BEI-L"},
                    {"color": "Terracota Guarayos", "talla": "M", "sku": "BOX-CHO-TER-M"},
                    {"color": "Terracota Guarayos", "talla": "L", "sku": "BOX-CHO-TER-L"},
                ]
            },
            {
                "id": 10,
                "nombre": "Polera Cropped \"Sunset Güembé\" Algodón Orgánico",
                "descripcion": "Corte cropped casual en algodón peinado transpirable, tono suave inspirado en los atardeceres del Biocentro Güembé.",
                "marca": "Casa Elena",
                "genero": "Damas",
                "grupoedad": "Adultos",
                "preciobase": Decimal("130.00"),
                "categoriaid": 3,
                "imagenprincipal": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=800",
                "proveedor_id": 3,
                "variantes": [
                    {"color": "Beige Chiquitano", "talla": "S", "sku": "CRP-GUE-BEI-S"},
                    {"color": "Beige Chiquitano", "talla": "M", "sku": "CRP-GUE-BEI-M"},
                    {"color": "Blanco Tajibo", "talla": "S", "sku": "CRP-GUE-BLA-S"},
                ]
            },
            {
                "id": 11,
                "nombre": "Polera Polo Luxury Pima Almanza Premium",
                "descripcion": "La máxima expresión de sofisticación casual cruceña. Hilado mercerizado título 60/2, botones de nácar natural y cuello indeformable.",
                "marca": "Almanza Casual",
                "genero": "Caballeros",
                "grupoedad": "Adultos",
                "preciobase": Decimal("260.00"),
                "categoriaid": 1,
                "imagenprincipal": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800",
                "proveedor_id": 1,
                "variantes": [
                    {"color": "Azul Marino Camba", "talla": "M", "sku": "POL-ALM-AZU-M"},
                    {"color": "Azul Marino Camba", "talla": "L", "sku": "POL-ALM-AZU-L"},
                    {"color": "Negro Azabache", "talla": "L", "sku": "POL-ALM-NEG-L"},
                    {"color": "Blanco Tajibo", "talla": "XL", "sku": "POL-ALM-BLA-XL"},
                ]
            },
            {
                "id": 12,
                "nombre": "Polera Vintage \"Sombrero e' Saó y Guitarra\"",
                "descripcion": "Estilo retro nostálgico con ilustraciones de símbolos cruceños. Tacto cero en estampa y pre-lavado enzimático para máxima soltura.",
                "marca": "CambaWear SCZ",
                "genero": "Unisex",
                "grupoedad": "Adultos",
                "preciobase": Decimal("155.00"),
                "categoriaid": 4,
                "imagenprincipal": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800",
                "proveedor_id": 2,
                "variantes": [
                    {"color": "Negro Azabache", "talla": "M", "sku": "VIN-SAO-NEG-M"},
                    {"color": "Negro Azabache", "talla": "L", "sku": "VIN-SAO-NEG-L"},
                    {"color": "Gris Melange Urbano", "talla": "M", "sku": "VIN-SAO-GRI-M"},
                    {"color": "Blanco Tajibo", "talla": "L", "sku": "VIN-SAO-BLA-L"},
                ]
            }
        ]

        total_variantes_creadas = 0
        total_inventarios_creados = 0

        for p_info in poleras_data:
            # Buscar o crear producto
            prod = db.query(ProductoModel).filter(ProductoModel.id == p_info["id"]).first()
            if prod:
                prod.nombre = p_info["nombre"]
                prod.descripcion = p_info["descripcion"]
                prod.marca = p_info["marca"]
                prod.genero = p_info["genero"]
                prod.grupoedad = p_info["grupoedad"]
                prod.preciobase = p_info["preciobase"]
                prod.categoriaid = p_info["categoriaid"]
                prod.imagenprincipal = p_info["imagenprincipal"]
                prod.activo = True
            else:
                prod = ProductoModel(
                    id=p_info["id"],
                    nombre=p_info["nombre"],
                    descripcion=p_info["descripcion"],
                    marca=p_info["marca"],
                    genero=p_info["genero"],
                    grupoedad=p_info["grupoedad"],
                    preciobase=p_info["preciobase"],
                    categoriaid=p_info["categoriaid"],
                    imagenprincipal=p_info["imagenprincipal"],
                    activo=True
                )
                db.add(prod)
            db.flush()

            # Vincular con Proveedor
            vinculo = db.query(ProductoProveedorModel).filter(
                ProductoProveedorModel.idproducto == prod.id,
                ProductoProveedorModel.idproveedor == p_info["proveedor_id"]
            ).first()
            if not vinculo:
                vinculo = ProductoProveedorModel(
                    idproducto=prod.id,
                    idproveedor=p_info["proveedor_id"],
                    costocompra=p_info["preciobase"] * Decimal("0.55"),
                    cantidad=150
                )
                db.add(vinculo)

            # Crear o actualizar variantes
            for v_data in p_info["variantes"]:
                color_obj = colores_map.get(v_data["color"])
                talla_obj = tallas_map.get(v_data["talla"])

                if not color_obj or not talla_obj:
                    continue

                variante = db.query(VarianteProductoModel).filter(
                    VarianteProductoModel.productoid == prod.id,
                    VarianteProductoModel.colorid == color_obj.id,
                    VarianteProductoModel.tallaid == talla_obj.id
                ).first()

                if not variante:
                    variante = VarianteProductoModel(
                        productoid=prod.id,
                        colorid=color_obj.id,
                        tallaid=talla_obj.id,
                        sku=v_data["sku"],
                        codigobarra=f"777{prod.id:03d}{color_obj.id:02d}{talla_obj.id:02d}",
                        imagenurl=prod.imagenprincipal,
                        precioventa=prod.preciobase,
                        activo=True
                    )
                    db.add(variante)
                    db.flush()
                else:
                    variante.sku = v_data["sku"]
                    variante.precioventa = prod.preciobase
                    variante.imagenurl = prod.imagenprincipal
                    variante.activo = True

                total_variantes_creadas += 1

                # Crear Inventario en las 3 sucursales de Santa Cruz
                stock_distribucion = {
                    1: 35,  # Equipetrol (Principal)
                    2: 25,  # Ventura Mall
                    3: 20   # Las Brisas
                }

                for suc_id, stock_cant in stock_distribucion.items():
                    inv = db.query(InventarioModel).filter(
                        InventarioModel.varianteid == variante.id,
                        InventarioModel.sucursalid == suc_id
                    ).first()

                    if not inv:
                        inv = InventarioModel(
                            sucursalid=suc_id,
                            varianteid=variante.id,
                            stockfisico=stock_cant,
                            stockreservado=0,
                            stockminimo=5,
                            fechaactualizacion=datetime.utcnow()
                        )
                        db.add(inv)
                        db.flush()

                        # Registro de kardex inicial
                        mov = MovimientoInventarioModel(
                            tipomovimiento="Ingreso por Recepción de Proveedor",
                            cantidad=stock_cant,
                            motivo="Carga inicial de catálogo Santa Cruz 2026",
                            referencia=f"FAC-PROV-{p_info['proveedor_id']}",
                            fecha=datetime.utcnow(),
                            inventarioid=inv.id,
                            usuarioid=admin_id
                        )
                        db.add(mov)
                    else:
                        # Asegurar stock positivo
                        if inv.stockfisico < 10:
                            inv.stockfisico = stock_cant
                        inv.stockminimo = 5

                    total_inventarios_creados += 1

        db.commit()

        print("==================================================================")
        print("¡POBLADO COMPLETADO EXITOSAMENTE!")
        print(f"✓ Sucursales Santa Cruz: {len(sucursales_data)}")
        print(f"✓ Categorías: {len(categorias_data)}")
        print(f"✓ Tallas: {len(tallas_data)} (S, M, L, XL, XXL)")
        print(f"✓ Colores: {len(colores_data)}")
        print(f"✓ Proveedores: {len(proveedores_data)}")
        print(f"✓ Poleras registradas: {len(poleras_data)}")
        print(f"✓ Variantes registradas: {total_variantes_creadas}")
        print(f"✓ Registros de Inventario en sucursales: {total_inventarios_creados}")
        print("==================================================================")
        return True

    except Exception as e:
        print(f"❌ ERROR AL POBLAR BASE DE DATOS: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    exito = seed_database()
    sys.exit(0 if exito else 1)
