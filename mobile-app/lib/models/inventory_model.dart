// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Módulo: CU08 - Consultar Catálogo y Disponibilidad de Inventario
// Ubicación: mobile-app/lib/models/inventory_model.dart
// ==============================================================================

class BranchModel {
  final int id;
  final String nombre;
  final String? ciudad;
  final String? direccion;
  final String? telefono;

  BranchModel({
    required this.id,
    required this.nombre,
    this.ciudad,
    this.direccion,
    this.telefono,
  });

  factory BranchModel.fromJson(Map<String, dynamic> json) {
    return BranchModel(
      id: json['id'],
      nombre: json['nombre'],
      ciudad: json['ciudad'],
      direccion: json['direccion'],
      telefono: json['telefono'],
    );
  }
}

class ProductVariantModel {
  final int varianteId;
  final String? sku;
  final String? talla;
  final String? color;
  final String? codigohex;
  final double precio;
  final int stock;
  final bool disponible;

  ProductVariantModel({
    required this.varianteId,
    this.sku,
    this.talla,
    this.color,
    this.codigohex,
    required this.precio,
    required this.stock,
    required this.disponible,
  });

  factory ProductVariantModel.fromJson(Map<String, dynamic> json) {
    return ProductVariantModel(
      varianteId: json['variante_id'],
      sku: json['sku'],
      talla: json['talla'],
      color: json['color'],
      codigohex: json['codigohex'],
      precio: (json['precio'] as num).toDouble(),
      stock: json['stock'] ?? 0,
      disponible: json['disponible'] ?? false,
    );
  }
}

class CatalogProductModel {
  final int id;
  final String nombre;
  final String? descripcion;
  final String? marca;
  final String? genero;
  final double preciobase;
  final String? imagenprincipal;
  final String? categoriaNombre;
  final int stockSucursal;
  final int stockTotal;
  final bool disponible;
  final List<ProductVariantModel> variantes;

  CatalogProductModel({
    required this.id,
    required this.nombre,
    this.descripcion,
    this.marca,
    this.genero,
    required this.preciobase,
    this.imagenprincipal,
    this.categoriaNombre,
    required this.stockSucursal,
    required this.stockTotal,
    required this.disponible,
    required this.variantes,
  });

  factory CatalogProductModel.fromJson(Map<String, dynamic> json) {
    var rawVariantes = json['variantes'] as List? ?? [];
    List<ProductVariantModel> listVariantes =
        rawVariantes.map((v) => ProductVariantModel.fromJson(v)).toList();

    return CatalogProductModel(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'],
      marca: json['marca'],
      genero: json['genero'],
      preciobase: (json['preciobase'] as num).toDouble(),
      imagenprincipal: json['imagenprincipal'],
      categoriaNombre: json['categoria_nombre'],
      stockSucursal: json['stock_sucursal'] ?? 0,
      stockTotal: json['stock_total'] ?? 0,
      disponible: json['disponible'] ?? false,
      variantes: listVariantes,
    );
  }
}
