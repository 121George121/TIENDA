// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador de Estado para Productos usando HTTP y ChangeNotifier
// ==============================================================================

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/product_model.dart';

class ProductController extends ChangeNotifier {
  // IP para emulador Android (10.0.2.2) o localhost según corresponda
  final String _baseUrl = "http://10.0.2.2:8000/api/v1/productos";
  
  List<ProductModel> _productos = [];
  bool _cargando = false;
  String? _error;

  List<ProductModel> get productos => _productos;
  bool get cargando => _cargando;
  String? get error => _error;

  /// Método del controlador para consultar la API de FastAPI
  Future<void> fetchProductos() async {
    _cargando = true;
    _error = null;
    notifyListeners(); // Notifica a las Vistas (UI) para mostrar un spinner de carga

    try {
      final response = await http.get(Uri.parse(_baseUrl));

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        _productos = data.map((json) => ProductModel.fromJson(json)).toList();
      } else {
        _error = "Error en el servidor: ${response.statusCode}";
      }
    } catch (e) {
      _error = "Error de conexión con la API FastAPI: $e";
    } finally {
      _cargando = false;
      notifyListeners(); // Actualiza las Vistas con los datos obtenidos
    }
  }
}
