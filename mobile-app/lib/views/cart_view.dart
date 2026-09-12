// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de Carrito de Compras (CU09)
// Ubicación: mobile-app/lib/views/cart_view.dart
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/cart_controller.dart';
import '../controllers/reservation_controller.dart';
import 'my_reservations_view.dart';

class CartView extends StatelessWidget {
  const CartView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final cartCtrl = Provider.of<CartController>(context);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Mi Carrito (CU09)'),
        backgroundColor: const Color(0xFF0F172A),
        foregroundColor: Colors.white,
        elevation: 2,
        actions: [
          IconButton(
            icon: const Icon(Icons.receipt_long),
            tooltip: 'Mis Reservas (CU10)',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const MyReservationsView()),
              );
            },
          ),
          if (cartCtrl.items.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_sweep),
              tooltip: 'Vaciar Carrito',
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('¿Vaciar carrito?'),
                    content: const Text('Se eliminarán todas las prendas seleccionadas.'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: const Text('Cancelar'),
                      ),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                        onPressed: () {
                          cartCtrl.limpiarCarrito();
                          Navigator.pop(ctx);
                        },
                        child: const Text('Vaciar'),
                      ),
                    ],
                  ),
                );
              },
            ),
        ],
      ),
      body: cartCtrl.items.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.remove_shopping_cart_outlined, size: 70, color: Colors.grey),
                  const SizedBox(height: 16),
                  const Text(
                    'Tu carrito está vacío',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Añade prendas desde el catálogo para continuar.',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF0F172A),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                    ),
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Volver al Catálogo'),
                    onPressed: () => Navigator.pop(context),
                  )
                ],
              ),
            )
          : Column(
              children: [
                // Lista de Prendas
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.all(12),
                    itemCount: cartCtrl.items.length,
                    itemBuilder: (ctx, i) {
                      final item = cartCtrl.items.values.toList()[i];
                      return Card(
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                        margin: const EdgeInsets.symmetric(vertical: 6),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Row(
                            children: [
                              ClipRRect(
                                borderRadius: BorderRadius.circular(8),
                                child: item.product.imagenUrl != null
                                    ? Image.network(
                                        item.product.imagenUrl!,
                                        width: 65,
                                        height: 75,
                                        fit: BoxFit.cover,
                                        errorBuilder: (_, __, ___) => Container(
                                          width: 65,
                                          height: 75,
                                          color: Colors.grey[200],
                                          child: const Icon(Icons.image_not_supported),
                                        ),
                                      )
                                    : Container(
                                        width: 65,
                                        height: 75,
                                        color: Colors.grey[200],
                                        child: const Icon(Icons.checkroom),
                                      ),
                              ),
                              const SizedBox(width: 14),

                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      item.product.nombre,
                                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      'Bs. ${item.product.precio.toStringAsFixed(2)} c/u',
                                      style: const TextStyle(color: Colors.grey, fontSize: 12),
                                    ),
                                    const SizedBox(height: 8),

                                    // Controles Stepper + y -
                                    Row(
                                      children: [
                                        Container(
                                          decoration: BoxDecoration(
                                            border: Border.all(color: Colors.grey.shade300),
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                          child: Row(
                                            children: [
                                              InkWell(
                                                onTap: () => cartCtrl.decrementar(item.product.id),
                                                child: const Padding(
                                                  padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                  child: Text('-', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                                                ),
                                              ),
                                              Padding(
                                                padding: const EdgeInsets.symmetric(horizontal: 8),
                                                child: Text(
                                                  '${item.cantidad}',
                                                  style: const TextStyle(fontWeight: FontWeight.bold),
                                                ),
                                              ),
                                              InkWell(
                                                onTap: () => cartCtrl.incrementar(item.product.id),
                                                child: const Padding(
                                                  padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                  child: Text('+', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),

                              Column(
                                crossAxisAlignment: CrossAxisAlignment.end,
                                children: [
                                  IconButton(
                                    icon: const Icon(Icons.delete_outline, color: Colors.grey, size: 20),
                                    onPressed: () => cartCtrl.removerProducto(item.product.id),
                                  ),
                                  Text(
                                    'Bs. ${item.subtotal.toStringAsFixed(2)}',
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w800,
                                      fontSize: 15,
                                      color: Color(0xFF0F172A),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),

                // Footer con Totales y Botón de Reserva (CU10)
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.06),
                        blurRadius: 10,
                        offset: const Offset(0, -4),
                      ),
                    ],
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'TOTAL:',
                            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.grey),
                          ),
                          Text(
                            'Bs. ${cartCtrl.totalMonto.toStringAsFixed(2)}',
                            style: const TextStyle(
                              fontSize: 22,
                              fontWeight: FontWeight.w800,
                              color: Color(0xFF0F172A),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 14),
                      SizedBox(
                        width: double.infinity,
                        height: 48,
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF0F172A),
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.event_seat),
                          label: const Text(
                            'Proceder a Reservar en Tienda (CU10)',
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                          onPressed: () async {
                            final sucursalId = cartCtrl.sucursalId ?? 1;
                            final resCtrl = context.read<ReservationController>();

                            showDialog(
                              context: context,
                              barrierDismissible: false,
                              builder: (_) => const Center(child: CircularProgressIndicator(color: Colors.white)),
                            );

                            final nuevaReserva = await resCtrl.crearReserva(
                              sucursalId: sucursalId,
                              observaciones: 'Reserva generada desde App Móvil',
                            );

                            Navigator.pop(context); // Cerrar loading

                            if (nuevaReserva != null) {
                              cartCtrl.limpiarCarrito();
                              showDialog(
                                context: context,
                                builder: (ctx) => AlertDialog(
                                  backgroundColor: const Color(0xFF1E293B),
                                  title: const Row(
                                    children: [
                                      Icon(Icons.check_circle, color: Colors.greenAccent),
                                      SizedBox(width: 8),
                                      Text('¡Reserva Exitosa!', style: TextStyle(color: Colors.white)),
                                    ],
                                  ),
                                  content: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      const Text(
                                        'Código de Retiro en Tienda:',
                                        style: TextStyle(color: Colors.white70, fontSize: 12),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        nuevaReserva.codigoReserva,
                                        style: const TextStyle(
                                          color: Color(0xFF38BDF8),
                                          fontSize: 24,
                                          fontWeight: FontWeight.bold,
                                          fontFamily: 'monospace',
                                        ),
                                      ),
                                      const SizedBox(height: 8),
                                      Text(
                                        'Presenta este código en sucursal para abonar y retirar tus prendas.',
                                        style: const TextStyle(color: Colors.white70, fontSize: 13),
                                      ),
                                    ],
                                  ),
                                  actions: [
                                    ElevatedButton(
                                      style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF38BDF8)),
                                      onPressed: () {
                                        Navigator.pop(ctx);
                                        Navigator.push(
                                          context,
                                          MaterialPageRoute(builder: (_) => const MyReservationsView()),
                                        );
                                      },
                                      child: const Text('Ver Mis Reservas', style: TextStyle(color: Colors.black)),
                                    ),
                                  ],
                                ),
                              );
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text(resCtrl.error ?? 'Error al procesar reserva'),
                                  backgroundColor: Colors.redAccent,
                                ),
                              );
                            }
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
}
