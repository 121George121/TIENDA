// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Controlador de Estado para CU08: Catálogo y Disponibilidad de Inventario
// Con Sistema de Caché Local Offline-First y Actualización en Segundo Plano
// ==============================================================================

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/product_model.dart';
import '../models/inventory_model.dart';
import '../config/api_config.dart';

import '../services/cache_service.dart';

class ProductController extends ChangeNotifier {
  static String get baseUrl => '${ApiConfig.baseUrl}/productos';
  static String get inventarioUrl => '${ApiConfig.baseUrl}/inventario';

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

  ProductController() {
    // Al instanciar el controlador, cargamos inmediatamente los datos en caché desde disco
    _cargarCacheDesdeDisco();
  }

  // --- GESTIÓN DE CACHÉ LOCAL EN DISCO OFFLINE-FIRST ---

  Future<void> _cargarCacheDesdeDisco() async {
    try {
      // 1. Cargar sucursales cacheadas
      final sucursalesRaw = await CacheService.instance.readJson('sucursales_cache.json');
      if (sucursalesRaw != null && sucursalesRaw.isNotEmpty) {
        final List<dynamic> data = json.decode(sucursalesRaw);
        _sucursales = data.map((j) => BranchModel.fromJson(j)).toList();
        if (_sucursales.isNotEmpty && _sucursalSeleccionadaId == null) {
          _sucursalSeleccionadaId = _sucursales.first.id;
        }
      }

      // 2. Cargar catálogo de poleras cacheado
      final catalogoRaw = await CacheService.instance.readJson('catalogo_cache.json');
      if (catalogoRaw != null && catalogoRaw.isNotEmpty) {
        final List<dynamic> data = json.decode(catalogoRaw);
        _catalogo = data.map((json) => CatalogProductModel.fromJson(json)).toList();
        _productos = _catalogo.map((c) => ProductModel(
          id: c.id,
          nombre: c.nombre,
          descripcion: c.descripcion,
          precio: c.preciobase,
          stock: c.stockSucursal,
          imagenUrl: c.imagenprincipal,
          activo: c.disponible,
        )).toList();
        notifyListeners();
        // Precargar imágenes en disco para que no requieran internet
        CacheService.instance.precacheImages(_catalogo.map((c) => c.imagenprincipal).toList());
      }
    } catch (e) {
      debugPrint('Error inicializando cache de productos desde disco: $e');
    }
  }

  /// CU08: Obtiene las tiendas físicas para el selector
  Future<void> fetchSucursales() async {
    try {
      final response = await http.get(Uri.parse('$inventarioUrl/sucursales')).timeout(const Duration(seconds: 8));
      if (response.statusCode == 200) {
        final raw = utf8.decode(response.bodyBytes);
        final List<dynamic> data = json.decode(raw);
        _sucursales = data.map((j) => BranchModel.fromJson(j)).toList();
        if (_sucursales.isNotEmpty && _sucursalSeleccionadaId == null) {
          _sucursalSeleccionadaId = _sucursales.first.id;
        }
        CacheService.instance.writeJson('sucursales_cache.json', raw);
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
    fetchCatalogoConDisponibilidad(sucursalId: sucursalId, forceRefresh: true);
  }

  /// CU08: Consulta el catálogo con existencias y variantes por sucursal
  /// Utiliza Stale-While-Revalidate: si ya hay datos en pantalla, no muestra spinner y actualiza suavemente en segundo plano
  Future<void> fetchCatalogoConDisponibilidad({int? sucursalId, String? search, bool forceRefresh = false}) async {
    final bool isSearch = search != null && search.trim().isNotEmpty;

    // Solo mostramos pantalla de carga si el catálogo está completamente vacío o si es una búsqueda de texto
    if (_catalogo.isEmpty || isSearch || forceRefresh) {
      if (_catalogo.isEmpty || isSearch) {
        _cargando = true;
      }
      _error = null;
      notifyListeners();
    }

    try {
      var uri = Uri.parse('$inventarioUrl/catalogo');
      Map<String, String> params = {};

      int? targetSucursal = sucursalId ?? _sucursalSeleccionadaId;
      if (targetSucursal != null) {
        params['sucursal_id'] = targetSucursal.toString();
      }
      if (isSearch) {
        params['search'] = search.trim();
      }

      if (params.isNotEmpty) {
        uri = uri.replace(queryParameters: params);
      }

      final response = await http.get(uri).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final rawBody = utf8.decode(response.bodyBytes);
        final List<dynamic> data = json.decode(rawBody);
        _catalogo = data.map((json) => CatalogProductModel.fromJson(json)).toList();

        // Mapear también a _productos para compatibilidad con vistas existentes
        _productos = _catalogo.map((c) => ProductModel(
          id: c.id,
          nombre: c.nombre,
          descripcion: c.descripcion,
          precio: c.preciobase,
          stock: c.stockSucursal,
          imagenUrl: c.imagenprincipal,
          activo: c.disponible,
        )).toList();

        // Guardar en disco el catálogo si es la consulta general (para que no se descargue a cada rato)
        if (!isSearch && (sucursalId == null || sucursalId == _sucursalSeleccionadaId)) {
          CacheService.instance.writeJson('catalogo_cache.json', rawBody);
          CacheService.instance.precacheImages(_catalogo.map((c) => c.imagenprincipal).toList());
        }
        _error = null;
      } else {
        if (_catalogo.isEmpty) {
          _error = "Error en el servidor: ${response.statusCode}";
        }
      }
    } catch (e) {
      if (_catalogo.isEmpty) {
        _error = "Error al consultar catálogo: $e";
      } else {
        debugPrint('Error de red en actualización de fondo (usando cache local): $e');
      }
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// CU08: Consulta la disponibilidad detallada de un producto en todas las sucursales
  Future<ProductAvailabilityModel?> fetchDisponibilidadProducto(int productoId) async {
    try {
      final response = await http.get(Uri.parse('$inventarioUrl/producto/$productoId/disponibilidad')).timeout(const Duration(seconds: 8));
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(utf8.decode(response.bodyBytes));
        return ProductAvailabilityModel.fromJson(data);
      }
    } catch (e) {
      debugPrint('Error al consultar disponibilidad multitienda: $e');
    }
    return null;
  }

  /// Consulta tradicional de productos (con carga de sucursales)
  Future<void> fetchProductos({bool forceRefresh = false}) async {
    await fetchSucursales();
    await fetchCatalogoConDisponibilidad(forceRefresh: forceRefresh);
  }
}

