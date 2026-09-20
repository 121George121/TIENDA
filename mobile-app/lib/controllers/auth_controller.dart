// ==============================================================================
// CONTROLADOR DE AUTENTICACIÓN (MVC - CONTROLLER)
// Gestión de Estado y Servicios REST para Login, Registro, OTP y Recuperación de Contraseña
// ==============================================================================

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';
import '../config/api_config.dart';

class AuthController with ChangeNotifier {
  static String get baseUrl => '${ApiConfig.baseUrl}/auth';

  UserModel? _currentUser;
  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;
  String? _lastDemoOtpCode;

  UserModel? get currentUser => _currentUser;
  bool get isLoggedIn => _currentUser != null;
  bool get isAuthenticated => isLoggedIn;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  String? get successMessage => _successMessage;
  String? get lastDemoOtpCode => _lastDemoOtpCode;

  void clearMessages() {
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();
  }

  /// Registrar nuevo Cliente desde la App Móvil (Genera código OTP)
  Future<bool> registerUser({
    required String nombre,
    required String apellido,
    required String email,
    required String password,
    required String telefono,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    _lastDemoOtpCode = null;
    notifyListeners();

    try {
      final uri = Uri.parse('$baseUrl/registro');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'nombre': nombre,
          'apellido': apellido,
          'email': email,
          'password': password,
          'telefono': telefono,
        }),
      ).timeout(const Duration(seconds: 10));

      final data = json.decode(response.body);

      if (response.statusCode == 201 || response.statusCode == 200) {
        _lastDemoOtpCode = data['codigo_demo'];
        _successMessage = '¡Código de 6 dígitos enviado a tu correo!';
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _errorMessage = data['detail'] ?? 'No se pudo completar el registro.';
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _errorMessage = 'Error de conexión con el servidor ($e)';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Verificar Código OTP de 6 dígitos
  Future<bool> verifyOtpCode(String email, String codigo) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    try {
      final uri = Uri.parse('$baseUrl/verificar-codigo');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'email': email,
          'codigo': codigo,
        }),
      ).timeout(const Duration(seconds: 10));

      final data = json.decode(response.body);

      if (response.statusCode == 200) {
        _currentUser = UserModel.fromJson(data);
        _successMessage = '¡Cuenta verificada exitosamente! Bienvenido.';
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _errorMessage = data['detail'] ?? 'Código de verificación incorrecto o expirado.';
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _errorMessage = 'Error de conexión con el servidor ($e)';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Iniciar Sesión usando la API REST (OAuth2 Form UrlEncoded)
  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    try {
      final uri = Uri.parse('$baseUrl/login');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'username': email,
          'password': password,
        },
      ).timeout(const Duration(seconds: 10));

      final data = json.decode(response.body);

      if (response.statusCode == 200) {
        _currentUser = UserModel.fromJson(data);
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _errorMessage = data['detail'] ?? 'Error al iniciar sesión';
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _errorMessage = 'Error de conexión con el servidor ($e)';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Solicitar Código/Token de Recuperación por Correo Electrónico
  Future<bool> requestPasswordRecovery(String email) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    try {
      final uri = Uri.parse('$baseUrl/recuperar-password');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'email': email}),
      ).timeout(const Duration(seconds: 10));

      final data = json.decode(response.body);

      if (response.statusCode == 200) {
        _successMessage = data['mensaje'] ?? 'Instrucciones enviadas a tu correo.';
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _errorMessage = data['detail'] ?? 'No se pudo procesar la solicitud.';
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _errorMessage = 'Error de conexión con el servidor ($e)';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Restablecer la Contraseña usando Token y Nueva Contraseña
  Future<bool> resetPassword(String token, String newPassword) async {
    _isLoading = true;
    _errorMessage = null;
    _successMessage = null;
    notifyListeners();

    try {
      final uri = Uri.parse('$baseUrl/reset-password');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'token': token,
          'new_password': newPassword,
        }),
      ).timeout(const Duration(seconds: 10));

      final data = json.decode(response.body);

      if (response.statusCode == 200) {
        _successMessage = data['mensaje'] ?? 'Contraseña restablecida exitosamente.';
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _errorMessage = data['detail'] ?? 'El token es inválido o ha expirado.';
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _errorMessage = 'Error de conexión con el servidor ($e)';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Cerrar Sesión
  void logout() {
    _currentUser = null;
    _errorMessage = null;
    _successMessage = null;
    _lastDemoOtpCode = null;
    notifyListeners();
  }
}
