// ==============================================================================
// WIDGET: PRENDA REALISTA PARA VESTIDOR VIRTUAL AR (CU12)
// Ubicación: mobile-app/lib/widgets/realistic_garment_widget.dart
// Dibuja la silueta anatómica fluida de prendas (Polera, Cuello V, Polo, Hoodie)
// con sombreado volumétrico de tela, pliegues textiles y detalles de confección.
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
    this.mostrarEstampado = false,
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
                if (usarModoRecorteCompleto && imagenUrl != null && imagenUrl!.isNotEmpty)
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

                // 3. Emblema sutil bordado en pecho izquierdo (opcional y elegante)
                if (mostrarEstampado)
                  _buildBoutiqueEmblema(size),
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

  Widget _buildBoutiqueEmblema(Size size) {
    final logoSize = size.width * 0.10;
    return Positioned(
      top: size.height * 0.30,
      left: size.width * 0.30,
      width: logoSize,
      height: logoSize,
      child: Opacity(
        opacity: 0.65,
        child: Center(
          child: Icon(
            Icons.shield_outlined,
            size: logoSize * 0.85,
            color: Colors.white70,
          ),
        ),
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

    // 1. Capa de color base con gradiente de iluminación cenital suave
    final lightColor = _aclararColor(color, 0.20);
    final darkColor = _oscurecerColor(color, 0.28);

    final baseGradient = RadialGradient(
      center: const Alignment(0.0, -0.35),
      radius: 1.15,
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
      ..color = darkColor.withValues(alpha: 0.35)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.2;
    canvas.drawPath(garmentPath, borderPaint);
  }

  void _dibujarPlieguesDeTela(Canvas canvas, Size size, Color shadowColor) {
    final w = size.width;
    final h = size.height;

    final shadowPaint = Paint()
      ..color = shadowColor.withValues(alpha: 0.30)
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 2.0
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 2.5);

    // Pliegue axila izquierda
    final pLeft = Path()
      ..moveTo(w * 0.24, h * 0.38)
      ..quadraticBezierTo(w * 0.31, h * 0.46, w * 0.35, h * 0.54);
    canvas.drawPath(pLeft, shadowPaint);

    // Pliegue axila derecha
    final pRight = Path()
      ..moveTo(w * 0.76, h * 0.38)
      ..quadraticBezierTo(w * 0.69, h * 0.46, w * 0.65, h * 0.54);
    canvas.drawPath(pRight, shadowPaint);

    // Pliegues suaves de torso (cintura)
    final pWaistLeft = Path()
      ..moveTo(w * 0.26, h * 0.68)
      ..quadraticBezierTo(w * 0.36, h * 0.71, w * 0.42, h * 0.70);
    canvas.drawPath(pWaistLeft, shadowPaint);

    final pWaistRight = Path()
      ..moveTo(w * 0.74, h * 0.70)
      ..quadraticBezierTo(w * 0.64, h * 0.72, w * 0.58, h * 0.71);
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
      ..color = darkColor.withValues(alpha: 0.70)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0;

    final innerNeckPaint = Paint()
      ..color = _oscurecerColor(darkColor, 0.45)
      ..style = PaintingStyle.fill;

    if (tipoPrenda == GarmentType.poleraCuelloRedondo) {
      // Interior del cuello (vista interna de la espalda)
      final backNeckPath = Path()
        ..moveTo(w * 0.36, h * 0.10)
        ..quadraticBezierTo(w * 0.50, h * 0.05, w * 0.64, h * 0.10)
        ..quadraticBezierTo(w * 0.50, h * 0.15, w * 0.36, h * 0.10);
      canvas.drawPath(backNeckPath, innerNeckPaint);

      // Ribete frontal del cuello
      final ribPath = Path()
        ..moveTo(w * 0.36, h * 0.10)
        ..quadraticBezierTo(w * 0.50, h * 0.18, w * 0.64, h * 0.10);
      canvas.drawPath(ribPath, ribPaint);
    } else if (tipoPrenda == GarmentType.poleraCuelloV) {
      // Interior del cuello en V
      final backNeckPath = Path()
        ..moveTo(w * 0.36, h * 0.10)
        ..quadraticBezierTo(w * 0.50, h * 0.05, w * 0.64, h * 0.10)
        ..lineTo(w * 0.50, h * 0.20)
        ..close();
      canvas.drawPath(backNeckPath, innerNeckPaint);

      // Cuello en V ribeteado
      final vNeck = Path()
        ..moveTo(w * 0.36, h * 0.10)
        ..lineTo(w * 0.50, h * 0.24)
        ..lineTo(w * 0.64, h * 0.10);
      canvas.drawPath(vNeck, ribPaint);
    } else if (tipoPrenda == GarmentType.poleraPolo) {
      // Cuello Polo Elegante con solapa y tapeta
      final innerPolo = Path()
        ..moveTo(w * 0.36, h * 0.10)
        ..quadraticBezierTo(w * 0.50, h * 0.06, w * 0.64, h * 0.10)
        ..quadraticBezierTo(w * 0.50, h * 0.14, w * 0.36, h * 0.10);
      canvas.drawPath(innerPolo, innerNeckPaint);

      // Solapa izquierda del cuello polo
      final lapelLeft = Path()
        ..moveTo(w * 0.34, h * 0.09)
        ..lineTo(w * 0.43, h * 0.19)
        ..lineTo(w * 0.49, h * 0.15)
        ..lineTo(w * 0.40, h * 0.07)
        ..close();
      final collarFill = Paint()..color = _aclararColor(baseColor, 0.12);
      canvas.drawPath(lapelLeft, collarFill);
      canvas.drawPath(lapelLeft, ribPaint..strokeWidth = 1.5);

      // Solapa derecha del cuello polo
      final lapelRight = Path()
        ..moveTo(w * 0.66, h * 0.09)
        ..lineTo(w * 0.57, h * 0.19)
        ..lineTo(w * 0.51, h * 0.15)
        ..lineTo(w * 0.60, h * 0.07)
        ..close();
      canvas.drawPath(lapelRight, collarFill);
      canvas.drawPath(lapelRight, ribPaint..strokeWidth = 1.5);

      // Tapeta central
      final placket = Rect.fromCenter(
        center: Offset(w * 0.50, h * 0.24),
        width: w * 0.065,
        height: h * 0.14,
      );
      canvas.drawRect(placket, Paint()..color = darkColor.withValues(alpha: 0.45));
      canvas.drawRect(placket, ribPaint..strokeWidth = 1.2);

      // 2 Botones nacarados
      final buttonPaint = Paint()..color = Colors.white.withValues(alpha: 0.85);
      canvas.drawCircle(Offset(w * 0.50, h * 0.20), 3.2, buttonPaint);
      canvas.drawCircle(Offset(w * 0.50, h * 0.26), 3.2, buttonPaint);
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

    // Costuras suaves de hombros
    final stitchPaint = Paint()
      ..color = darkColor.withValues(alpha: 0.35)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0;

    canvas.drawLine(Offset(w * 0.36, h * 0.10), Offset(w * 0.18, h * 0.17), stitchPaint);
    canvas.drawLine(Offset(w * 0.64, h * 0.10), Offset(w * 0.82, h * 0.17), stitchPaint);
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

  // Iniciar en la base del cuello izquierdo
  path.moveTo(w * 0.36, h * 0.10);

  // Caída de hombro izquierdo (curva natural ligeramente convexa)
  path.quadraticBezierTo(w * 0.26, h * 0.12, w * 0.18, h * 0.17);

  // Manga izquierda: curvatura del hombro exterior
  path.quadraticBezierTo(w * 0.10, h * 0.23, w * 0.07, h * 0.34);

  // Basta de la manga izquierda (borde curvo del puño)
  path.quadraticBezierTo(w * 0.12, h * 0.39, w * 0.18, h * 0.39);

  // Axila izquierda (hueco redondeado anatómico)
  path.quadraticBezierTo(w * 0.22, h * 0.38, w * 0.23, h * 0.35);

  // Lateral izquierdo del torso (caída anatómica con cintura suave)
  path.cubicTo(w * 0.24, h * 0.52, w * 0.23, h * 0.72, w * 0.22, h * 0.88);

  // Basta inferior (borde inferior con curvatura textil natural)
  path.quadraticBezierTo(w * 0.50, h * 0.93, w * 0.78, h * 0.88);

  // Lateral derecho del torso
  path.cubicTo(w * 0.77, h * 0.72, w * 0.76, h * 0.52, w * 0.77, h * 0.35);

  // Axila derecha
  path.quadraticBezierTo(w * 0.78, h * 0.38, w * 0.82, h * 0.39);

  // Basta de manga derecha
  path.quadraticBezierTo(w * 0.88, h * 0.39, w * 0.93, h * 0.34);

  // Manga derecha (curvatura del hombro exterior)
  path.quadraticBezierTo(w * 0.90, h * 0.23, w * 0.82, h * 0.17);

  // Caída de hombro derecho
  path.quadraticBezierTo(w * 0.74, h * 0.12, w * 0.64, h * 0.10);

  // Línea de cuello según el tipo de prenda
  if (tipo == GarmentType.poleraCuelloV) {
    path.lineTo(w * 0.50, h * 0.24);
    path.lineTo(w * 0.36, h * 0.10);
  } else if (tipo == GarmentType.poleraPolo) {
    path.quadraticBezierTo(w * 0.50, h * 0.14, w * 0.36, h * 0.10);
  } else {
    // Cuello Redondo anatómico
    path.quadraticBezierTo(w * 0.50, h * 0.18, w * 0.36, h * 0.10);
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
