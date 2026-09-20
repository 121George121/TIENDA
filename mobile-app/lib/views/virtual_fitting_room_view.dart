// ==============================================================================
// CU12 - UTILIZAR VESTIDOR VIRTUAL -> VISTA MÓVIL PROFESIONAL AR
// Ubicación: mobile-app/lib/views/virtual_fitting_room_view.dart
// Características:
// 1. Cámara en tiempo real (Live AR Mirror) a 30/60 FPS con cámara frontal/trasera.
// 2. Prenda 3D realista con iluminación de tela, pliegues y estampado del producto.
// 3. Gestos multitáctiles completos (Arrastre 2D, Pinch-to-zoom y Rotación suave).
// 4. Guía de calibración anatómica de hombros y torso.
// 5. Paleta de colores textiles que NO tapan la textura de la tela.
// 6. Selector de Tallas (S-XXL) y Tipos de Prenda (Cuello redondo, Cuello V, Polo, Hoodie).
// ==============================================================================

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../models/product_model.dart';
import '../controllers/cart_controller.dart';
import '../widgets/realistic_garment_widget.dart';
import '../widgets/ar_body_guide_overlay.dart';
import 'cart_view.dart';

enum FittingMode { camaraVivo, fotoPersonal, maniqui }

class VirtualFittingRoomView extends StatefulWidget {
  final ProductModel producto;

  const VirtualFittingRoomView({super.key, required this.producto});

  @override
  State<VirtualFittingRoomView> createState() => _VirtualFittingRoomViewState();
}

class _VirtualFittingRoomViewState extends State<VirtualFittingRoomView> with WidgetsBindingObserver {
  // Estado del Modo de Visualización
  FittingMode _modoActual = FittingMode.camaraVivo;
  File? _fotoUsuario;
  final ImagePicker _picker = ImagePicker();

  // Controlador de Cámara en Tiempo Real
  List<CameraDescription> _camarasDisponibles = [];
  CameraController? _cameraController;
  bool _camaraIniciando = false;
  bool _camaraLista = false;
  String? _errorCamara;
  int _camaraSeleccionadaIndex = 0;

  // Parámetros de Transformación AR de la Prenda
  Offset _prendaOffset = const Offset(0, 30);
  double _prendaEscala = 1.0;
  double _prendaRotacion = 0.0;
  double _prendaOpacidad = 0.95;

  // Variables para gestos multitáctiles
  Offset _baseFocalPoint = Offset.zero;
  Offset _baseOffset = Offset.zero;
  double _baseScale = 1.0;
  double _baseRotation = 0.0;

  // Personalización de la Prenda
  String _tallaSeleccionada = 'M';
  Color _colorSeleccionado = const Color(0xFF1E293B); // Charcoal / Grafito elegante
  GarmentType _tipoPrenda = GarmentType.poleraCuelloRedondo;
  bool _usarRecorteFotoCatalogo = false;
  bool _mostrarGuiaCalibracion = true;
  final bool _mostrarControlesFlotantes = true;

  // Lista de Tallas con medidas sugeridas
  final Map<String, String> _tallasInfo = {
    'S': 'Pecho: 88-92 cm',
    'M': 'Pecho: 96-102 cm',
    'L': 'Pecho: 104-108 cm',
    'XL': 'Pecho: 110-116 cm',
    'XXL': 'Pecho: 118-124 cm',
  };

  // Paleta de Colores de Telas Realistas (con nombres comerciales)
  final List<Map<String, dynamic>> _coloresDisponibles = [
    {'nombre': 'Grafito', 'color': const Color(0xFF1E293B)},
    {'nombre': 'Blanco Nieve', 'color': const Color(0xFFF1F5F9)},
    {'nombre': 'Azul Marino', 'color': const Color(0xFF1E3A8A)},
    {'nombre': 'Rojo Pasión', 'color': const Color(0xFFDC2626)},
    {'nombre': 'Verde Militar', 'color': const Color(0xFF365314)},
    {'nombre': 'Borgoña', 'color': const Color(0xFF831843)},
    {'nombre': 'Negro Jet', 'color': const Color(0xFF090D16)},
    {'nombre': 'Amarillo Ocre', 'color': const Color(0xFFD97706)},
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _inicializarCamara();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (_cameraController == null || !_cameraController!.value.isInitialized) return;

    if (state == AppLifecycleState.inactive) {
      _cameraController?.dispose();
    } else if (state == AppLifecycleState.resumed) {
      _inicializarCamara();
    }
  }

