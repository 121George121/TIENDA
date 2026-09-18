// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// CU18 - Gestionar Recomendaciones mediante IA (Web y Móvil)
// Ubicación: mobile-app/lib/controllers/recommendation_controller.dart
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class RecommendationItem {
  final int productoId;
  final String nombre;
  final double precio;
  final String? imagenUrl;
  final String razonEstilo;
  final int afinidadPorcentaje;
  final String fuente;

  RecommendationItem({
    required this.productoId,
    required this.nombre,
    required this.precio,
    this.imagenUrl,
    required this.razonEstilo,
    required this.afinidadPorcentaje,
    required this.fuente,
  });

  factory RecommendationItem.fromJson(Map<String, dynamic> json) {
    return RecommendationItem(
      productoId: json['producto_id'] ?? 0,
      nombre: json['nombre'] ?? '',
      precio: (json['precio'] is num) ? (json['precio'] as num).toDouble() : 0.0,
      imagenUrl: json['imagen_url'],
      razonEstilo: json['razon_estilo'] ?? '',
      afinidadPorcentaje: json['afinidad_porcentaje'] ?? 90,
      fuente: json['fuente'] ?? 'IA Stylist',
    );
  }
}

class RecommendationController extends ChangeNotifier {
  static String get _host {
    if (kIsWeb) return 'http://localhost:8000/api/v1';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1';
    return 'http://127.0.0.1:8000/api/v1';
  }

  List<RecommendationItem> _recomendaciones = [];
  bool _cargando = false;
  String? _error;

  List<RecommendationItem> get recomendaciones => _recomendaciones;
  bool get cargando => _cargando;
  String? get error => _error;

  Future<void> fetchRecomendaciones({int? productoId, List<int>? carritoIds}) async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      final body = json.encode({
        'producto_id': productoId,
        'carrito_ids': carritoIds,
        'limite': 3,
      });

      final res = await http.post(
        Uri.parse('$_host/recomendaciones/outfit'),
        headers: {'Content-Type': 'application/json'},
        body: body,
      );

      if (res.statusCode == 200) {
        final List data = json.decode(utf8.decode(res.bodyBytes));
        _recomendaciones = data.map((item) => RecommendationItem.fromJson(item)).toList();
      } else {
        _error = 'No se pudieron generar recomendaciones';
      }
    } catch (e) {
      _error = 'Error de conexión con el motor IA: $e';
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }
}
