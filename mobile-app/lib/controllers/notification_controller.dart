// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// CU19 - Gestionar Notificaciones (Web y Móvil)
// Ubicación: mobile-app/lib/controllers/notification_controller.dart
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class NotificacionItem {
  final int id;
  final String titulo;
  final String mensaje;
  final String tipo;
  final bool leido;
  final String? enlace;
  final String fecha;

  NotificacionItem({
    required this.id,
    required this.titulo,
    required this.mensaje,
    required this.tipo,
    required this.leido,
    this.enlace,
    required this.fecha,
  });

  factory NotificacionItem.fromJson(Map<String, dynamic> json) {
    return NotificacionItem(
      id: json['id'],
      titulo: json['titulo'] ?? '',
      mensaje: json['mensaje'] ?? '',
      tipo: json['tipo'] ?? 'INFO',
      leido: json['leido'] ?? false,
      enlace: json['enlace'],
      fecha: json['fecha'] ?? '',
    );
  }
}

class NotificationController extends ChangeNotifier {
  static String get _host {
    if (kIsWeb) return 'http://localhost:8000/api/v1';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1';
    return 'http://127.0.0.1:8000/api/v1';
  }

  List<NotificacionItem> _notificaciones = [];
  bool _cargando = false;
  String? _error;

  List<NotificacionItem> get notificaciones => _notificaciones;
  bool get cargando => _cargando;
  String? get error => _error;

  int get noLeidasCount => _notificaciones.where((n) => !n.leido).length;

  Future<void> fetchNotificaciones(String? token) async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      final headers = <String, String>{};
      if (token != null && token.isNotEmpty) {
        headers['Authorization'] = 'Bearer $token';
      }

      final res = await http.get(
        Uri.parse('$_host/notificaciones'),
        headers: headers,
      );

      if (res.statusCode == 200) {
        final List data = json.decode(utf8.decode(res.bodyBytes));
        _notificaciones = data.map((n) => NotificacionItem.fromJson(n)).toList();
      } else {
        _error = 'Error al cargar notificaciones';
      }
    } catch (e) {
      _error = 'Error de conexión: $e';
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  Future<void> marcarLeida(int id, String? token) async {
    try {
      final headers = <String, String>{};
      if (token != null && token.isNotEmpty) {
        headers['Authorization'] = 'Bearer $token';
      }
      await http.patch(
        Uri.parse('$_host/notificaciones/$id/leer'),
        headers: headers,
      );
      final index = _notificaciones.indexWhere((n) => n.id == id);
      if (index != -1) {
        final old = _notificaciones[index];
        _notificaciones[index] = NotificacionItem(
          id: old.id,
          titulo: old.titulo,
          mensaje: old.mensaje,
          tipo: old.tipo,
          leido: true,
          enlace: old.enlace,
          fecha: old.fecha,
        );
        notifyListeners();
      }
    } catch (e) {
      debugPrint('Error marcar leida: $e');
    }
  }

  Future<void> marcarTodasLeidas(String? token) async {
    try {
      final headers = <String, String>{};
      if (token != null && token.isNotEmpty) {
        headers['Authorization'] = 'Bearer $token';
      }
      await http.post(
        Uri.parse('$_host/notificaciones/marcar-todas-leidas'),
        headers: headers,
      );
      _notificaciones = _notificaciones.map((n) => NotificacionItem(
        id: n.id,
        titulo: n.titulo,
        mensaje: n.mensaje,
        tipo: n.tipo,
        leido: true,
        enlace: n.enlace,
        fecha: n.fecha,
      )).toList();
      notifyListeners();
    } catch (e) {
      debugPrint('Error marcar todas: $e');
    }
  }
}