  /// Inicializa la cámara física del teléfono dando prioridad a la cámara frontal (Modo Espejo)
  Future<void> _inicializarCamara() async {
    setState(() {
      _camaraIniciando = true;
      _errorCamara = null;
    });

    try {
      _camarasDisponibles = await availableCameras();

      if (_camarasDisponibles.isEmpty) {
        setState(() {
          _errorCamara = 'No se detectaron cámaras en este dispositivo.';
          _camaraIniciando = false;
          _modoActual = FittingMode.maniqui;
        });
        return;
      }

      // Buscar cámara frontal (selfie)
      int targetIndex = _camarasDisponibles.indexWhere(
        (cam) => cam.lensDirection == CameraLensDirection.front,
      );

      if (targetIndex == -1) targetIndex = 0; // Fallback a trasera si no hay frontal
      _camaraSeleccionadaIndex = targetIndex;

      await _configurarControladorCamara(_camarasDisponibles[targetIndex]);
    } catch (e) {
      setState(() {
        _errorCamara = 'Permiso de cámara denegado o no disponible: $e';
        _camaraIniciando = false;
        _modoActual = FittingMode.maniqui;
      });
    }
  }

  Future<void> _configurarControladorCamara(CameraDescription cameraDescription) async {
    final prevController = _cameraController;
    if (prevController != null) {
      await prevController.dispose();
    }

    final newController = CameraController(
      cameraDescription,
      ResolutionPreset.high,
      enableAudio: false,
    );

    try {
      await newController.initialize();
      if (!mounted) return;

      setState(() {
        _cameraController = newController;
        _camaraLista = true;
        _camaraIniciando = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorCamara = 'Error al iniciar la cámara: $e';
        _camaraIniciando = false;
        _modoActual = FittingMode.maniqui;
      });
    }
  }

  /// Alterna entre la cámara frontal y la trasera
  Future<void> _cambiarCamara() async {
    if (_camarasDisponibles.length < 2) return;

    final nextIndex = (_camaraSeleccionadaIndex + 1) % _camarasDisponibles.length;
    _camaraSeleccionadaIndex = nextIndex;
    await _configurarControladorCamara(_camarasDisponibles[nextIndex]);
  }

