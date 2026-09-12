// ==============================================================================
// CAPA CONTROLADOR (MVC - CONTROLLER EN FLUTTER / DART)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: mobile-app/lib/controllers/reservation_controller.dart
// ==============================================================================

import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/reservation_model.dart';

class ReservationController extends ChangeNotifier {
  static String get _host {
    if (kIsWeb) return 'http://localhost:8000/api/v1';
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8000/api/v1';
    return 'http://127.0.0.1:8000/api/v1';
  }

  static String get _reservasUrl => '$_host/reservas';

  List<ReservaModel> _reservas = [];
  bool _cargando = false;
  String? _error;

  List<ReservaModel> get reservas => _reservas;
  bool get cargando => _cargando;
  String? get error => _error;

  /// CU10: Convierte el carrito activo en una reserva física
  Future<ReservaModel?> crearReserva({int? sucursalId, String? observaciones}) async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse(_reservasUrl),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          if (sucursalId != null) 'sucursal_id': sucursalId,
          if (observaciones != null) 'observaciones': observaciones,
        }),
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        final nuevaReserva = ReservaModel.fromJson(data);
        _reservas.insert(0, nuevaReserva);
        return nuevaReserva;
      } else {
        final err = json.decode(utf8.decode(response.bodyBytes));
        _error = err['detail'] ?? 'Error al crear la reserva';
        return null;
      }
    } catch (e) {
      _error = 'Error de conexión: $e';
      return null;
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// CU10: Consulta el listado de reservas del usuario
  Future<void> cargarMisReservas() async {
    _cargando = true;
    _error = null;
    notifyListeners();

    try {
      final response = await http.get(Uri.parse('$_reservasUrl/mis-reservas'));
      if (response.statusCode == 200) {
        final List data = json.decode(utf8.decode(response.bodyBytes));
        _reservas = data.map((json) => ReservaModel.fromJson(json)).toList();
      } else {
        _error = 'Error al cargar reservas';
      }
    } catch (e) {
      _error = 'Error de conexión: $e';
    } finally {
      _cargando = false;
      notifyListeners();
    }
  }

  /// CU10: Cancela una reserva pendiente
  Future<bool> cancelarReserva(int id, {String? motivo}) async {
    try {
      final response = await http.patch(
        Uri.parse('$_reservasUrl/$id/cancelar'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'motivo': motivo ?? 'Cancelado desde app móvil'}),
      );
      if (response.statusCode == 200) {
        await cargarMisReservas();
        return true;
      }
      return false;
    } catch (e) {
      debugPrint('Error al cancelar reserva: $e');
      return false;
    }
  }
}
