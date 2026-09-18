// ==============================================================================
// CU12 - UTILIZAR VESTIDOR VIRTUAL -> VISTA MÓVIL (MVC - VIEW EN FLUTTER)
// Ubicación: mobile-app/lib/views/virtual_fitting_room_view.dart
// ==============================================================================

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../models/product_model.dart';
import '../controllers/cart_controller.dart';
import 'cart_view.dart';

enum FittingMode { camaraVivo, fotoPersonal, maniqui }

class VirtualFittingRoomView extends StatefulWidget {
  final ProductModel producto;

  const VirtualFittingRoomView({super.key, required this.producto});

  @override
  State<VirtualFittingRoomView> createState() => _VirtualFittingRoomViewState();
}

class _VirtualFittingRoomViewState extends State<VirtualFittingRoomView> {
  FittingMode _modoActual = FittingMode.camaraVivo;
  File? _fotoUsuario;
  final ImagePicker _picker = ImagePicker();

  // Parámetros de transformación de la prenda
  Offset _prendaOffset = const Offset(0, 40);
  double _prendaEscala = 1.0;
  double _prendaOpacidad = 0.92;
  String _tallaSeleccionada = 'M';
  Color _colorSeleccionado = const Color(0xFF0F172A);

  // Selector de Maniquí
  final String _tipoCuerpo = 'Regular Fit';

  final List<String> _tallas = ['S', 'M', 'L', 'XL', 'XXL'];
  final List<Color> _paletaColores = [
    const Color(0xFF0F172A), // Negro clásico
    const Color(0xFFE2E8F0), // Blanco nieve
    const Color(0xFF1E3A8A), // Azul marino
    const Color(0xFFDC2626), // Rojo pasión
    const Color(0xFF475569), // Gris grafito
    const Color(0xFF15803D), // Verde oliva
  ];

