// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Módulo: CU10 - Gestionar Reservas de Prendas
// Ubicación: mobile-app/lib/views/my_reservations_view.dart
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../controllers/reservation_controller.dart';
import '../models/reservation_model.dart';

class MyReservationsView extends StatefulWidget {
  const MyReservationsView({super.key});

  @override
  State<MyReservationsView> createState() => _MyReservationsViewState();
}

class _MyReservationsViewState extends State<MyReservationsView> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ReservationController>().cargarMisReservas();
    });
  }

  void _mostrarTicketDigital(BuildContext context, ReservaModel reserva) {
    showDialog(
      context: context,
      builder: (ctx) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        backgroundColor: const Color(0xFF1E293B),
        child: Padding(
          padding: const EdgeInsets.all(22.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.confirmation_number_outlined, color: Color(0xFF38BDF8), size: 22),
                      SizedBox(width: 8),
                      Text('TICKET DIGITAL', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white60, size: 20),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const Divider(color: Colors.white24, height: 24),
              const Text(
                'Presenta este código al cajero en sucursal:',
                style: TextStyle(color: Colors.white70, fontSize: 13),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 12),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFF38BDF8), width: 1.5),
                ),
                child: Column(
                  children: [
                    Text(
                      reserva.codigoReserva,
                      style: const TextStyle(
                        fontFamily: 'monospace',
                        color: Color(0xFF38BDF8),
                        fontSize: 26,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 3,
                      ),
                    ),
                    const SizedBox(height: 8),
                    // Simulación visual de código de barras
                    const Text(
                      '║▌│█║▌│ █║▌│█│║▌║▌│█',
                      style: TextStyle(
                        fontFamily: 'monospace',
                        color: Colors.white38,
                        fontSize: 20,
                        letterSpacing: 2,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),
              OutlinedButton.icon(
                style: OutlinedButton.styleFrom(
                  foregroundColor: const Color(0xFF38BDF8),
                  side: const BorderSide(color: Color(0xFF38BDF8)),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                icon: const Icon(Icons.copy, size: 16),
                label: const Text('Copiar Código'),
                onPressed: () {
                  Clipboard.setData(ClipboardData(text: reserva.codigoReserva));
                  HapticFeedback.lightImpact();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('¡Código de reserva copiado al portapapeles!'),
                      backgroundColor: Colors.teal,
                      duration: Duration(seconds: 2),
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.amber.withAlpha(25),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.amber.withAlpha(80)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.timer_outlined, color: Colors.amber, size: 20),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Válido por 48 horas en ${reserva.sucursalNombre ?? "Sucursal Central"}. Las prendas se reservan automáticamente.',
                        style: const TextStyle(color: Colors.amber, fontSize: 11),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getStatusColor(String estado) {
    switch (estado.toUpperCase()) {
      case 'PENDIENTE':
        return Colors.amber.shade700;
      case 'CONFIRMADA':
        return Colors.blue.shade600;
      case 'ENTREGADA':
        return Colors.green.shade600;
      case 'CANCELADA':
        return Colors.red.shade600;
      default:
        return Colors.grey.shade600;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        title: const Text(
          'Mis Reservas (CU10)',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Consumer<ReservationController>(
        builder: (context, controller, child) {
          if (controller.cargando && controller.reservas.isEmpty) {
            return const Center(
              child: CircularProgressIndicator(color: Colors.indigoAccent),
            );
          }

          if (controller.error != null && controller.reservas.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 64, color: Colors.redAccent),
                  const SizedBox(height: 16),
                  Text(
                    controller.error!,
                    style: const TextStyle(color: Colors.white70),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => controller.cargarMisReservas(),
                    child: const Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          if (controller.reservas.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.event_seat_outlined, size: 80, color: Colors.blueGrey.shade600),
                  const SizedBox(height: 16),
                  const Text(
                    'No tienes reservas registradas',
                    style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Agrega prendas al carrito y resérvalas para retiro en sucursal.',
                    style: TextStyle(color: Colors.white60),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () => controller.cargarMisReservas(),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: controller.reservas.length,
              itemBuilder: (context, index) {
                final reserva = controller.reservas[index];
                final statusColor = _getStatusColor(reserva.estado);

                return Container(
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1E293B),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: const Color(0x14FFFFFF)),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header con Código y Estado
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'CÓDIGO DE RESERVA',
                                  style: TextStyle(
                                    color: Colors.white60,
                                    fontSize: 11,
                                    letterSpacing: 0.8,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  reserva.codigoReserva,
                                  style: const TextStyle(
                                    color: Color(0xFF38BDF8),
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    fontFamily: 'monospace',
                                  ),
                                ),
                              ],
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                              decoration: BoxDecoration(
                                color: statusColor.withAlpha(38),
                                borderRadius: BorderRadius.circular(20),
                                border: Border.all(color: statusColor.withAlpha(102)),
                              ),
                              child: Text(
                                reserva.estado,
                                style: TextStyle(
                                  color: statusColor,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const Divider(color: Colors.white12, height: 24),

                        // Sucursal
                        if (reserva.sucursalNombre != null) ...[
                          Row(
                            children: [
                              const Icon(Icons.storefront, size: 18, color: Colors.indigoAccent),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  '${reserva.sucursalNombre!} (${reserva.sucursalDireccion ?? ''})',
                                  style: const TextStyle(color: Colors.white, fontSize: 13),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                        ],

                        // Desglose de ítems
                        Text(
                          'Prendas (${reserva.totalItems} uds):',
                          style: const TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 6),
                        ...reserva.detalles.map((det) => Padding(
                              padding: const EdgeInsets.symmetric(vertical: 3),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    '${det.cantidad}x ${det.productoNombre} ${det.talla != null ? '(${det.talla})' : ''}',
                                    style: const TextStyle(color: Colors.white, fontSize: 13),
                                  ),
                                  Text(
                                    'Bs. ${det.subtotal.toStringAsFixed(2)}',
                                    style: const TextStyle(color: Colors.greenAccent, fontSize: 13),
                                  ),
                                ],
                              ),
                            )),

                        const Divider(color: Colors.white12, height: 24),

                        // Footer con Total y Acciones
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Total en caja:',
                                  style: TextStyle(color: Colors.white60, fontSize: 11),
                                ),
                                Text(
                                  'Bs. ${reserva.totalEstimado.toStringAsFixed(2)}',
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              children: [
                                ElevatedButton.icon(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: const Color(0xFF0284C7),
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                    elevation: 0,
                                  ),
                                  onPressed: () => _mostrarTicketDigital(context, reserva),
                                  icon: const Icon(Icons.qr_code_2, size: 16),
                                  label: const Text('Ticket', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                                ),
                                if (reserva.estado == 'PENDIENTE') ...[
                                  const SizedBox(width: 4),
                                  TextButton.icon(
                                    onPressed: () async {
                                      final confirmar = await showDialog<bool>(
                                        context: context,
                                        builder: (ctx) => AlertDialog(
                                          title: const Text('Cancelar Reserva'),
                                          content: Text('¿Deseas cancelar la reserva ${reserva.codigoReserva}? El stock apartado será liberado.'),
                                          actions: [
                                            TextButton(
                                              onPressed: () => Navigator.pop(ctx, false),
                                              child: const Text('No'),
                                            ),
                                            ElevatedButton(
                                              style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                                              onPressed: () => Navigator.pop(ctx, true),
                                              child: const Text('Sí, Cancelar'),
                                            ),
                                          ],
                                        ),
                                      );

                                      if (confirmar == true) {
                                        await controller.cancelarReserva(reserva.id);
                                      }
                                    },
                                    icon: const Icon(Icons.cancel_outlined, size: 14, color: Colors.redAccent),
                                    label: const Text(
                                      'Cancelar',
                                      style: TextStyle(color: Colors.redAccent, fontSize: 12),
                                    ),
                                  ),
                                ],
                              ],
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
