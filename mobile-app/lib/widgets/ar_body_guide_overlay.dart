// ==============================================================================
// WIDGET: GUÍA DE CALIBRACIÓN CORPORAL AR (CU12)
// Ubicación: mobile-app/lib/widgets/ar_body_guide_overlay.dart
// Muestra una silueta guía y líneas de referencia para que el usuario
// encuadre hombros, torso y cabeza frente a la cámara o selfie.
// ==============================================================================

import 'package:flutter/material.dart';

class ArBodyGuideOverlay extends StatelessWidget {
  final bool visible;
  final VoidCallback? onToggle;

  const ArBodyGuideOverlay({
    super.key,
    this.visible = true,
    this.onToggle,
  });

  @override
  Widget build(BuildContext context) {
    if (!visible) return const SizedBox.shrink();

    return IgnorePointer(
      child: Stack(
        children: [
          CustomPaint(
            size: Size.infinite,
            painter: _BodyGuidePainter(),
          ),
          Positioned(
            top: 20,
            left: 20,
            right: 20,
            child: Center(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.black.withValues(alpha: 0.65),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFF38BDF8).withValues(alpha: 0.5)),
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.center_focus_strong, size: 16, color: Color(0xFF38BDF8)),
                    SizedBox(width: 8),
                    Text(
                      'Alinea tus hombros con la guía punteada',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        letterSpacing: 0.3,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _BodyGuidePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;

    final guidePaint = Paint()
      ..color = const Color(0xFF38BDF8).withValues(alpha: 0.35)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.6;

    final linePaint = Paint()
      ..color = Colors.white.withValues(alpha: 0.25)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0;

    // 1. Óvalo de Referencia de Cabeza
    final headCenter = Offset(w * 0.5, h * 0.22);
    canvas.drawOval(
      Rect.fromCenter(center: headCenter, width: w * 0.32, height: h * 0.18),
      guidePaint,
    );

    // 2. Línea de Hombros de referencia
    final shoulderY = h * 0.34;
    canvas.drawLine(
      Offset(w * 0.18, shoulderY),
      Offset(w * 0.82, shoulderY),
      linePaint,
    );

    // Marcas de hombro izquierdo y derecho
    canvas.drawCircle(Offset(w * 0.22, shoulderY), 4, guidePaint);
    canvas.drawCircle(Offset(w * 0.78, shoulderY), 4, guidePaint);

    // 3. Silueta de Torso Suave
    final torsoPath = Path()
      ..moveTo(w * 0.22, shoulderY)
      ..quadraticBezierTo(w * 0.25, h * 0.55, w * 0.27, h * 0.70)
      ..lineTo(w * 0.73, h * 0.70)
      ..quadraticBezierTo(w * 0.75, h * 0.55, w * 0.78, shoulderY);

    canvas.drawPath(torsoPath, linePaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