  Future<void> _capturarOFoto(ImageSource source) async {
    try {
      final XFile? imagen = await _picker.pickImage(
        source: source,
        maxWidth: 1080,
        maxHeight: 1920,
        imageQuality: 85,
      );
      if (imagen != null) {
        setState(() {
          _fotoUsuario = File(imagen.path);
          _modoActual = FittingMode.fotoPersonal;
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('No se pudo acceder a la imagen: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final cartCtrl = Provider.of<CartController>(context, listen: false);

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: Text('🪞 Vestidor Virtual: ${widget.producto.nombre}', style: const TextStyle(fontSize: 16)),
        backgroundColor: const Color(0xFF1E293B),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Reiniciar Posición',
            onPressed: () {
              setState(() {
                _prendaOffset = const Offset(0, 40);
                _prendaEscala = 1.0;
              });
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Selector de Modo (Cámara en Vivo / Foto / Maniquí)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            color: const Color(0xFF1E293B),
            child: Row(
              children: [
                _buildTabButton(FittingMode.camaraVivo, Icons.videocam_outlined, 'En Tiempo Real'),
                const SizedBox(width: 8),
                _buildTabButton(FittingMode.fotoPersonal, Icons.camera_alt_outlined, 'Foto / Galería'),
                const SizedBox(width: 8),
                _buildTabButton(FittingMode.maniqui, Icons.accessibility_new, 'Maniquí 3D'),
              ],
            ),
          ),

          // Área de Visualización y Superposición AR
          Expanded(
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Fondo según el modo
                _buildFondoSegunModo(),

                // Prenda Arrastrable y Escalable (Overlay AR)
                Positioned(
                  left: MediaQuery.of(context).size.width / 2 - (110 * _prendaEscala) + _prendaOffset.dx,
                  top: MediaQuery.of(context).size.height / 4 - (110 * _prendaEscala) + _prendaOffset.dy,
                  child: GestureDetector(
                    onPanUpdate: (details) {
                      setState(() {
                        _prendaOffset += details.delta;
                      });
                    },
                    child: Opacity(
                      opacity: _prendaOpacidad,
                      child: Container(
                        width: 220 * _prendaEscala,
                        height: 250 * _prendaEscala,
                        decoration: BoxDecoration(
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withAlpha(50),
                              blurRadius: 15,
                              offset: const Offset(0, 8),
                            )
                          ],
                        ),
                        child: widget.producto.imagenUrl != null
                            ? Image.network(
                                widget.producto.imagenUrl!,
                                fit: BoxFit.contain,
                                errorBuilder: (_, __, ___) => _buildSiluetaPolera(),
                              )
                            : _buildSiluetaPolera(),
                      ),
                    ),
                  ),
                ),

                // Guía e Indicadores Superpuestos
                Positioned(
                  bottom: 12,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.black.withAlpha(160),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: Colors.white24),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.pan_tool_alt_outlined, size: 14, color: Colors.white70),
                        const SizedBox(width: 6),
                        Text(
                          'Arrastra con el dedo para encajar en hombros | Talla $_tallaSeleccionada',
                          style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Panel de Controles y Personalización Inferior
          Container(
            padding: const EdgeInsets.all(16),
            decoration: const BoxDecoration(
              color: Color(0xFF1E293B),
              borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
              boxShadow: [
                BoxShadow(color: Colors.black38, blurRadius: 10, offset: Offset(0, -3))
              ],
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Fila de Tallas
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'TALLA:',
                      style: TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    Row(
                      children: _tallas.map((t) {
                        final isSel = _tallaSeleccionada == t;
                        return GestureDetector(
                          onTap: () {
                            setState(() {
                              _tallaSeleccionada = t;
                              // Escala visual acorde a la talla
                              if (t == 'S') _prendaEscala = 0.9;
                              if (t == 'M') _prendaEscala = 1.0;
                              if (t == 'L') _prendaEscala = 1.1;
                              if (t == 'XL') _prendaEscala = 1.2;
                              if (t == 'XXL') _prendaEscala = 1.3;
                            });
                          },
                          child: Container(
                            margin: const EdgeInsets.symmetric(horizontal: 4),
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                            decoration: BoxDecoration(
                              color: isSel ? const Color(0xFFE11D48) : const Color(0xFF334155),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: isSel ? Colors.white : Colors.white12),
                            ),
                            child: Text(
                              t,
                              style: TextStyle(
                                color: isSel ? Colors.white : Colors.white70,
                                fontWeight: FontWeight.bold,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Fila de Colores
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'COLOR:',
                      style: TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    Row(
                      children: _paletaColores.map((c) {
                        final isSel = _colorSeleccionado == c;
                        return GestureDetector(
                          onTap: () => setState(() => _colorSeleccionado = c),
                          child: Container(
                            margin: const EdgeInsets.symmetric(horizontal: 4),
                            width: 26,
                            height: 26,
                            decoration: BoxDecoration(
                              color: c,
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: isSel ? const Color(0xFF38BDF8) : Colors.white24,
                                width: isSel ? 3 : 1,
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Control de Escala y Opacidad
                Row(
                  children: [
                    const Icon(Icons.opacity, size: 16, color: Colors.white70),
                    const SizedBox(width: 6),
                    Expanded(
                      child: SliderTheme(
                        data: SliderTheme.of(context).copyWith(
                          trackHeight: 3,
                          thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                        ),
                        child: Slider(
                          value: _prendaOpacidad,
                          min: 0.4,
                          max: 1.0,
                          activeColor: const Color(0xFF38BDF8),
                          onChanged: (v) => setState(() => _prendaOpacidad = v),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    const Icon(Icons.zoom_in, size: 16, color: Colors.white70),
                    const SizedBox(width: 6),
                    Expanded(
                      child: SliderTheme(
                        data: SliderTheme.of(context).copyWith(
                          trackHeight: 3,
                          thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                        ),
                        child: Slider(
                          value: _prendaEscala,
                          min: 0.7,
                          max: 1.5,
                          activeColor: const Color(0xFFE11D48),
                          onChanged: (v) => setState(() => _prendaEscala = v),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 14),

                // Botones de Acción: Agregar al Carrito
                SizedBox(
                  width: double.infinity,
                  height: 46,
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFE11D48),
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    icon: const Icon(Icons.shopping_bag),
                    label: Text(
                      '¡Me queda perfecto! Agregar Talla $_tallaSeleccionada (Bs. ${widget.producto.precio.toStringAsFixed(2)})',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                    ),
                    onPressed: () {
                      cartCtrl.agregarProducto(widget.producto);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('¡${widget.producto.nombre} (Talla $_tallaSeleccionada) agregada al carrito!'),
                          backgroundColor: Colors.green,
                          action: SnackBarAction(
                            label: 'Ver Carrito',
                            textColor: Colors.white,
                            onPressed: () {
                              Navigator.push(context, MaterialPageRoute(builder: (_) => const CartView()));
                            },
                          ),
                        ),
                      );
                      Navigator.pop(context);
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTabButton(FittingMode modo, IconData icon, String label) {
    final isSelected = _modoActual == modo;
    return Expanded(
      child: InkWell(
        onTap: () {
          if (modo == FittingMode.fotoPersonal && _fotoUsuario == null) {
            _mostrarOpcionesFoto();
          } else {
            setState(() => _modoActual = modo);
          }
        },
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFFE11D48) : const Color(0xFF334155),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 16, color: Colors.white),
              const SizedBox(width: 6),
              Text(
                label,
                style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _mostrarOpcionesFoto() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(16))),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Subir Foto para Vestidor Virtual', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
            const SizedBox(height: 16),
            ListTile(
              leading: const Icon(Icons.camera_alt, color: Color(0xFF38BDF8)),
              title: const Text('Tomar Selfie / Foto de Cuerpo Entero', style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(ctx);
                _capturarOFoto(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library, color: Color(0xFFE11D48)),
              title: const Text('Elegir de Galería', style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(ctx);
                _capturarOFoto(ImageSource.gallery);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFondoSegunModo() {
    if (_modoActual == FittingMode.fotoPersonal && _fotoUsuario != null) {
      return SizedBox.expand(
        child: Image.file(_fotoUsuario!, fit: BoxFit.cover),
      );
    }

    if (_modoActual == FittingMode.maniqui) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.accessibility_new, size: 280, color: Colors.white.withAlpha(50)),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(12)),
              child: Text(
                'Maniquí Unisex: $_tipoCuerpo',
                style: const TextStyle(color: Colors.white70, fontSize: 12),
              ),
            ),
          ],
        ),
      );
    }

    // Modo Cámara en Vivo (Live Camera Viewfinder Simulation)
    return Stack(
      children: [
        Container(
          color: const Color(0xFF0F172A),
          child: Center(
            child: Icon(Icons.person_outline, size: 300, color: Colors.white.withAlpha(20)),
          ),
        ),
        // Marco guía de encuadre AR
        Center(
          child: Container(
            width: 280,
            height: 380,
            decoration: BoxDecoration(
              border: Border.all(color: const Color(0xFF38BDF8).withAlpha(100), width: 1.5),
              borderRadius: BorderRadius.circular(24),
            ),
            child: const Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text(
                    'ENFOCA TUS HOMBROS Y PECHO AQUÍ',
                    style: TextStyle(color: Color(0xFF38BDF8), fontSize: 10, letterSpacing: 1),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.camera_front, size: 14, color: Colors.white60),
                      SizedBox(width: 4),
                      Text('Cámara Frontal Activa (AR Live Feed)', style: TextStyle(color: Colors.white60, fontSize: 10)),
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSiluetaPolera() {
    return Container(
      decoration: BoxDecoration(
        color: _colorSeleccionado,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white30, width: 1.5),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.checkroom, size: 60, color: Colors.white),
            const SizedBox(height: 6),
            Text(
              widget.producto.nombre,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }
}
