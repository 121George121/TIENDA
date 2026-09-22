// ==============================================================================
// CONFIGURACIÓN DE RED Y ENDPOINTS DE LA API (FLUTTER)
// Proyecto: ECOMMERCE_TIENDA
// Ubicación: mobile-app/lib/config/api_config.dart
// ==============================================================================

import 'dart:io';
import 'package:flutter/foundation.dart';

class ApiConfig {
  /// Dirección IP de tu PC en la red local Wi-Fi.
  /// IMPORTANTE: Si pruebas en tu teléfono físico, tu celular y tu PC deben estar
  /// conectados a la misma red Wi-Fi y el backend debe iniciarse con:
  ///   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  static const String pcLocalIp = '192.168.0.104';

  /// Retorna la URL base correspondiente según el dispositivo de ejecución
  static String get baseUrl {
    // Si corre en Web (Chrome / Edge)
    if (kIsWeb) {
      return 'http://localhost:8000/api/v1';
    }

    // Si corre en Android (Teléfono físico o Emulador)
    if (Platform.isAndroid) {
      // Si la IP de la PC está configurada, permite conectar desde el teléfono físico
      if (pcLocalIp.isNotEmpty) {
        return 'http://$pcLocalIp:8000/api/v1';
      }
      // Fallback para emulador estándar de Android Studio
      return 'http://10.0.2.2:8000/api/v1';
    }

    // Windows Desktop / Linux / macOS
    return 'http://127.0.0.1:8000/api/v1';
  }
}
