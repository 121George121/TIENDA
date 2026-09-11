// ==============================================================================
// VISTA DE RESTABLECER CONTRASEÑA (MVC - VIEW)
// Formulario para ingresar token y establecer nueva contraseña con checklist en vivo
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/auth_controller.dart';

class ResetPasswordView extends StatefulWidget {
  const ResetPasswordView({Key? key}) : super(key: key);

  @override
  State<ResetPasswordView> createState() => _ResetPasswordViewState();
}

class _ResetPasswordViewState extends State<ResetPasswordView> {
  final _formKey = GlobalKey<FormState>();
  final _tokenController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  bool _obscurePassword = true;

  // Estados de Validación en Tiempo Real para la Contraseña
  bool _hasMinLength = false;
  bool _hasUppercase = false;
  bool _hasLowercase = false;
  bool _hasNumber = false;
  bool _hasSpecialChar = false;

  bool get _isPasswordValid =>
      _hasMinLength && _hasUppercase && _hasLowercase && _hasNumber && _hasSpecialChar;

  void _onPasswordChanged(String val) {
    setState(() {
      _hasMinLength = val.length >= 8;
      _hasUppercase = RegExp(r'[A-Z]').hasMatch(val);
      _hasLowercase = RegExp(r'[a-z]').hasMatch(val);
      _hasNumber = RegExp(r'[0-9]').hasMatch(val);
      _hasSpecialChar = RegExp(r'[\W_]').hasMatch(val);
    });
  }

