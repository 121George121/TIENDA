// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador del Carrito de Compras en la Aplicación Móvil (CU09)
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/product_model.dart';
import '../models/cart_item_model.dart';

class CartController extends ChangeNotifier {
  static String get _host {
    if (kIsWeb) return 'http://localhost:8000/api/v1';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1';
    return 'http://127.0.0.1:8000/api/v1';
  }

  static String get _carritoUrl => '$_host/carrito';
  static String get _orderUrl => '$_host/ordenes/';

  final Map<int, CartItemModel> _items = {};
  int? _sucursalId;
  String? _sucursalNombre;
  bool _cargando = false;

  Map<int, CartItemModel> get items => _items;
  int? get sucursalId => _sucursalId;
  String? get sucursalNombre => _sucursalNombre;
  bool get cargando => _cargando;

  int get totalItemCount {
    return _items.values.fold(0, (sum, item) => sum + item.cantidad);
  }

  double get totalMonto {
    return _items.values.fold(0.0, (sum, item) => sum + item.subtotal);
  }

  /// Añadir producto al carrito
  void agregarProducto(ProductModel producto) {
    if (_items.containsKey(producto.id)) {
      _items[producto.id]!.cantidad += 1;
    } else {
      _items[producto.id] = CartItemModel(product: producto);
    }
    notifyListeners();
  }

  /// Establecer sucursal activa para reserva o retiro
  void setSucursal(int id, String nombre) {
    _sucursalId = id;
    _sucursalNombre = nombre;
    notifyListeners();
  }

  /// Incrementar cantidad validando el stock disponible del producto
  bool incrementar(int productoId) {
    if (_items.containsKey(productoId)) {
      final item = _items[productoId]!;
      if (item.cantidad < item.product.stock) {
        item.cantidad += 1;
        notifyListeners();
        return true;
      }
      return false; // Límite de stock alcanzado
    }
    return false;
  }

  /// Decrementar cantidad o remover si llega a 0
  void decrementar(int productoId) {
    if (_items.containsKey(productoId)) {
      if (_items[productoId]!.cantidad > 1) {
        _items[productoId]!.cantidad -= 1;
      } else {
        _items.remove(productoId);
      }
      notifyListeners();
    }
  }

  void removerProducto(int productoId) {
    _items.remove(productoId);
    notifyListeners();
  }

  void limpiarCarrito() {
    _items.clear();
    notifyListeners();
  }

  /// Sincroniza el carrito con la API de FastAPI
  Future<void> sincronizarConApi() async {
    _cargando = true;
    notifyListeners();
    try {
      final response = await http.get(Uri.parse(_carritoUrl));
      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        _sucursalId = data['sucursal_id'];
        _sucursalNombre = data['sucursal_nombre'];
      }
    } catch (e) {
      debugPrint('Error al sincronizar carrito: $e');
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// Procesa la compra enviando el payload JSON a FastAPI
  Future<bool> procesarCompra(String direccion, {String? authToken}) async {
    if (_items.isEmpty) return false;

    final body = {
      "direccion_envio": direccion,
      "items": _items.values.map((item) => {
        "producto_id": item.product.id,
        "cantidad": item.cantidad,
      }).toList(),
    };

    try {
      final headers = <String, String>{
        "Content-Type": "application/json",
      };
      if (authToken != null && authToken.isNotEmpty) {
        headers["Authorization"] = "Bearer $authToken";
      }

      final response = await http.post(
        Uri.parse(_orderUrl),
        headers: headers,
        body: json.encode(body),
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 201 || response.statusCode == 200) {
        limpiarCarrito();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
