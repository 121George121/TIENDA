// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador para Historial de Pedidos / Compras Digitales (CU15)
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/order_model.dart';

class OrderController extends ChangeNotifier {
  static String get baseUrl {
    if (kIsWeb) return 'http://localhost:8000/api/v1/ordenes';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1/ordenes';
    return 'http://127.0.0.1:8000/api/v1/ordenes';
  }

  List<OrderModel> _ordenes = [];
  bool _cargando = false;
  String? _error;

  List<OrderModel> get ordenes => _ordenes;
  bool get cargando => _cargando;
  String? get error => _error;

  Future<void> fetchMisOrdenes(String? token) async {
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

      final response = await http.get(
        Uri.parse('$baseUrl/me'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        _ordenes = data.map((json) => OrderModel.fromJson(json)).toList();
      } else {
        _error = "Error al obtener pedidos (${response.statusCode})";
      }
    } catch (e) {
      _error = "Error de conexión: $e";
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }
}
