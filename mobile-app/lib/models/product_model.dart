// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Estructura de Datos y Conversión JSON para Productos
// ==============================================================================

class ProductModel {
  final int id;
  final String nombre;
  final String? descripcion;
  final double precio;
  final int stock;
  final int? categoriaId;
  final String? imagenUrl;
  final bool activo;

  ProductModel({
    required this.id,
    required this.nombre,
    this.descripcion,
    required this.precio,
    required this.stock,
    this.categoriaId,
    this.imagenUrl,
    required this.activo,
  });

  // Método de Fábrica para mapear el JSON recibido de la API FastAPI de forma robusta y segura
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    // Parsing seguro para precio (soporta 'precio', 'preciobase', num o string numérico)
    final rawPrecio = json['precio'] ?? json['preciobase'] ?? 0;
    final double precioValue = rawPrecio is num
        ? rawPrecio.toDouble()
        : (double.tryParse(rawPrecio.toString()) ?? 0.0);

    // Parsing seguro para stock (soporta 'stock', 'stockdisponible', 'stockfisico' con fallback 20)
    final rawStock = json['stock'] ?? json['stockdisponible'] ?? json['stockfisico'] ?? 20;
    final int stockValue = rawStock is num
        ? rawStock.toInt()
        : (int.tryParse(rawStock.toString()) ?? 20);

    return ProductModel(
      id: json['id'] is int ? json['id'] : (int.tryParse(json['id']?.toString() ?? '0') ?? 0),
      nombre: json['nombre']?.toString() ?? '',
      descripcion: json['descripcion']?.toString(),
      precio: precioValue,
      stock: stockValue,
      categoriaId: json['categoria_id'] is int ? json['categoria_id'] : json['categoriaid'],
      imagenUrl: json['imagen_url']?.toString() ?? json['imagenprincipal']?.toString(),
      activo: json['activo'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'descripcion': descripcion,
      'precio': precio,
      'stock': stock,
      'categoria_id': categoriaId,
      'imagen_url': imagenUrl,
      'activo': activo,
    };
  }
}
