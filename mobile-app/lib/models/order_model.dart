// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Modelo de Orden / Pedido de Compra Digital (CU15)
// ==============================================================================

class OrderModel {
  final int id;
  final String codigoVenta;
  final String estado;
  final String tipoVenta;
  final double subtotal;
  final double total;
  final DateTime? fecha;
  final String? mensaje;

  OrderModel({
    required this.id,
    required this.codigoVenta,
    required this.estado,
    required this.tipoVenta,
    required this.subtotal,
    required this.total,
    this.fecha,
    this.mensaje,
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'] ?? 0,
      codigoVenta: json['codigoventa'] ?? '',
      estado: json['estado'] ?? 'Completada',
      tipoVenta: json['tipoventa'] ?? 'Digital',
      subtotal: (json['subtotal'] is num) ? (json['subtotal'] as num).toDouble() : double.tryParse(json['subtotal']?.toString() ?? '0') ?? 0.0,
      total: (json['total'] is num) ? (json['total'] as num).toDouble() : double.tryParse(json['total']?.toString() ?? '0') ?? 0.0,
      fecha: json['fecha'] != null ? DateTime.tryParse(json['fecha']) : null,
      mensaje: json['mensaje'],
    );
  }
}
