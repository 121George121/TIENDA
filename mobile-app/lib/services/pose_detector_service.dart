// ==============================================================================
// SERVICIO: DETECCIÓN DE POSE Y TRACKING ANATÓMICO CORPORAL (ML KIT)
// Ubicación: mobile-app/lib/services/pose_detector_service.dart
// Detecta hombros, cuello, torso y rotación para posicionar y escalar
// automáticamente la prenda sobre el cuerpo sin necesidad de arrastre manual.
// ==============================================================================

import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';

class BodyPoseData {
  final Offset shoulderCenter;
  final double shoulderWidth;
  final double rotationAngle;
  final double? torsoLength;
  final double confidence;
  final Size imageSize;

  BodyPoseData({
    required this.shoulderCenter,
    required this.shoulderWidth,
    required this.rotationAngle,
    this.torsoLength,
    required this.confidence,
    required this.imageSize,
  });
}

class PoseDetectorService {
  PoseDetector? _poseDetector;

  void _initDetector() {
    _poseDetector ??= PoseDetector(
      options: PoseDetectorOptions(
        mode: PoseDetectionMode.single,
        model: PoseDetectionModel.base,
      ),
    );
  }

  /// Procesa una imagen estática (foto tomada o subida de galería)
  Future<BodyPoseData?> detectPoseFromFile(File file) async {
    _initDetector();

    try {
      final inputImage = InputImage.fromFile(file);
      final List<Pose> poses = await _poseDetector!.processImage(inputImage);

      if (poses.isEmpty) return null;

      final pose = poses.first;
      final leftShoulder = pose.landmarks[PoseLandmarkType.leftShoulder];
      final rightShoulder = pose.landmarks[PoseLandmarkType.rightShoulder];

      if (leftShoulder == null || rightShoulder == null) return null;

      // Calcular ancho de hombros euclidiano
      final dx = rightShoulder.x - leftShoulder.x;
      final dy = rightShoulder.y - leftShoulder.y;
      final shoulderWidth = sqrt(dx * dx + dy * dy);

      // Punto central exacto entre ambos hombros
      final centerX = (leftShoulder.x + rightShoulder.x) / 2;
      final centerY = (leftShoulder.y + rightShoulder.y) / 2;

      // Ángulo de inclinación de hombros (rotación)
      final rotation = atan2(dy, dx);

      // Distancia de torso hacia caderas (si están visibles)
      double? torsoLength;
      final leftHip = pose.landmarks[PoseLandmarkType.leftHip];
      final rightHip = pose.landmarks[PoseLandmarkType.rightHip];
      if (leftHip != null && rightHip != null) {
        final hipCenterY = (leftHip.y + rightHip.y) / 2;
        torsoLength = (hipCenterY - centerY).abs();
      }

      // Tamaño de imagen original
      final imgSize = inputImage.metadata?.size ?? const Size(1080, 1920);

      // Promedio de confianza de detección
      final conf = ((leftShoulder.likelihood + rightShoulder.likelihood) / 2);

      return BodyPoseData(
        shoulderCenter: Offset(centerX, centerY),
        shoulderWidth: shoulderWidth,
        rotationAngle: rotation,
        torsoLength: torsoLength,
        confidence: conf,
        imageSize: imgSize,
      );
    } catch (e) {
      debugPrint('Error en PoseDetectorService: $e');
      return null;
    }
  }

  void dispose() {
    _poseDetector?.close();
    _poseDetector = null;
  }
}
