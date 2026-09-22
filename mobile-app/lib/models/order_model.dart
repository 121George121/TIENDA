// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Modelo de Orden / Pedido de Compra Digital (CU15)
// ==============================================================================

class OrderItemModel {
  final int productoId;
  final String productoNombre;
  final String? imagenUrl;
  final String? talla;
  final String? color;
  final int cantidad;
  final double precioUnitario;
  final double subtotal;

  OrderItemModel({
    required this.productoId,
    required this.productoNombre,
    this.imagenUrl,
    this.talla,
    this.color,
    required this.cantidad,
    required this.precioUnitario,
    required this.subtotal,
  });

  factory OrderItemModel.fromJson(Map<String, dynamic> json) {
    return OrderItemModel(
      productoId: json['producto_id'] ?? 0,
      productoNombre: json['producto_nombre'] ?? 'Prenda de Vestir',
      imagenUrl: json['imagen_url'],
      talla: json['talla'],
      color: json['color'],
      cantidad: json['cantidad'] ?? 1,
      precioUnitario: (json['preciounitario'] is num)
          ? (json['preciounitario'] as num).toDouble()
          : double.tryParse(json['preciounitario']?.toString() ?? '0') ?? 0.0,
      subtotal: (json['subtotal'] is num)
          ? (json['subtotal'] as num).toDouble()
          : double.tryParse(json['subtotal']?.toString() ?? '0') ?? 0.0,
    );
  }
}

class OrderModel {
  final int id;
  final String codigoVenta;
  final String estado;
  final String tipoVenta;
  final double subtotal;
  final double total;
  final DateTime? fecha;
  final String? mensaje;
  final List<OrderItemModel> items;

  OrderModel({
    required this.id,
    required this.codigoVenta,
    required this.estado,
    required this.tipoVenta,
    required this.subtotal,
    required this.total,
    this.fecha,
    this.mensaje,
    this.items = const [],
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    var rawItems = json['items'];
    List<OrderItemModel> parsedItems = [];
    if (rawItems is List) {
      parsedItems = rawItems
          .map((e) => OrderItemModel.fromJson(e as Map<String, dynamic>))
          .toList();
    }

    return OrderModel(
      id: json['id'] ?? 0,
      codigoVenta: json['codigoventa'] ?? '',
      estado: json['estado'] ?? 'Comprado',
      tipoVenta: json['tipoventa'] ?? 'Digital',
      subtotal: (json['subtotal'] is num)
          ? (json['subtotal'] as num).toDouble()
          : double.tryParse(json['subtotal']?.toString() ?? '0') ?? 0.0,
      total: (json['total'] is num)
          ? (json['total'] as num).toDouble()
          : double.tryParse(json['total']?.toString() ?? '0') ?? 0.0,
      fecha: json['fecha'] != null ? DateTime.tryParse(json['fecha']) : null,
      mensaje: json['mensaje'],
      items: parsedItems,
    );
  }
}

