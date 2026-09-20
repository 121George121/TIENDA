// ==============================================================================
// WIDGET: PRENDA REALISTA PARA VESTIDOR VIRTUAL AR (CU12)
// Ubicación: mobile-app/lib/widgets/realistic_garment_widget.dart
// Dibuja la silueta anatómica de prendas (Polera, Cuello V, Polo, Hoodie)
// con sombreado volumétrico de tela, pliegues realistas y estampado centrado.
// ==============================================================================

import 'package:flutter/material.dart';

enum GarmentType { poleraCuelloRedondo, poleraCuelloV, poleraPolo, hoodie }

class RealisticGarmentWidget extends StatelessWidget {
  final Color color;
  final String? imagenUrl;
  final String nombreProducto;
  final GarmentType tipoPrenda;
  final double opacidad;
  final bool mostrarEstampado;
  final bool usarModoRecorteCompleto;

  const RealisticGarmentWidget({
    super.key,
    required this.color,
    this.imagenUrl,
    required this.nombreProducto,
    this.tipoPrenda = GarmentType.poleraCuelloRedondo,
    this.opacidad = 1.0,
    this.mostrarEstampado = true,
    this.usarModoRecorteCompleto = false,
  });

  @override
  Widget build(BuildContext context) {
    return Opacity(
      opacity: opacidad.clamp(0.1, 1.0),
      child: AspectRatio(
        aspectRatio: 0.88, // Proporción anatómica estándar ancho/alto de torso
        child: LayoutBuilder(
          builder: (context, constraints) {
            final size = Size(constraints.maxWidth, constraints.maxHeight);

            return Stack(
              fit: StackFit.expand,
              children: [
                // 1. Sombra suave proyectada detrás de la prenda
                CustomPaint(
                  size: size,
                  painter: _GarmentDropShadowPainter(tipoPrenda),
                ),

                // 2. Prenda Base con Iluminación y Pliegues Realistas
                if (usarModoRecorteCompleto && imagenUrl != null)
                  ClipPath(
                    clipper: GarmentClipper(tipoPrenda),
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        // Imagen de catálogo recortada a la silueta exacta
                        Image.network(
                          imagenUrl!,
                          fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) => _buildVectorGarment(size),
                        ),
                        // Tinte de color suave encima con modo de fusión
                        Container(
                          color: color.withValues(alpha: 0.35),
                        ),
                        // Sombras de tela y cuello por encima
                        CustomPaint(
                          size: size,
                          painter: RealisticGarmentOverlayPainter(
                            tipoPrenda: tipoPrenda,
                            colorBase: color,
                          ),
                        ),
                      ],
                    ),
                  )
                else
                  _buildVectorGarment(size),

                // 3. Estampado / Gráfico del Producto en el Pecho (Centrado y con perspectiva de tela)
                if (mostrarEstampado && !usarModoRecorteCompleto)
                  _buildEstampadoPecho(size),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildVectorGarment(Size size) {
    return CustomPaint(
      size: size,
      painter: RealisticGarmentPainter(
        color: color,
        tipoPrenda: tipoPrenda,
      ),
    );
  }

  Widget _buildEstampadoPecho(Size size) {
    // Zona de serigrafía centrada en el pecho
    final printWidth = size.width * 0.38;
    final printHeight = size.height * 0.32;
    final topMargin = size.height * 0.28;

    return Positioned(
      top: topMargin,
      left: (size.width - printWidth) / 2,
      width: printWidth,
      height: printHeight,
      child: Center(
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.12),
                blurRadius: 6,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: imagenUrl != null && imagenUrl!.isNotEmpty
                ? Image.network(
                    imagenUrl!,
                    fit: BoxFit.contain,
                    errorBuilder: (_, __, ___) => _buildLogoEmblema(),
                  )
                : _buildLogoEmblema(),
          ),
        ),
      ),
    );
  }

  Widget _buildLogoEmblema() {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.08),
        border: Border.all(color: Colors.white.withValues(alpha: 0.2)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            tipoPrenda == GarmentType.hoodie ? Icons.dry_cleaning : Icons.checkroom,
            size: 28,
            color: Colors.white.withValues(alpha: 0.85),
          ),
          const SizedBox(height: 4),
          Text(
            nombreProducto,
            maxLines: 2,
            textAlign: TextAlign.center,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.bold,
              color: Colors.white.withValues(alpha: 0.9),
              letterSpacing: 0.5,
              shadows: const [
                Shadow(color: Colors.black45, blurRadius: 4, offset: Offset(0, 1))
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ==============================================================================
// CLIPPER: RECORTA CUALQUIER IMAGEN A LA SILUETA EXACTA DE LA PRENDA
// ==============================================================================
class GarmentClipper extends CustomClipper<Path> {
  final GarmentType tipo;

  GarmentClipper(this.tipo);

  @override
  Path getClip(Size size) {
    return _crearPathPrenda(size, tipo);
  }

  @override
  bool shouldReclip(covariant GarmentClipper oldClipper) => oldClipper.tipo != tipo;
}

// ==============================================================================
// PAINTER: SOMBRA ARROJADA BAJO LA PRENDA
// ==============================================================================
class _GarmentDropShadowPainter extends CustomPainter {
  final GarmentType tipo;
  _GarmentDropShadowPainter(this.tipo);

  @override
  void paint(Canvas canvas, Size size) {
    final path = _crearPathPrenda(size, tipo);
    final shadowPaint = Paint()
      ..color = Colors.black.withValues(alpha: 0.28)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 16);

    canvas.save();
    canvas.translate(0, 10);
    canvas.drawPath(path, shadowPaint);
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// ==============================================================================
// PAINTER: RENDERIZADO VECTORIAL 3D DE LA PRENDA CON TEXTURA Y LUCES
// ==============================================================================
class RealisticGarmentPainter extends CustomPainter {
  final Color color;
  final GarmentType tipoPrenda;

  RealisticGarmentPainter({required this.color, required this.tipoPrenda});

  @override
  void paint(Canvas canvas, Size size) {
    final garmentPath = _crearPathPrenda(size, tipoPrenda);

    // 1. Capa de color base con gradiente de iluminación cenital (luz en hombros y centro)
    final lightColor = _aclararColor(color, 0.22);
    final darkColor = _oscurecerColor(color, 0.30);

    final baseGradient = RadialGradient(
      center: const Alignment(0.0, -0.4),
      radius: 1.1,
      colors: [lightColor, color, darkColor],
      stops: const [0.0, 0.55, 1.0],
    );

    final basePaint = Paint()
      ..shader = baseGradient.createShader(Rect.fromLTWH(0, 0, size.width, size.height))
      ..style = PaintingStyle.fill;

    canvas.drawPath(garmentPath, basePaint);

    // 2. Dibujar pliegues de tela y sombras orgánicas
    _dibujarPlieguesDeTela(canvas, size, darkColor);

    // 3. Dibujar cuello, ribete y costuras
    _dibujarCuelloYDetalles(canvas, size, color, darkColor, lightColor);

    // 4. Borde sutil exterior para acabado de alta costura
    final borderPaint = Paint()
      ..color = darkColor.withValues(alpha: 0.4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4;
    canvas.drawPath(garmentPath, borderPaint);
  }

  void _dibujarPlieguesDeTela(Canvas canvas, Size size, Color shadowColor) {
    final w = size.width;
    final h = size.height;

    final shadowPaint = Paint()
      ..color = shadowColor.withValues(alpha: 0.35)
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 2.2
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3);

    // Pliegue axila izquierda
    final pLeft = Path()
      ..moveTo(w * 0.24, h * 0.40)
      ..quadraticBezierTo(w * 0.32, h * 0.48, w * 0.36, h * 0.56);
    canvas.drawPath(pLeft, shadowPaint);

    // Pliegue axila derecha
    final pRight = Path()
      ..moveTo(w * 0.76, h * 0.40)
      ..quadraticBezierTo(w * 0.68, h * 0.48, w * 0.64, h * 0.56);
    canvas.drawPath(pRight, shadowPaint);

    // Pliegues suaves de torso (cintura)
    final pWaistLeft = Path()
      ..moveTo(w * 0.26, h * 0.68)
      ..quadraticBezierTo(w * 0.38, h * 0.71, w * 0.44, h * 0.70);
    canvas.drawPath(pWaistLeft, shadowPaint);

    final pWaistRight = Path()
      ..moveTo(w * 0.74, h * 0.70)
      ..quadraticBezierTo(w * 0.62, h * 0.73, w * 0.56, h * 0.71);
    canvas.drawPath(pWaistRight, shadowPaint);
  }

  void _dibujarCuelloYDetalles(
    Canvas canvas,
    Size size,
    Color baseColor,
    Color darkColor,
    Color lightColor,
  ) {
    final w = size.width;
    final h = size.height;

    final ribPaint = Paint()
      ..color = darkColor.withValues(alpha: 0.65)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.5;

    final innerNeckPaint = Paint()
      ..color = _oscurecerColor(darkColor, 0.4)
      ..style = PaintingStyle.fill;

    if (tipoPrenda == GarmentType.poleraCuelloRedondo) {
      // Interior del cuello (vista interna de la espalda)
      final backNeckPath = Path()
        ..moveTo(w * 0.37, h * 0.08)
        ..quadraticBezierTo(w * 0.50, h * 0.04, w * 0.63, h * 0.08)
        ..quadraticBezierTo(w * 0.50, h * 0.14, w * 0.37, h * 0.08);
      canvas.drawPath(backNeckPath, innerNeckPaint);

      // Ribete frontal del cuello
      final ribPath = Path()
        ..moveTo(w * 0.37, h * 0.08)
        ..quadraticBezierTo(w * 0.50, h * 0.16, w * 0.63, h * 0.08);
      canvas.drawPath(ribPath, ribPaint);
    } else if (tipoPrenda == GarmentType.poleraCuelloV) {
      // Interior del cuello en V
      final backNeckPath = Path()
        ..moveTo(w * 0.38, h * 0.08)
        ..quadraticBezierTo(w * 0.50, h * 0.04, w * 0.62, h * 0.08)
        ..lineTo(w * 0.50, h * 0.19)
        ..close();
      canvas.drawPath(backNeckPath, innerNeckPaint);

      // Cuello en V ribeteado
      final vNeck = Path()
        ..moveTo(w * 0.38, h * 0.08)
        ..lineTo(w * 0.50, h * 0.21)
        ..lineTo(w * 0.62, h * 0.08);
      canvas.drawPath(vNeck, ribPaint);
    } else if (tipoPrenda == GarmentType.poleraPolo) {
      // Cuello con solapa y botones
      final collarPath = Path()
        ..moveTo(w * 0.36, h * 0.08)
        ..lineTo(w * 0.44, h * 0.18)
        ..lineTo(w * 0.50, h * 0.14)
        ..lineTo(w * 0.56, h * 0.18)
        ..lineTo(w * 0.64, h * 0.08)
        ..quadraticBezierTo(w * 0.50, h * 0.04, w * 0.36, h * 0.08);

      final collarFill = Paint()..color = _aclararColor(baseColor, 0.1);
      canvas.drawPath(collarPath, collarFill);
      canvas.drawPath(collarPath, ribPaint);

      // Tapeta central con botones
      final placket = Rect.fromCenter(
        center: Offset(w * 0.5, h * 0.22),
        width: w * 0.06,
        height: h * 0.14,
      );
      canvas.drawRect(placket, Paint()..color = darkColor.withValues(alpha: 0.4));
      // Botón 1 y 2
      final buttonPaint = Paint()..color = Colors.white70;
      canvas.drawCircle(Offset(w * 0.5, h * 0.18), 3, buttonPaint);
      canvas.drawCircle(Offset(w * 0.5, h * 0.24), 3, buttonPaint);
    } else if (tipoPrenda == GarmentType.hoodie) {
      // Capucha envolvente
      final hoodPath = Path()
        ..moveTo(w * 0.32, h * 0.12)
        ..cubicTo(w * 0.32, h * -0.04, w * 0.68, h * -0.04, w * 0.68, h * 0.12)
        ..quadraticBezierTo(w * 0.50, h * 0.18, w * 0.32, h * 0.12);

      final hoodPaint = Paint()..color = _oscurecerColor(baseColor, 0.15);
      canvas.drawPath(hoodPath, hoodPaint);
      canvas.drawPath(hoodPath, ribPaint);

      // Bolsillo canguro frontal
      final pocketPath = Path()
        ..moveTo(w * 0.32, h * 0.65)
        ..lineTo(w * 0.38, h * 0.58)
        ..lineTo(w * 0.62, h * 0.58)
        ..lineTo(w * 0.68, h * 0.65)
        ..lineTo(w * 0.68, h * 0.82)
        ..lineTo(w * 0.32, h * 0.82)
        ..close();

      canvas.drawPath(pocketPath, Paint()..color = darkColor.withValues(alpha: 0.25));
      canvas.drawPath(pocketPath, ribPaint..strokeWidth = 1.5);
    }

    // Costuras de hombros
    final stitchPaint = Paint()
      ..color = darkColor.withValues(alpha: 0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0;

    canvas.drawLine(Offset(w * 0.37, h * 0.08), Offset(w * 0.18, h * 0.16), stitchPaint);
    canvas.drawLine(Offset(w * 0.63, h * 0.08), Offset(w * 0.82, h * 0.16), stitchPaint);
  }

  @override
  bool shouldRepaint(covariant RealisticGarmentPainter oldDelegate) {
    return oldDelegate.color != color || oldDelegate.tipoPrenda != tipoPrenda;
  }
}

// ==============================================================================
// PAINTER: SOBREPOSICIÓN DE SOMBRAS Y CUELLO CUANDO SE USA FOTO DE CATÁLOGO
// ==============================================================================
class RealisticGarmentOverlayPainter extends CustomPainter {
  final GarmentType tipoPrenda;
  final Color colorBase;

  RealisticGarmentOverlayPainter({required this.tipoPrenda, required this.colorBase});

  @override
  void paint(Canvas canvas, Size size) {
    final darkColor = _oscurecerColor(colorBase, 0.4);
    final lightColor = _aclararColor(colorBase, 0.3);

    final garmentPainter = RealisticGarmentPainter(color: colorBase, tipoPrenda: tipoPrenda);
    garmentPainter._dibujarPlieguesDeTela(canvas, size, darkColor);
    garmentPainter._dibujarCuelloYDetalles(canvas, size, colorBase, darkColor, lightColor);
  }

  @override
  bool shouldRepaint(covariant RealisticGarmentOverlayPainter oldDelegate) => false;
}

// ==============================================================================
// FUNCIÓN MATEMÁTICA: TRAZADO ANATÓMICO PRECISO DE LA PRENDA
// ==============================================================================
Path _crearPathPrenda(Size size, GarmentType tipo) {
  final w = size.width;
  final h = size.height;
  final path = Path();

  // Iniciar en el hombro izquierdo junto al cuello
  path.moveTo(w * 0.37, h * 0.08);

  // Hombro izquierdo hacia manga
  path.lineTo(w * 0.18, h * 0.16);

  // Manga izquierda (caída y basta de la manga)
  path.lineTo(w * 0.04, h * 0.32);
  path.lineTo(w * 0.16, h * 0.40);

  // Axila izquierda
  path.quadraticBezierTo(w * 0.22, h * 0.38, w * 0.24, h * 0.35);

  // Costado izquierdo del torso (curva de cintura suave)
  path.quadraticBezierTo(w * 0.23, h * 0.60, w * 0.22, h * 0.88);

  // Basta inferior (curvatura natural de la tela)
  path.quadraticBezierTo(w * 0.50, h * 0.92, w * 0.78, h * 0.88);

  // Costado derecho del torso
  path.quadraticBezierTo(w * 0.77, h * 0.60, w * 0.76, h * 0.35);

  // Axila derecha y manga derecha
  path.quadraticBezierTo(w * 0.78, h * 0.38, w * 0.84, h * 0.40);
  path.lineTo(w * 0.96, h * 0.32);
  path.lineTo(w * 0.82, h * 0.16);

  // Hombro derecho hacia el cuello
  path.lineTo(w * 0.63, h * 0.08);

  // Cuello según el tipo
  if (tipo == GarmentType.poleraCuelloV) {
    path.lineTo(w * 0.50, h * 0.21);
    path.lineTo(w * 0.37, h * 0.08);
  } else if (tipo == GarmentType.poleraPolo) {
    path.lineTo(w * 0.50, h * 0.14);
    path.lineTo(w * 0.37, h * 0.08);
  } else {
    // Cuello redondo tradicional
    path.quadraticBezierTo(w * 0.50, h * 0.16, w * 0.37, h * 0.08);
  }

  path.close();
  return path;
}

// Helpers de iluminación basados en HSL
Color _aclararColor(Color c, double factor) {
  final hsl = HSLColor.fromColor(c);
  final newLightness = (hsl.lightness + factor * (1.0 - hsl.lightness)).clamp(0.0, 1.0);
  return hsl.withLightness(newLightness).toColor();
}

Color _oscurecerColor(Color c, double factor) {
  final hsl = HSLColor.fromColor(c);
  final newLightness = (hsl.lightness * (1.0 - factor)).clamp(0.0, 1.0);
  return hsl.withLightness(newLightness).toColor();
}