  @override
  void dispose() {
    _tokenController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  void _handleReset() async {
    if (!_formKey.currentState!.validate()) return;
    if (!_isPasswordValid) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Por favor cumple con todos los requisitos de la nueva contraseña'),
          backgroundColor: Color(0xFFE11D48),
        ),
      );
      return;
    }

    final authController = Provider.of<AuthController>(context, listen: false);
    final success = await authController.resetPassword(
      _tokenController.text.trim(),
      _passwordController.text,
    );

    if (success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(authController.successMessage ?? '¡Contraseña actualizada! Inicia sesión.'),
          backgroundColor: Colors.green.shade700,
        ),
      );
      Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final authController = Provider.of<AuthController>(context);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new, color: Color(0xFF0F172A), size: 20),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFE4E6),
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.lock_reset_outlined,
                    size: 48,
                    color: Color(0xFFE11D48),
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Restablecer Contraseña',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF0F172A),
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'Ingresa tu token de recuperación y la nueva contraseña.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade600,
                  ),
                ),
                const SizedBox(height: 28),

                Card(
                  elevation: 2,
                  shadowColor: Colors.black.withOpacity(0.05),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          if (authController.errorMessage != null) ...[
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: const Color(0xFFFEF2F2),
                                borderRadius: BorderRadius.circular(10),
                                border: Border.all(color: const Color(0xFFFCA5A5)),
                              ),
                              child: Row(
                                children: [
                                  const Icon(Icons.error_outline, color: Color(0xFFEF4444), size: 20),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      authController.errorMessage!,
                                      style: const TextStyle(color: Color(0xFF991B1B), fontSize: 13),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(height: 16),
                          ],

                          // Campo Token
                          const Text(
                            'Token de Recuperación',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF334155),
                            ),
                          ),
                          const SizedBox(height: 8),
                          TextFormField(
                            controller: _tokenController,
                            decoration: InputDecoration(
                              hintText: 'Pega tu token recibido por correo',
                              prefixIcon: const Icon(Icons.vpn_key_outlined, size: 20),
                              filled: true,
                              fillColor: const Color(0xFFF8FAFC),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(10),
                                borderSide: BorderSide(color: Colors.grey.shade300),
                              ),
                            ),
                            validator: (val) {
                              if (val == null || val.trim().isEmpty) return 'El token es requerido';
                              return null;
                            },
                          ),
                          const SizedBox(height: 18),

                          // Campo Nueva Contraseña
                          const Text(
                            'Nueva Contraseña',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF334155),
                            ),
                          ),
                          const SizedBox(height: 8),
                          TextFormField(
                            controller: _passwordController,
                            obscureText: _obscurePassword,
                            onChanged: _onPasswordChanged,
                            decoration: InputDecoration(
                              hintText: '••••••••',
                              prefixIcon: const Icon(Icons.lock_outline, size: 20),
                              suffixIcon: IconButton(
                                icon: Icon(
                                  _obscurePassword ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                                  size: 20,
                                ),
                                onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                              ),
                              filled: true,
                              fillColor: const Color(0xFFF8FAFC),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(10),
                                borderSide: BorderSide(color: Colors.grey.shade300),
                              ),
                            ),
                            validator: (val) {
                              if (!_isPasswordValid) return 'Revisa los requisitos abajo';
                              return null;
                            },
                          ),
                          const SizedBox(height: 14),

                          // Tarjeta de Requisitos de Contraseña en Tiempo Real
                          Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(14),
                            decoration: BoxDecoration(
                              color: _isPasswordValid ? const Color(0xFFECFDF5) : const Color(0xFFF8FAFC),
                              borderRadius: BorderRadius.circular(14),
                              border: Border.all(
                                color: _isPasswordValid ? const Color(0xFF10B981) : const Color(0xFFE2E8F0),
                                width: _isPasswordValid ? 2 : 1,
                              ),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      _isPasswordValid ? Icons.verified : Icons.security_outlined,
                                      color: _isPasswordValid ? const Color(0xFF10B981) : const Color(0xFF64748B),
                                      size: 16,
                                    ),
                                    const SizedBox(width: 8),
                                    Text(
                                      _isPasswordValid ? '¡Contraseña Válida!' : 'Requisitos de Seguridad:',
                                      style: TextStyle(
                                        fontSize: 12,
                                        fontWeight: FontWeight.bold,
                                        color: _isPasswordValid ? const Color(0xFF047857) : const Color(0xFF334155),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                _buildRequirementRow('Mínimo 8 caracteres', _hasMinLength),
                                _buildRequirementRow('Al menos 1 letra Mayúscula (A-Z)', _hasUppercase),
                                _buildRequirementRow('Al menos 1 letra Minúscula (a-z)', _hasLowercase),
                                _buildRequirementRow('Al menos 1 Número (0-9)', _hasNumber),
                                _buildRequirementRow('Al menos 1 Carácter especial (!@#\$%^&*)', _hasSpecialChar),
                              ],
                            ),
                          ),
                          const SizedBox(height: 18),

                          // Confirmar Contraseña
                          const Text(
                            'Confirmar Nueva Contraseña',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF334155),
                            ),
                          ),
                          const SizedBox(height: 8),
                          TextFormField(
                            controller: _confirmPasswordController,
                            obscureText: _obscurePassword,
                            decoration: InputDecoration(
                              hintText: 'Repite la contraseña',
                              prefixIcon: const Icon(Icons.lock_reset_outlined, size: 20),
                              filled: true,
                              fillColor: const Color(0xFFF8FAFC),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(10),
                                borderSide: BorderSide(color: Colors.grey.shade300),
                              ),
                            ),
                            validator: (val) {
                              if (val != _passwordController.text) {
                                return 'Las contraseñas no coinciden';
                              }
                              return null;
                            },
                          ),
                          const SizedBox(height: 24),

                          ElevatedButton(
                            onPressed: (authController.isLoading || !_isPasswordValid) ? null : _handleReset,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: _isPasswordValid ? const Color(0xFFE11D48) : const Color(0xFFCBD5E1),
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 14),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                              elevation: _isPasswordValid ? 2 : 0,
                            ),
                            child: authController.isLoading
                                ? const SizedBox(
                                    height: 20,
                                    width: 20,
                                    child: CircularProgressIndicator(strokeWidth: 2, valueColor: AlwaysStoppedAnimation(Colors.white)),
                                  )
                                : const Text('Cambiar Contraseña', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRequirementRow(String text, bool satisfied) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 5.0),
      child: Row(
        children: [
          AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            width: 16,
            height: 16,
            decoration: BoxDecoration(
              color: satisfied ? const Color(0xFF10B981) : Colors.transparent,
              shape: BoxShape.circle,
              border: Border.all(
                color: satisfied ? const Color(0xFF10B981) : const Color(0xFF94A3B8),
                width: 1.5,
              ),
            ),
            child: satisfied
                ? const Icon(Icons.check, size: 10, color: Colors.white)
                : null,
          ),
          const SizedBox(width: 8),
          Expanded(
            child: AnimatedDefaultTextStyle(
              duration: const Duration(milliseconds: 200),
              style: TextStyle(
                fontSize: 12,
                fontWeight: satisfied ? FontWeight.bold : FontWeight.normal,
                color: satisfied ? const Color(0xFF047857) : const Color(0xFF64748B),
              ),
              child: Text(text),
            ),
          ),
        ],
      ),
    );
  }
}
