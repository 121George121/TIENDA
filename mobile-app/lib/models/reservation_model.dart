// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: mobile-app/lib/models/reservation_model.dart
// ==============================================================================

double _parseDouble(dynamic value, [double defaultValue = 0.0]) {
  if (value == null) return defaultValue;
  if (value is num) return value.toDouble();
  return double.tryParse(value.toString()) ?? defaultValue;
}

int _parseInt(dynamic value, [int defaultValue = 0]) {
  if (value == null) return defaultValue;
  if (value is num) return value.toInt();
  return int.tryParse(value.toString()) ?? defaultValue;
}

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
      varianteId: _parseInt(json['variante_id'] ?? json['id']),
      productoNombre: json['producto_nombre']?.toString() ?? json['producto']?.toString() ?? 'Prenda',
      talla: json['talla']?.toString(),
      color: json['color']?.toString(),
      imagenUrl: json['imagen_url']?.toString(),
      precioUnitario: _parseDouble(json['precio_unitario']),
      cantidad: _parseInt(json['cantidad'], 1),
      subtotal: _parseDouble(json['subtotal']),
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
    var rawDetalles = json['detalles'] as List? ?? json['items'] as List? ?? [];
    List<ReservaDetalleItem> detallesList =
        rawDetalles.map((d) => ReservaDetalleItem.fromJson(d)).toList();

    return ReservaModel(
      id: _parseInt(json['id']),
      codigoReserva: json['codigo_reserva']?.toString() ?? '',
      fechaReserva: json['fecha_reserva']?.toString() ?? '',
      estado: json['estado']?.toString() ?? 'PENDIENTE',
      observaciones: json['observaciones']?.toString(),
      sucursalNombre: sucursal != null ? sucursal['nombre']?.toString() : json['sucursal_nombre']?.toString(),
      sucursalDireccion: sucursal != null ? sucursal['direccion']?.toString() : json['sucursal_direccion']?.toString(),
      detalles: detallesList,
      totalItems: _parseInt(json['total_items'] ?? detallesList.length),
      totalEstimado: _parseDouble(json['total_estimado']),
    );
  }
}
