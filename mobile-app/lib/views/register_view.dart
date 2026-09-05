import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/auth_controller.dart';
import 'verify_otp_view.dart';

class RegisterView extends StatefulWidget {
  const RegisterView({super.key});

  @override
  State<RegisterView> createState() => _RegisterViewState();
}

class _RegisterViewState extends State<RegisterView> {
  final _formKey = GlobalKey<FormState>();

  final TextEditingController _nombreCtrl = TextEditingController();
  final TextEditingController _apellidoCtrl = TextEditingController();
  final TextEditingController _emailCtrl = TextEditingController();
  final TextEditingController _phoneCtrl = TextEditingController();
  final TextEditingController _passwordCtrl = TextEditingController();

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
    _nombreCtrl.dispose();
    _apellidoCtrl.dispose();
    _emailCtrl.dispose();
    _phoneCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  void _onRegisterPressed() async {
    if (!_formKey.currentState!.validate()) return;
    if (!_isPasswordValid) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Por favor cumple con todos los requisitos de la contraseña'),
          backgroundColor: Color(0xFFE11D48),
        ),
      );
      return;
    }

    FocusScope.of(context).unfocus();
    final authController = Provider.of<AuthController>(context, listen: false);

    final email = _emailCtrl.text.trim();

    final success = await authController.registerUser(
      nombre: _nombreCtrl.text.trim(),
      apellido: _apellidoCtrl.text.trim(),
      email: email,
      password: _passwordCtrl.text,
      telefono: _phoneCtrl.text.trim(),
    );

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(authController.successMessage ?? '¡Código enviado a tu correo!'),
          backgroundColor: Colors.green.shade700,
        ),
      );
      // Redirigir a la pantalla de verificación OTP
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => VerifyOtpView(email: email),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(authController.errorMessage ?? 'Error al registrarte'),
          backgroundColor: const Color(0xFFE11D48),
        ),
      );
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
          icon: const Icon(Icons.arrow_back_ios_new, color: Color(0xFF0F172A)),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 28.0, vertical: 12.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header Logo / Icon
                Center(
                  child: Container(
                    width: 70,
                    height: 70,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFFE11D48), Color(0xFFBE123C)],
                      ),
                      borderRadius: BorderRadius.circular(22),
                      boxShadow: const [
                        BoxShadow(
                          color: Color(0x40E11D48),
                          blurRadius: 16,
                          offset: Offset(0, 6),
                        )
                      ],
                    ),
                    child: const Icon(
                      Icons.person_add_alt_1_rounded,
                      color: Colors.white,
                      size: 34,
                    ),
                  ),
                ),
                const SizedBox(height: 18),

                const Center(
                  child: Text(
                    'Crear Cuenta de Cliente',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.w800,
                      color: Color(0xFF0F172A),
                    ),
                  ),
                ),
                const SizedBox(height: 6),
                const Center(
                  child: Text(
                    'Únete a T-Shirt Boutique para comprar poleras exclusivas',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 14,
                      color: Color(0xFF64748B),
                    ),
                  ),
                ),
                const SizedBox(height: 28),

                // Campo Nombre
                TextFormField(
                  controller: _nombreCtrl,
                  decoration: _buildInputDecoration('Nombre', Icons.person_outline),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Ingresa tu nombre';
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                // Campo Apellido
                TextFormField(
                  controller: _apellidoCtrl,
                  decoration: _buildInputDecoration('Apellido', Icons.badge_outlined),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Ingresa tu apellido';
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                // Campo Email
                TextFormField(
                  controller: _emailCtrl,
                  keyboardType: TextInputType.emailAddress,
                  decoration: _buildInputDecoration('Correo Electrónico', Icons.email_outlined),
                  validator: (val) {
                    if (val == null || val.trim().isEmpty) return 'Ingresa tu correo';
                    if (!val.contains('@')) return 'Correo electrónico no válido';
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                // Campo Teléfono
                TextFormField(
                  controller: _phoneCtrl,
                  keyboardType: TextInputType.phone,
                  decoration: _buildInputDecoration('Teléfono / WhatsApp', Icons.phone_outlined),
                ),
                const SizedBox(height: 16),

                // Campo Contraseña
                TextFormField(
                  controller: _passwordCtrl,
                  obscureText: _obscurePassword,
                  onChanged: _onPasswordChanged,
                  decoration: _buildInputDecoration('Contraseña', Icons.lock_outline).copyWith(
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                        color: const Color(0xFF94A3B8),
                      ),
                      onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                    ),
                  ),
                  validator: (val) {
                    if (!_isPasswordValid) return 'Revisa los requisitos de contraseña abajo';
                    return null;
                  },
                ),
                const SizedBox(height: 14),

                // Tarjeta de Requisitos de Contraseña en Tiempo Real
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: _isPasswordValid ? const Color(0xFFECFDF5) : Colors.white,
                    borderRadius: BorderRadius.circular(16),
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
                            size: 18,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            _isPasswordValid ? '¡Contraseña Segura Aprobada!' : 'Requisitos de Contraseña:',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.bold,
                              color: _isPasswordValid ? const Color(0xFF047857) : const Color(0xFF334155),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      _buildRequirementRow('Mínimo 8 caracteres', _hasMinLength),
                      _buildRequirementRow('Al menos 1 letra Mayúscula (A-Z)', _hasUppercase),
                      _buildRequirementRow('Al menos 1 letra Minúscula (a-z)', _hasLowercase),
                      _buildRequirementRow('Al menos 1 Número (0-9)', _hasNumber),
                      _buildRequirementRow('Al menos 1 Carácter especial (!@#\$%^&*)', _hasSpecialChar),
                    ],
                  ),
                ),
                const SizedBox(height: 28),

                // Botón Registrarse (Solo se ilumina cuando _isPasswordValid es true)
                SizedBox(
                  width: double.infinity,
                  height: 54,
                  child: ElevatedButton(
                    onPressed: (authController.isLoading || !_isPasswordValid) ? null : _onRegisterPressed,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _isPasswordValid ? const Color(0xFFE11D48) : const Color(0xFFCBD5E1),
                      disabledBackgroundColor: const Color(0xFFE2E8F0),
                      elevation: _isPasswordValid ? 4 : 0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      shadowColor: const Color(0x40E11D48),
                    ),
                    child: authController.isLoading
                        ? const SizedBox(
                            width: 24,
                            height: 24,
                            child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                          )
                        : Text(
                            'Registrarme Ahora',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                              color: _isPasswordValid ? Colors.white : const Color(0xFF94A3B8),
                            ),
                          ),
                  ),
                ),
                const SizedBox(height: 20),

                // Enlace a Login
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text(
                      '¿Ya tienes cuenta? ',
                      style: TextStyle(color: Color(0xFF64748B)),
                    ),
                    GestureDetector(
                      onTap: () => Navigator.pop(context),
                      child: const Text(
                        'Inicia Sesión',
                        style: TextStyle(
                          color: Color(0xFFE11D48),
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRequirementRow(String text, bool satisfied) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6.0),
      child: Row(
        children: [
          AnimatedContainer(
            duration: const Duration(milliseconds: 250),
            width: 18,
            height: 18,
            decoration: BoxDecoration(
              color: satisfied ? const Color(0xFF10B981) : Colors.transparent,
              shape: BoxShape.circle,
              border: Border.all(
                color: satisfied ? const Color(0xFF10B981) : const Color(0xFF94A3B8),
                width: 1.5,
              ),
            ),
            child: satisfied
                ? const Icon(Icons.check, size: 12, color: Colors.white)
                : null,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: AnimatedDefaultTextStyle(
              duration: const Duration(milliseconds: 250),
              style: TextStyle(
                fontSize: 13,
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

  InputDecoration _buildInputDecoration(String label, IconData icon) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Color(0xFF64748B), fontSize: 14),
      prefixIcon: Icon(icon, color: const Color(0xFF94A3B8)),
      filled: true,
      fillColor: Colors.white,
      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: Color(0xFFE11D48), width: 2),
      ),
    );
  }
}
