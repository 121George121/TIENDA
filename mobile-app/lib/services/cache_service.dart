// ==============================================================================
// SERVICIO DE CACHÉ LOCAL DISCO (OFFLINE-FIRST & ZERO-LATENCY)
// Ubicación: mobile-app/lib/services/cache_service.dart
// Garantiza la persistencia permanente en el almacenamiento interno del dispositivo:
// 1. Catálogo JSON de poleras y disponibilidad de sucursales.
// 2. Caché persistente de imágenes PNG/JPG en disco (evita re-descargas constantes).
// ==============================================================================

import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;

class CacheService {
  static final CacheService instance = CacheService._internal();
  CacheService._internal();

  Directory? _baseDir;
  Directory? _imagesDir;
  bool _initialized = false;

  bool get isInitialized => _initialized;

  /// Inicializa los directorios seguros en el almacenamiento interno de la app
  Future<void> init() async {
    if (_initialized) return;
    try {
      _baseDir = await getApplicationDocumentsDirectory();
      _imagesDir = Directory('${_baseDir!.path}/garment_cache_images');
      if (!_imagesDir!.existsSync()) {
        _imagesDir!.createSync(recursive: true);
      }
      _initialized = true;
      debugPrint('[CacheService] Inicializado correctamente en: ${_baseDir!.path}');
    } catch (e) {
      debugPrint('[CacheService] Error fatal al inicializar directorios de cache: $e');
    }
  }

  // ==========================================
  // GESTIÓN DE ARCHIVOS JSON DE DATOS
  // ==========================================

  Future<File?> _getFile(String filename) async {
    if (!_initialized) await init();
    if (_baseDir == null) return null;
    return File('${_baseDir!.path}/$filename');
  }

  Future<void> writeJson(String filename, String content) async {
    try {
      final file = await _getFile(filename);
      if (file != null) {
        await file.writeAsString(content, flush: true);
        debugPrint('[CacheService] JSON guardado con éxito: $filename (${content.length} caracteres)');
      }
    } catch (e) {
      debugPrint('[CacheService] Error escribiendo JSON $filename: $e');
    }
  }

  Future<String?> readJson(String filename) async {
    try {
      final file = await _getFile(filename);
      if (file != null && await file.exists()) {
        final content = await file.readAsString();
        if (content.isNotEmpty) {
          debugPrint('[CacheService] JSON recuperado desde disco: $filename (${content.length} caracteres)');
          return content;
        }
      }
    } catch (e) {
      debugPrint('[CacheService] Error leyendo JSON $filename: $e');
    }
    return null;
  }

  // ==========================================
  // GESTIÓN DE CACHÉ DE IMÁGENES DE POLERAS
  // ==========================================

  String _getFilenameForUrl(String url) {
    final hash = url.hashCode.abs();
    String ext = '.png';
    final lower = url.toLowerCase();
    if (lower.contains('.jpg') || lower.contains('.jpeg')) {
      ext = '.jpg';
    } else if (lower.contains('.webp')) {
      ext = '.webp';
    }
    // Extraer identificador final limpio
    final uri = Uri.tryParse(url);
    final lastSegment = (uri?.pathSegments.isNotEmpty == true)
        ? uri!.pathSegments.last.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '_')
        : 'garment';
    return 'polera_${hash}_$lastSegment$ext';
  }

  /// Retorna el archivo en disco si ya fue descargado previamente (0 milisegundos de espera)
  File? getCachedImageFile(String url) {
    if (!_initialized || _imagesDir == null || url.trim().isEmpty) return null;
    final filename = _getFilenameForUrl(url.trim());
    final file = File('${_imagesDir!.path}/$filename');
    if (file.existsSync() && file.lengthSync() > 100) {
      return file;
    }
    return null;
  }

  /// Obtiene la imagen de disco; si no existe, la descarga por red y la almacena en disco
  Future<File?> getOrDownloadImage(String url) async {
    if (url.trim().isEmpty) return null;
    if (!_initialized) await init();
    if (_imagesDir == null) return null;

    final cleanUrl = url.trim();
    final filename = _getFilenameForUrl(cleanUrl);
    final file = File('${_imagesDir!.path}/$filename');

    // 1. Si ya existe en disco y tiene contenido válido (> 100 bytes), retorno inmediato
    if (await file.exists() && await file.length() > 100) {
      return file;
    }

    // 2. Descargar y persistir en disco
    try {
      final response = await http.get(Uri.parse(cleanUrl)).timeout(const Duration(seconds: 15));
      if (response.statusCode == 200 && response.bodyBytes.length > 100) {
        await file.writeAsBytes(response.bodyBytes, flush: true);
        debugPrint('[CacheService] Polera guardada en cache de disco: $filename (${response.bodyBytes.length} bytes)');
        return file;
      }
    } catch (e) {
      debugPrint('[CacheService] Error descargando imagen de polera $cleanUrl: $e');
    }
    return null;
  }

  /// Precarga un lote completo de URLs de poleras en segundo plano
  void precacheImages(List<String?> urls) {
    Future.microtask(() async {
      for (final rawUrl in urls) {
        if (rawUrl == null || rawUrl.trim().isEmpty) continue;
        final url = rawUrl.trim();
        try {
          final cached = getCachedImageFile(url);
          if (cached == null) {
            await getOrDownloadImage(url);
          }
        } catch (_) {}
      }
    });
  }
}