  /// Captura de foto desde cámara o galería
  Future<void> _seleccionarFotoPersonal(ImageSource source) async {
    try {
      final XFile? imagen = await _picker.pickImage(
        source: source,
        maxWidth: 1440,
        maxHeight: 2560,
        imageQuality: 90,
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
          SnackBar(content: Text('No se pudo cargar la imagen: $e')),
        );
      }
    }
  }

  /// Restablece la posición y orientación de la prenda
  void _resetearPosicionPrenda() {
    setState(() {
      _prendaOffset = const Offset(0, 30);
      _prendaRotacion = 0.0;
      _aplicarEscalaPorTalla(_tallaSeleccionada);
    });
  }

  void _aplicarEscalaPorTalla(String talla) {
    _tallaSeleccionada = talla;
    if (talla == 'S') _prendaEscala = 0.88;
    if (talla == 'M') _prendaEscala = 1.00;
    if (talla == 'L') _prendaEscala = 1.12;
    if (talla == 'XL') _prendaEscala = 1.24;
    if (talla == 'XXL') _prendaEscala = 1.36;
  }

  @override
  Widget build(BuildContext context) {
    final cartCtrl = Provider.of<CartController>(context, listen: false);

    return Scaffold(
      backgroundColor: const Color(0xFF0B0F19),
      body: SafeArea(
        child: Column(
          children: [
            // Barra Superior Personalizada (Glassmorphic Top Bar)
            _buildTopBar(),

            // Selector de Modos (Cámara en Vivo, Foto, Maniquí)
            _buildModeSelector(),

            // Área Principal de Visualización AR
            Expanded(
              child: Stack(
                fit: StackFit.expand,
                children: [
                  // 1. Capa de Fondo (Cámara en tiempo real, Foto personal o Maniquí)
                  _buildFondoAR(),

                  // 2. Guía de Posicionamiento Corporal
                  ArBodyGuideOverlay(visible: _mostrarGuiaCalibracion),

                  // 3. Prenda AR Interactiva con Gestos Multitáctiles
                  _buildPrendaInteractiva(),

                  // 4. Controles Flotantes Rápidos (Subir, Bajar, Zoom, Centrar)
                  if (_mostrarControlesFlotantes)
                    Positioned(
                      right: 12,
                      top: 16,
                      child: _buildPanelControlesRapidos(),
                    ),

                  // 5. Botón de alternar cámara (si está en modo cámara)
                  if (_modoActual == FittingMode.camaraVivo && _camaraLista)
                    Positioned(
                      left: 14,
                      top: 16,
                      child: FloatingActionButton.small(
                        heroTag: 'switch_cam',
                        backgroundColor: Colors.black.withValues(alpha: 0.65),
                        foregroundColor: Colors.white,
                        onPressed: _cambiarCamara,
                        tooltip: 'Cambiar a Cámara Frontal/Trasera',
                        child: const Icon(Icons.flip_camera_ios, size: 20),
                      ),
                    ),

                  // 6. Indicador de gesto en la parte inferior del visor
                  Positioned(
                    bottom: 8,
                    left: 20,
                    right: 20,
                    child: Center(
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
                        decoration: BoxDecoration(
                          color: Colors.black.withValues(alpha: 0.7),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: Colors.white24),
                        ),
                        child: Text(
                          'Usa 2 dedos para pellizcar (zoom) y rotar | 1 dedo para mover',
                          style: TextStyle(
                            color: Colors.white.withValues(alpha: 0.9),
                            fontSize: 10.5,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Panel Inferior de Ajustes de Prenda (Tallas, Colores, Estilos y Carrito)
            _buildPanelAjustesInferior(cartCtrl),
          ],
        ),
      ),
    );
  }

  // ============================================================================
  // TOP BAR
  // ============================================================================
  Widget _buildTopBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
      decoration: const BoxDecoration(
        color: Color(0xFF111827),
        border: Border(bottom: BorderSide(color: Color(0xFF1F2937))),
      ),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new, color: Colors.white, size: 20),
            onPressed: () => Navigator.pop(context),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Text('🪞 ', style: TextStyle(fontSize: 16)),
                    Expanded(
                      child: Text(
                        widget.producto.nombre,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ),
                  ],
                ),
                Text(
                  '${_tallasInfo[_tallaSeleccionada]} • Bs. ${widget.producto.precio.toStringAsFixed(2)}',
                  style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 11),
                ),
              ],
            ),
          ),
          IconButton(
            icon: Icon(
              _mostrarGuiaCalibracion ? Icons.accessibility : Icons.accessibility_new_outlined,
              color: _mostrarGuiaCalibracion ? const Color(0xFF38BDF8) : Colors.white60,
              size: 22,
            ),
            tooltip: 'Guía de Hombros',
            onPressed: () => setState(() => _mostrarGuiaCalibracion = !_mostrarGuiaCalibracion),
          ),
          IconButton(
            icon: const Icon(Icons.restart_alt, color: Colors.white, size: 22),
            tooltip: 'Resetear Prenda',
            onPressed: _resetearPosicionPrenda,
          ),
        ],
      ),
    );
  }

  // ============================================================================
  // SELECTOR DE MODO (TIEMPO REAL / FOTO / MANIQUÍ)
  // ============================================================================
  Widget _buildModeSelector() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      color: const Color(0xFF0F172A),
      child: Row(
        children: [
          _buildModeTab(
            FittingMode.camaraVivo,
            Icons.videocam,
            'En Tiempo Real',
            onTap: () {
              setState(() => _modoActual = FittingMode.camaraVivo);
              if (!_camaraLista && !_camaraIniciando) _inicializarCamara();
            },
          ),
          const SizedBox(width: 6),
          _buildModeTab(
            FittingMode.fotoPersonal,
            Icons.photo_camera_back,
            'Mi Foto / Galería',
            onTap: () {
              if (_fotoUsuario == null) {
                _mostrarBottomSheetFoto();
              } else {
                setState(() => _modoActual = FittingMode.fotoPersonal);
              }
            },
          ),
          const SizedBox(width: 6),
          _buildModeTab(
            FittingMode.maniqui,
            Icons.boy_outlined,
            'Maniquí 3D',
            onTap: () => setState(() => _modoActual = FittingMode.maniqui),
          ),
        ],
      ),
    );
  }

  Widget _buildModeTab(FittingMode modo, IconData icon, String label, {required VoidCallback onTap}) {
    final isSelected = _modoActual == modo;
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: const EdgeInsets.symmetric(vertical: 7),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFF6366F1) : const Color(0xFF1E293B),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: isSelected ? const Color(0xFF818CF8) : Colors.white12,
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 15, color: isSelected ? Colors.white : Colors.white70),
              const SizedBox(width: 5),
              Flexible(
                child: Text(
                  label,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    color: isSelected ? Colors.white : Colors.white70,
                    fontSize: 11,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ============================================================================
  // CAPA DE FONDO SEGÚN EL MODO
  // ============================================================================
  Widget _buildFondoAR() {
    if (_modoActual == FittingMode.camaraVivo) {
      if (_camaraIniciando) {
        return Container(
          color: Colors.black,
          child: const Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                CircularProgressIndicator(color: Color(0xFF6366F1)),
                SizedBox(height: 12),
                Text('Iniciando Espejo en Tiempo Real...', style: TextStyle(color: Colors.white70, fontSize: 13)),
              ],
            ),
          ),
        );
      }

      if (_errorCamara != null || !_camaraLista || _cameraController == null) {
        return Container(
          color: const Color(0xFF0F172A),
          padding: const EdgeInsets.all(24),
          child: Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.videocam_off, size: 48, color: Colors.amber),
                const SizedBox(height: 12),
                Text(
                  _errorCamara ?? 'Cámara no disponible',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white, fontSize: 13),
                ),
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF6366F1)),
                  icon: const Icon(Icons.refresh),
                  label: const Text('Reintentar Cámara'),
                  onPressed: _inicializarCamara,
                ),
                const SizedBox(height: 8),
                TextButton(
                  onPressed: () => _mostrarBottomSheetFoto(),
                  child: const Text('Subir Foto Personal en su lugar', style: TextStyle(color: Color(0xFF38BDF8))),
                )
              ],
            ),
          ),
        );
      }

      // Cámara en vivo con espejo (mirror) para cámara frontal
      final isFront = _camarasDisponibles.isNotEmpty &&
          _camarasDisponibles[_camaraSeleccionadaIndex].lensDirection == CameraLensDirection.front;

      return ClipRect(
        child: Transform(
          alignment: Alignment.center,
          transform: isFront ? Matrix4.rotationY(3.14159) : Matrix4.identity(),
          child: FittedBox(
            fit: BoxFit.cover,
            child: SizedBox(
              width: _cameraController!.value.previewSize?.height ?? 1080,
              height: _cameraController!.value.previewSize?.width ?? 1920,
              child: CameraPreview(_cameraController!),
            ),
          ),
        ),
      );
    }

    if (_modoActual == FittingMode.fotoPersonal && _fotoUsuario != null) {
      return SizedBox.expand(
        child: Image.file(_fotoUsuario!, fit: BoxFit.cover),
      );
    }

    // Modo Maniquí 3D Profesional
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFF0F172A), Color(0xFF1E1B4B)],
        ),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withValues(alpha: 0.04),
                border: Border.all(color: Colors.white10),
              ),
              child: Icon(Icons.person, size: 220, color: Colors.white.withValues(alpha: 0.22)),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
              decoration: BoxDecoration(
                color: Colors.white12,
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Text(
                'Maniquí Unisex: Complexión Regular',
                style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ============================================================================
  // PRENDA AR INTERACTIVA CON GESTOS COMPLETOS
  // ============================================================================
  Widget _buildPrendaInteractiva() {
    final screenSize = MediaQuery.of(context).size;
    final garmentBaseWidth = screenSize.width * 0.72;

    return Positioned(
      left: (screenSize.width / 2) - (garmentBaseWidth / 2) + _prendaOffset.dx,
      top: (screenSize.height * 0.22) + _prendaOffset.dy,
      width: garmentBaseWidth,
      child: GestureDetector(
        onScaleStart: (details) {
          _baseFocalPoint = details.focalPoint;
          _baseOffset = _prendaOffset;
          _baseScale = _prendaEscala;
          _baseRotation = _prendaRotacion;
        },
        onScaleUpdate: (details) {
          setState(() {
            // Arrastre 2D
            _prendaOffset = _baseOffset + (details.focalPoint - _baseFocalPoint);

            // Zoom / Escala con 2 dedos (limite 0.6x a 2.4x)
            _prendaEscala = (_baseScale * details.scale).clamp(0.6, 2.4);

            // Rotación suave con 2 dedos
            _prendaRotacion = _baseRotation + details.rotation;
          });
        },
        child: Transform(
          alignment: Alignment.center,
          transform: Matrix4.diagonal3Values(_prendaEscala, _prendaEscala, 1.0)
            ..rotateZ(_prendaRotacion),
          child: RealisticGarmentWidget(
            color: _colorSeleccionado,
            nombreProducto: widget.producto.nombre,
            imagenUrl: widget.producto.imagenUrl,
            tipoPrenda: _tipoPrenda,
            opacidad: _prendaOpacidad,
            mostrarEstampado: true,
            usarModoRecorteCompleto: _usarRecorteFotoCatalogo,
          ),
        ),
      ),
    );
  }

  // ============================================================================
  // PANEL DE CONTROLES RÁPIDOS EN PANTALLA (D-PAD)
  // ============================================================================
  Widget _buildPanelControlesRapidos() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.black.withValues(alpha: 0.65),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white24),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildQuickActionBtn(Icons.arrow_upward, 'Subir', () {
            setState(() => _prendaOffset += const Offset(0, -12));
          }),
          const SizedBox(height: 6),
          _buildQuickActionBtn(Icons.arrow_downward, 'Bajar', () {
            setState(() => _prendaOffset += const Offset(0, 12));
          }),
          const Divider(color: Colors.white24, height: 12),
          _buildQuickActionBtn(Icons.zoom_in, 'Agrandar', () {
            setState(() => _prendaEscala = (_prendaEscala + 0.06).clamp(0.6, 2.4));
          }),
          const SizedBox(height: 6),
          _buildQuickActionBtn(Icons.zoom_out, 'Achicar', () {
            setState(() => _prendaEscala = (_prendaEscala - 0.06).clamp(0.6, 2.4));
          }),
          const Divider(color: Colors.white24, height: 12),
          _buildQuickActionBtn(Icons.center_focus_strong, 'Centrar', _resetearPosicionPrenda),
        ],
      ),
    );
  }

  Widget _buildQuickActionBtn(IconData icon, String tooltip, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.all(6),
        child: Icon(icon, size: 18, color: Colors.white),
      ),
    );
  }

  // ============================================================================
  // PANEL INFERIOR DE AJUSTES (TALLAS, COLORES, TELAS Y COMPRA)
  // ============================================================================
  Widget _buildPanelAjustesInferior(CartController cartCtrl) {
    return Container(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
      decoration: const BoxDecoration(
        color: Color(0xFF111827),
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        border: Border(top: BorderSide(color: Color(0xFF1F2937))),
        boxShadow: [
          BoxShadow(color: Colors.black54, blurRadius: 16, offset: Offset(0, -4)),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // 1. Selector de Tipo de Prenda
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: [
                _buildTipoPrendaChip('Cuello Redondo', GarmentType.poleraCuelloRedondo),
                const SizedBox(width: 8),
                _buildTipoPrendaChip('Cuello en V', GarmentType.poleraCuelloV),
                const SizedBox(width: 8),
                _buildTipoPrendaChip('Polo', GarmentType.poleraPolo),
                const SizedBox(width: 8),
                _buildTipoPrendaChip('Hoodie', GarmentType.hoodie),
              ],
            ),
          ),
          const SizedBox(height: 10),

          // 2. Selector de Talla con Medidas
          Row(
            children: [
              const Text(
                'TALLA:',
                style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.bold),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: _tallasInfo.keys.map((talla) {
                    final isSel = _tallaSeleccionada == talla;
                    return GestureDetector(
                      onTap: () => setState(() => _aplicarEscalaPorTalla(talla)),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: isSel ? const Color(0xFF6366F1) : const Color(0xFF1F2937),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(
                            color: isSel ? const Color(0xFF818CF8) : Colors.white10,
                            width: isSel ? 1.5 : 1.0,
                          ),
                        ),
                        child: Text(
                          talla,
                          style: TextStyle(
                            color: isSel ? Colors.white : Colors.white70,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),

          // 3. Paleta de Colores Textiles con Iluminación Natural
          Row(
            children: [
              const Text(
                'COLOR:',
                style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.bold),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: SizedBox(
                  height: 32,
                  child: ListView.separated(
                    scrollDirection: Axis.horizontal,
                    itemCount: _coloresDisponibles.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 8),
                    itemBuilder: (ctx, i) {
                      final item = _coloresDisponibles[i];
                      final Color c = item['color'];
                      final isSel = _colorSeleccionado == c;

                      return GestureDetector(
                        onTap: () => setState(() => _colorSeleccionado = c),
                        child: Container(
                          width: 30,
                          height: 30,
                          decoration: BoxDecoration(
                            color: c,
                            shape: BoxShape.circle,
                            border: Border.all(
                              color: isSel ? const Color(0xFF38BDF8) : Colors.white30,
                              width: isSel ? 3 : 1,
                            ),
                            boxShadow: [
                              if (isSel)
                                BoxShadow(
                                  color: const Color(0xFF38BDF8).withValues(alpha: 0.5),
                                  blurRadius: 8,
                                ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),

          // 4. Control de Opacidad / Transparencia de la tela
          Row(
            children: [
              const Icon(Icons.opacity, size: 16, color: Colors.white60),
              const SizedBox(width: 6),
              const Text('Fusión:', style: TextStyle(color: Colors.white60, fontSize: 11)),
              Expanded(
                child: SliderTheme(
                  data: SliderTheme.of(context).copyWith(
                    trackHeight: 2,
                    thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                    activeTrackColor: const Color(0xFF6366F1),
                    thumbColor: const Color(0xFF818CF8),
                  ),
                  child: Slider(
                    value: _prendaOpacidad,
                    min: 0.35,
                    max: 1.0,
                    onChanged: (v) => setState(() => _prendaOpacidad = v),
                  ),
                ),
              ),
              // Botón alternar recorte de foto de catálogo
              if (widget.producto.imagenUrl != null)
                TextButton.icon(
                  style: TextButton.styleFrom(padding: EdgeInsets.zero),
                  icon: Icon(
                    _usarRecorteFotoCatalogo ? Icons.check_box : Icons.check_box_outline_blank,
                    size: 16,
                    color: const Color(0xFF38BDF8),
                  ),
                  label: const Text(
                    'Foto Catálogo',
                    style: TextStyle(color: Color(0xFF38BDF8), fontSize: 11),
                  ),
                  onPressed: () {
                    setState(() => _usarRecorteFotoCatalogo = !_usarRecorteFotoCatalogo);
                  },
                ),
            ],
          ),
          const SizedBox(height: 10),

          // 5. Botón de Compra Directa: "¡Me queda perfecto! Agregar al Carrito"
          SizedBox(
            width: double.infinity,
            height: 46,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF6366F1),
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                elevation: 4,
              ),
              onPressed: () {
                cartCtrl.agregarProducto(widget.producto);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      '¡${widget.producto.nombre} (Talla $_tallaSeleccionada) agregada al carrito!',
                    ),
                    backgroundColor: const Color(0xFF10B981),
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
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.shopping_bag_outlined, size: 18),
                  const SizedBox(width: 8),
                  Text(
                    '¡Me queda perfecto! Llevar Talla $_tallaSeleccionada (Bs. ${widget.producto.precio.toStringAsFixed(2)})',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTipoPrendaChip(String label, GarmentType tipo) {
    final isSel = _tipoPrenda == tipo;
    return GestureDetector(
      onTap: () => setState(() => _tipoPrenda = tipo),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        decoration: BoxDecoration(
          color: isSel ? const Color(0xFF6366F1).withValues(alpha: 0.2) : Colors.transparent,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSel ? const Color(0xFF818CF8) : Colors.white24,
          ),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: isSel ? const Color(0xFF818CF8) : Colors.white70,
            fontSize: 11,
            fontWeight: isSel ? FontWeight.bold : FontWeight.normal,
          ),
        ),
      ),
    );
  }

  void _mostrarBottomSheetFoto() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(16))),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Cargar Foto para el Vestidor',
              style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 16),
            ListTile(
              leading: const Icon(Icons.camera_alt, color: Color(0xFF38BDF8)),
              title: const Text('Tomar Foto de Cuerpo Entero', style: TextStyle(color: Colors.white)),
              subtitle: const Text('Usa buena iluminación de frente', style: TextStyle(color: Colors.white54, fontSize: 11)),
              onTap: () {
                Navigator.pop(ctx);
                _seleccionarFotoPersonal(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library, color: Color(0xFF6366F1)),
              title: const Text('Elegir de Galería', style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(ctx);
                _seleccionarFotoPersonal(ImageSource.gallery);
              },
            ),
          ],
        ),
      ),
    );
  }
}
