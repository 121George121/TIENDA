// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// CU16 - Gestionar Pagos y Comprobantes (Web y Móvil)
// Ubicación: mobile-app/lib/controllers/payment_controller.dart
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

class PaymentMethod {
  final int id;
  final String nombre;
  final bool estado;

  PaymentMethod({required this.id, required this.nombre, required this.estado});

  factory PaymentMethod.fromJson(Map<String, dynamic> json) {
    return PaymentMethod(
      id: json['id'],
      nombre: json['nombre'],
      estado: json['estado'] ?? true,
    );
  }
}

class PaymentController extends ChangeNotifier {
  static String get _host {
    if (kIsWeb) return 'http://localhost:8000/api/v1';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1';
    return 'http://127.0.0.1:8000/api/v1';
  }

  List<PaymentMethod> _metodos = [];
  bool _cargando = false;
  String? _error;
  int _metodoSeleccionadoId = 6; // PayPal por defecto (o 4 para QR, 2 para Efectivo)

  List<PaymentMethod> get metodos => _metodos;
  bool get cargando => _cargando;
  String? get error => _error;
  int get metodoSeleccionadoId => _metodoSeleccionadoId;

  void setMetodoSeleccionado(int id) {
    _metodoSeleccionadoId = id;
    notifyListeners();
  }

  /// Carga los métodos de pago desde el backend (FastAPI / PostgreSQL)
  Future<void> cargarMetodosPago() async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      final res = await http.get(Uri.parse('$_host/pagos/metodos'));
      if (res.statusCode == 200) {
        final List data = json.decode(utf8.decode(res.bodyBytes));
        _metodos = data.map((m) => PaymentMethod.fromJson(m)).toList();
        if (_metodos.isNotEmpty && !_metodos.any((m) => m.id == _metodoSeleccionadoId)) {
          _metodoSeleccionadoId = _metodos.first.id;
        }
      }
    } catch (e) {
      _error = 'No se pudo conectar con el servicio de pagos.';
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// Inicia el flujo de pago según el método (PayPal, QR o Efectivo)
  Future<Map<String, dynamic>?> iniciarPago({
    required int ventaId,
    required int metodoId,
    String? token,
  }) async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      final headers = <String, String>{
        'Content-Type': 'application/json',
      };
      if (token != null && token.isNotEmpty) {
        headers['Authorization'] = 'Bearer $token';
      }

      final body = json.encode({
        'venta_id': ventaId,
        'metodo_id': metodoId,
        'return_url': 'http://localhost:4200/cart?pago_status=exito&venta_id=$ventaId',
        'cancel_url': 'http://localhost:4200/cart?pago_status=cancelado',
      });

      final res = await http.post(
        Uri.parse('$_host/pagos/iniciar'),
        headers: headers,
        body: body,
      );

      if (res.statusCode == 200) {
        final data = json.decode(utf8.decode(res.bodyBytes));
        return data;
      } else {
        final err = json.decode(utf8.decode(res.bodyBytes));
        _error = err['detail'] ?? 'Error al iniciar pago.';
        return null;
      }
    } catch (e) {
      _error = 'Error de conexión al procesar el pago: $e';
      return null;
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// Abre la URL oficial de checkout de PayPal en el navegador del dispositivo
  Future<bool> abrirPayPal(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      return await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
    return false;
  }

  /// Obtiene los datos oficiales del comprobante con QR fiscal
  Future<Map<String, dynamic>?> obtenerComprobante(int ventaId, {String? token}) async {
    try {
      final headers = <String, String>{};
      if (token != null && token.isNotEmpty) {
        headers['Authorization'] = 'Bearer $token';
      }
      final res = await http.get(
        Uri.parse('$_host/pagos/$ventaId/comprobante'),
        headers: headers,
      );
      if (res.statusCode == 200) {
        return json.decode(utf8.decode(res.bodyBytes));
      }
      return null;
    } catch (e) {
      debugPrint('Error comprobante: $e');
      return null;
    }
  }

  /// Obtiene la URL para ver o imprimir el comprobante HTML
  String getComprobanteHtmlUrl(int ventaId) {
    return '$_host/pagos/$ventaId/comprobante-html';
  }
}
