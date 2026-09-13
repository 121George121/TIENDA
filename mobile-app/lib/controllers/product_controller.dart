// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador de Estado para CU08: Catálogo y Disponibilidad de Inventario
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/product_model.dart';
import '../models/inventory_model.dart';

class ProductController extends ChangeNotifier {
  static String get _host {
    if (kIsWeb) return 'http://localhost:8000/api/v1';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1';
    return 'http://127.0.0.1:8000/api/v1';
  }

  static String get baseUrl => '$_host/productos';
  static String get inventarioUrl => '$_host/inventario';

  // Lista tradicional (compatibilidad)
  List<ProductModel> _productos = [];
  bool _cargando = false;
  String? _error;

  // CU08: Catálogo enriquecido con disponibilidad por sucursal
  List<CatalogProductModel> _catalogo = [];
  List<BranchModel> _sucursales = [];
  int? _sucursalSeleccionadaId;

  List<ProductModel> get productos => _productos;
  List<CatalogProductModel> get catalogo => _catalogo;
  List<BranchModel> get sucursales => _sucursales;
  int? get sucursalSeleccionadaId => _sucursalSeleccionadaId;
  bool get cargando => _cargando;
  String? get error => _error;

  /// CU08: Obtiene las tiendas físicas para el selector
  Future<void> fetchSucursales() async {
    try {
      final response = await http.get(Uri.parse('$inventarioUrl/sucursales'));
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
        _sucursales = data.map((j) => BranchModel.fromJson(j)).toList();
        if (_sucursales.isNotEmpty && _sucursalSeleccionadaId == null) {
          _sucursalSeleccionadaId = _sucursales.first.id;
        }
        notifyListeners();
      }
    } catch (e) {
      debugPrint('Error al cargar sucursales: $e');
    }
  }

  /// CU08: Cambia la sucursal activa y refresca el inventario en tiempo real
  void seleccionarSucursal(int? sucursalId) {
    _sucursalSeleccionadaId = sucursalId;
    notifyListeners();
    fetchCatalogoConDisponibilidad(sucursalId: sucursalId);
  }

  /// CU08: Consulta el catálogo con existencias y variantes por sucursal
  Future<void> fetchCatalogoConDisponibilidad({int? sucursalId, String? search}) async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      var uri = Uri.parse('$inventarioUrl/catalogo');
      Map<String, String> params = {};

      int? targetSucursal = sucursalId ?? _sucursalSeleccionadaId;
      if (targetSucursal != null) {
        params['sucursal_id'] = targetSucursal.toString();
      }
      if (search != null && search.trim().isNotEmpty) {
        params['search'] = search.trim();
      }

      if (params.isNotEmpty) {
        uri = uri.replace(queryParameters: params);
      }

      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
        _catalogo = data.map((json) => CatalogProductModel.fromJson(json)).toList();

        // Mapear también a _productos para compatibilidad con vistas existentes
        _productos = _catalogo.map((c) => ProductModel(
          id: c.id,
          nombre: c.nombre,
          descripcion: c.descripcion,
          precio: c.preciobase,
          stock: c.stockSucursal,
          imagenUrl: c.imagenprincipal,
          activo: c.disponible
        )).toList();
      } else {
        _error = "Error en el servidor: ${response.statusCode}";
      }
    } catch (e) {
      _error = "Error al consultar catálogo y disponibilidad: $e";
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// Consulta tradicional de productos
  Future<void> fetchProductos() async {
    await fetchSucursales();
    await fetchCatalogoConDisponibilidad();
  }
}
