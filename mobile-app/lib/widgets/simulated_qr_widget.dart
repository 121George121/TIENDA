// ==============================================================================
// COMPONENTE VISUAL - CÓDIGO QR SIMULADO DE ALTA FIDELIDAD
// Renderiza códigos QR nítidos, auténticos y deterministas para pagos y recibos fiscales
// Ubicación: mobile-app/lib/widgets/simulated_qr_widget.dart
// ==============================================================================

import 'package:flutter/material.dart';

class SimulatedQrWidget extends StatelessWidget {
  final String data;
  final double size;
  final Color foregroundColor;
  final Color backgroundColor;
  final Widget? centerIcon;

  const SimulatedQrWidget({
    super.key,
    required this.data,
    this.size = 180,
    this.foregroundColor = const Color(0xFF0F172A),
    this.backgroundColor = Colors.white,
    this.centerIcon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      padding: EdgeInsets.all(size * 0.05),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withAlpha(20),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(color: Colors.grey.shade300, width: 1),
      ),
      child: Stack(
        alignment: Alignment.center,
        children: [
          CustomPaint(
            size: Size(size * 0.9, size * 0.9),
            painter: _QrPainter(
              data: data,
              color: foregroundColor,
            ),
          ),
          if (centerIcon != null)
            Container(
              padding: const EdgeInsets.all(4),
              decoration: BoxDecoration(
                color: backgroundColor,
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: foregroundColor.withAlpha(80), width: 1.5),
              ),
              child: centerIcon,
            ),
        ],
      ),
    );
  }
}

class _QrPainter extends CustomPainter {
  final String data;
  final Color color;

  _QrPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    const int gridSize = 25; // Matriz 25x25 estándar QR Versión 2
    final double cellSize = size.width / gridSize;

    // Generar matriz booleana determinista basada en el contenido
    final matrix = List.generate(gridSize, (_) => List.filled(gridSize, false));

    // 1. Patrones de Detección de Posición (Finder Patterns) en las 3 esquinas (7x7)
    _drawFinderPattern(matrix, 0, 0);
    _drawFinderPattern(matrix, gridSize - 7, 0);
    _drawFinderPattern(matrix, 0, gridSize - 7);

    // 2. Líneas de sincronización (Timing Patterns)
    for (int i = 8; i < gridSize - 8; i++) {
      if (i % 2 == 0) {
        matrix[6][i] = true;
        matrix[i][6] = true;
      }
    }

    // 3. Patrón de alineación en versión estándar (alrededor de x:18, y:18)
    _drawAlignmentPattern(matrix, gridSize - 9, gridSize - 9);

    // 4. Llenar los módulos de datos determinísticamente a partir del hash de `data`
    int hash = 5381;
    for (int i = 0; i < data.length; i++) {
      hash = ((hash << 5) + hash) + data.codeUnitAt(i);
    }

    int seed = hash.abs();
    for (int r = 0; r < gridSize; r++) {
      for (int c = 0; c < gridSize; c++) {
        // Respetar las zonas reservadas de los 3 finders
        if ((r < 8 && c < 8) ||
            (r < 8 && c >= gridSize - 8) ||
            (r >= gridSize - 8 && c < 8)) {
          continue;
        }
        // Respetar sincronización
        if (r == 6 || c == 6) continue;
        // Respetar el centro (evitar bloquear el icono central si existe)
        if (r >= 10 && r <= 14 && c >= 10 && c <= 14) continue;

        // Algoritmo pseudo-aleatorio LCG congruente lineal
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF;
        matrix[r][c] = (seed % 100) < 48; // Densidad aprox 48%
      }
    }

    // Dibujar todos los módulos activos con esquinas ligeramente redondeadas
    final rrectRadius = Radius.circular(cellSize * 0.25);
    for (int r = 0; r < gridSize; r++) {
      for (int c = 0; c < gridSize; c++) {
        if (matrix[r][c]) {
          final rect = Rect.fromLTWH(
            c * cellSize,
            r * cellSize,
            cellSize * 0.94,
            cellSize * 0.94,
          );
          canvas.drawRRect(RRect.fromRectAndRadius(rect, rrectRadius), paint);
        }
      }
    }
  }

  void _drawFinderPattern(List<List<bool>> matrix, int startRow, int startCol) {
    for (int r = 0; r < 7; r++) {
      for (int c = 0; c < 7; c++) {
        if (r == 0 || r == 6 || c == 0 || c == 6) {
          matrix[startRow + r][startCol + c] = true;
        } else if (r >= 2 && r <= 4 && c >= 2 && c <= 4) {
          matrix[startRow + r][startCol + c] = true;
        } else {
          matrix[startRow + r][startCol + c] = false;
        }
      }
    }
  }

  void _drawAlignmentPattern(List<List<bool>> matrix, int centerRow, int centerCol) {
    for (int r = -2; r <= 2; r++) {
      for (int c = -2; c <= 2; c++) {
        if (r == -2 || r == 2 || c == -2 || c == 2 || (r == 0 && c == 0)) {
          matrix[centerRow + r][centerCol + c] = true;
        } else {
          matrix[centerRow + r][centerCol + c] = false;
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant _QrPainter oldDelegate) {
    return oldDelegate.data != data || oldDelegate.color != color;
  }
}
