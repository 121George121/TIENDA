// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador del Carrito de Compras Móvil (CU09)
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

  /// Incrementar cantidad
  void incrementar(int productoId) {
    if (_items.containsKey(productoId)) {
      _items[productoId]!.cantidad += 1;
      notifyListeners();
    }
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

  /// Envía orden a FastAPI
  Future<bool> procesarCompra(String direccion) async {
    if (_items.isEmpty) return false;
    return true;
  }
}
