// ==============================================================================
// WIDGET: IMAGEN DE PRENDA CON CACHÉ PERSISTENTE EN DISCO
// Ubicación: mobile-app/lib/widgets/cached_garment_image.dart
// Carga instantánea (0ms) desde el almacenamiento interno del dispositivo.
// Descarga una única vez por red y no vuelve a descargar nunca más.
// ==============================================================================

import 'dart:io';
import 'package:flutter/material.dart';
import '../services/cache_service.dart';

class CachedGarmentImage extends StatefulWidget {
  final String? imageUrl;
  final double? width;
  final double? height;
  final BoxFit fit;
  final BorderRadius? borderRadius;
  final Widget? placeholder;
  final Widget? errorWidget;

  const CachedGarmentImage({
    super.key,
    required this.imageUrl,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
    this.borderRadius,
    this.placeholder,
    this.errorWidget,
  });

  @override
  State<CachedGarmentImage> createState() => _CachedGarmentImageState();
}

class _CachedGarmentImageState extends State<CachedGarmentImage> {
  File? _imageFile;
  bool _cargando = false;
  bool _error = false;
  String? _lastUrl;

  @override
  void initState() {
    super.initState();
    _resolverImagen();
  }

  @override
  void didUpdateWidget(covariant CachedGarmentImage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.imageUrl != widget.imageUrl) {
      _resolverImagen();
    }
  }

  void _resolverImagen() {
    final url = widget.imageUrl?.trim() ?? '';
    _lastUrl = url;

    if (url.isEmpty) {
      setState(() {
        _imageFile = null;
        _cargando = false;
        _error = false;
      });
      return;
    }

    // 1. Verificación síncrona inmediata en caché de disco (Cero latencia)
    final enCache = CacheService.instance.getCachedImageFile(url);
    if (enCache != null) {
      setState(() {
        _imageFile = enCache;
        _cargando = false;
        _error = false;
      });
      return;
    }

    // 2. Si no está en disco todavía, descargar en segundo plano
    setState(() {
      _imageFile = null;
      _cargando = true;
      _error = false;
    });

    CacheService.instance.getOrDownloadImage(url).then((file) {
      if (!mounted || _lastUrl != url) return;
      if (file != null) {
        setState(() {
          _imageFile = file;
          _cargando = false;
          _error = false;
        });
      } else {
        setState(() {
          _cargando = false;
          _error = true;
        });
      }
    }).catchError((_) {
      if (!mounted || _lastUrl != url) return;
      setState(() {
        _cargando = false;
        _error = true;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    Widget content;

    if (widget.imageUrl == null || widget.imageUrl!.trim().isEmpty) {
      content = widget.errorWidget ?? _buildDefaultFallback();
    } else if (_imageFile != null) {
      content = Image.file(
        _imageFile!,
        width: widget.width,
        height: widget.height,
        fit: widget.fit,
        errorBuilder: (_, __, ___) => widget.errorWidget ?? _buildDefaultFallback(),
      );
    } else if (_cargando) {
      content = widget.placeholder ?? _buildDefaultPlaceholder();
    } else if (_error) {
      // Intento de fallback con Image.network directo si la escritura a disco falló
      content = Image.network(
        widget.imageUrl!.trim(),
        width: widget.width,
        height: widget.height,
        fit: widget.fit,
        errorBuilder: (_, __, ___) => widget.errorWidget ?? _buildDefaultFallback(),
        loadingBuilder: (_, child, progress) {
          if (progress == null) return child;
          return widget.placeholder ?? _buildDefaultPlaceholder();
        },
      );
    } else {
      content = widget.errorWidget ?? _buildDefaultFallback();
    }

    if (widget.borderRadius != null) {
      return ClipRRect(
        borderRadius: widget.borderRadius!,
        child: content,
      );
    }

    return content;
  }

  Widget _buildDefaultPlaceholder() {
    return Container(
      width: widget.width,
      height: widget.height,
      color: const Color(0xFFF1F5F9),
      child: const Center(
        child: SizedBox(
          width: 20,
          height: 20,
          child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF94A3B8)),
        ),
      ),
    );
  }

  Widget _buildDefaultFallback() {
    return Container(
      width: widget.width,
      height: widget.height,
      color: const Color(0xFFF1F5F9),
      child: const Center(
        child: Icon(Icons.checkroom, size: 36, color: Color(0xFF94A3B8)),
      ),
    );
  }
}
