// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: mobile-app/lib/models/reservation_model.dart
// ==============================================================================

class ReservaDetalleItem {
  final int varianteId;
  final String productoNombre;
  final String? talla;
  final String? color;
  final String? imagenUrl;
  final double precioUnitario;
  final int cantidad;
  final double subtotal;

  ReservaDetalleItem({
    required this.varianteId,
    required this.productoNombre,
    this.talla,
    this.color,
    this.imagenUrl,
    required this.precioUnitario,
    required this.cantidad,
    required this.subtotal,
  });

  factory ReservaDetalleItem.fromJson(Map<String, dynamic> json) {
    return ReservaDetalleItem(
      varianteId: json['variante_id'] ?? 0,
      productoNombre: json['producto_nombre'] ?? 'Prenda',
      talla: json['talla'],
      color: json['color'],
      imagenUrl: json['imagen_url'],
      precioUnitario: (json['precio_unitario'] ?? 0.0).toDouble(),
      cantidad: json['cantidad'] ?? 1,
      subtotal: (json['subtotal'] ?? 0.0).toDouble(),
    );
  }
}

class ReservaModel {
  final int id;
  final String codigoReserva;
  final String fechaReserva;
  final String estado;
  final String? observaciones;
  final String? sucursalNombre;
  final String? sucursalDireccion;
  final List<ReservaDetalleItem> detalles;
  final int totalItems;
  final double totalEstimado;

  ReservaModel({
    required this.id,
    required this.codigoReserva,
    required this.fechaReserva,
    required this.estado,
    this.observaciones,
    this.sucursalNombre,
    this.sucursalDireccion,
    required this.detalles,
    required this.totalItems,
    required this.totalEstimado,
  });

  factory ReservaModel.fromJson(Map<String, dynamic> json) {
    var sucursal = json['sucursal'];
    var rawDetalles = json['detalles'] as List? ?? [];
    List<ReservaDetalleItem> detallesList =
        rawDetalles.map((d) => ReservaDetalleItem.fromJson(d)).toList();

    return ReservaModel(
      id: json['id'] ?? 0,
      codigoReserva: json['codigo_reserva'] ?? '',
      fechaReserva: json['fecha_reserva'] ?? '',
      estado: json['estado'] ?? 'PENDIENTE',
      observaciones: json['observaciones'],
      sucursalNombre: sucursal != null ? sucursal['nombre'] : null,
      sucursalDireccion: sucursal != null ? sucursal['direccion'] : null,
      detalles: detallesList,
      totalItems: json['total_items'] ?? 0,
      totalEstimado: (json['total_estimado'] ?? 0.0).toDouble(),
    );
  }
}
