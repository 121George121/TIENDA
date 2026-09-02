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

  // Método de Fábrica para mapear el JSON recibido de la API FastAPI
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'],
      precio: (json['precio'] as num).toDouble(),
      stock: json['stock'],
      categoriaId: json['categoria_id'],
      imagenUrl: json['imagen_url'],
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
