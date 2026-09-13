// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de Carrito de Compras (CU09 & CU15)
// Ubicación: mobile-app/lib/views/cart_view.dart
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/cart_controller.dart';
import '../controllers/auth_controller.dart';
import '../controllers/reservation_controller.dart';
import 'my_reservations_view.dart';
import 'orders_history_view.dart';

class CartView extends StatelessWidget {
  const CartView({super.key});

  @override
  Widget build(BuildContext context) {
    final cartCtrl = Provider.of<CartController>(context);
    final authCtrl = Provider.of<AuthController>(context, listen: false);
    final resCtrl = Provider.of<ReservationController>(context, listen: false);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('🛒 Carrito de Compras'),
        backgroundColor: const Color(0xFF0F172A),
        foregroundColor: Colors.white,
        elevation: 2,
        actions: [
          IconButton(
            icon: const Icon(Icons.bookmark_border),
            tooltip: 'Mis Reservas (CU10)',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const MyReservationsView()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.receipt_long),
            tooltip: 'Historial de Pedidos (CU15)',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const OrdersHistoryView()),
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
                                                  child: Icon(Icons.remove, size: 16),
                                                ),
                                              ),
                                              Text(
                                                '${item.cantidad}',
                                                style: const TextStyle(fontWeight: FontWeight.bold),
                                              ),
                                              InkWell(
                                                onTap: () => cartCtrl.incrementar(item.product.id),
                                                child: const Padding(
                                                  padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                  child: Icon(Icons.add, size: 16),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                        const Spacer(),
                                        Text(
                                          'Bs. ${item.subtotal.toStringAsFixed(2)}',
                                          style: const TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 15,
                                            color: Color(0xFF0F172A),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),

                // Panel Inferior de Checkout / Reserva
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(
                        color: Color(0x0F000000),
                        offset: Offset(0, -4),
                        blurRadius: 10,
                      )
                    ],
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
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

                      // Botón 1: Comprar Online (CU15)
                      SizedBox(
                        width: double.infinity,
                        height: 46,
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFFE11D48),
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.shopping_bag_outlined),
                          label: const Text('Comprar Online (Envío a Domicilio)', style: TextStyle(fontWeight: FontWeight.bold)),
                          onPressed: () async {
                            if (!authCtrl.isAuthenticated) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('Inicia sesión para confirmar tu compra digital.'),
                                  backgroundColor: Colors.orange,
                                ),
                              );
                              Navigator.pushNamed(context, '/login');
                              return;
                            }

                            showDialog(
                              context: context,
                              barrierDismissible: false,
                              builder: (_) => const Center(child: CircularProgressIndicator()),
                            );

                            bool exito = await cartCtrl.procesarCompra(
                              "Av. Principal #123, Santa Cruz",
                              authToken: authCtrl.currentUser?.token,
                            );

                            if (!context.mounted) return;
                            Navigator.pop(context); // Cerrar spinner

                            if (exito) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('¡Pedido confirmado exitosamente!'),
                                  backgroundColor: Colors.green,
                                ),
                              );
                              Navigator.pushReplacement(
                                context,
                                MaterialPageRoute(builder: (_) => const OrdersHistoryView()),
                              );
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('No se pudo procesar la orden. Verifica stock o conexión.'),
                                  backgroundColor: Colors.red,
                                ),
                              );
                            }
                          },
                        ),
                      ),

                      const SizedBox(height: 10),

                      // Botón 2: Reservar en Sucursal Física (CU10)
                      SizedBox(
                        width: double.infinity,
                        height: 46,
                        child: OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: const Color(0xFF0F172A),
                            side: const BorderSide(color: Color(0xFF0F172A), width: 1.5),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.storefront),
                          label: const Text('Apartar y Pagar en Tienda (CU10)', style: TextStyle(fontWeight: FontWeight.bold)),
                          onPressed: () async {
                            showDialog(
                              context: context,
                              barrierDismissible: false,
                              builder: (_) => const Center(child: CircularProgressIndicator()),
                            );

                            final nuevaReserva = await resCtrl.crearReservaDesdeCarrito(
                              sucursalId: cartCtrl.sucursalId,
                              token: authCtrl.currentUser?.token,
                            );

                            if (!context.mounted) return;
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
                                      const Text(
                                        'Presenta este código en sucursal para abonar y retirar tus prendas.',
                                        style: TextStyle(color: Colors.white70, fontSize: 13),
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
