// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador del Carrito de Compras en la Aplicación Móvil
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/product_model.dart';
import '../models/cart_item_model.dart';

class CartController extends ChangeNotifier {
  static String get _orderUrl {
    if (kIsWeb) return 'http://localhost:8000/api/v1/ordenes/';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1/ordenes/';
    return 'http://127.0.0.1:8000/api/v1/ordenes/';
  }
  
  final Map<int, CartItemModel> _items = {};

  Map<int, CartItemModel> get items => _items;

  int get totalItemCount {
    return _items.values.fold(0, (sum, item) => sum + item.cantidad);
  }

  double get totalMonto {
    return _items.values.fold(0.0, (sum, item) => sum + item.subtotal);
  }

  /// Lógica del controlador para añadir producto al carrito
  void agregarProducto(ProductModel producto) {
    if (_items.containsKey(producto.id)) {
      _items[producto.id]!.cantidad += 1;
    } else {
      _items[producto.id] = CartItemModel(product: producto);
    }
    notifyListeners(); // Renderiza de nuevo las vistas móviles
  }

  void removerProducto(int productoId) {
    _items.remove(productoId);
    notifyListeners();
  }

  void limpiarCarrito() {
    _items.clear();
    notifyListeners();
  }

  /// Procesa la compra enviando el payload JSON a FastAPI
  Future<bool> procesarCompra(String direccion) async {
    if (_items.isEmpty) return false;

    final body = {
      "direccion_envio": direccion,
      "items": _items.values.map((item) => {
        "producto_id": item.product.id,
        "cantidad": item.cantidad,
      }).toList(),
    };

    try {
      final response = await http.post(
        Uri.parse(_orderUrl),
        headers: {"Content-Type": "application/json"},
        body: json.encode(body),
      );

      if (response.statusCode == 201) {
        limpiarCarrito();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
