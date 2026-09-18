// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de Carrito de Compras (CU09 & CU15)
// Ubicación: mobile-app/lib/views/cart_view.dart
// ==============================================================================

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/cart_controller.dart';
import '../controllers/auth_controller.dart';
import '../controllers/reservation_controller.dart';
import '../controllers/payment_controller.dart';
import '../controllers/recommendation_controller.dart';
import 'my_reservations_view.dart';
import 'orders_history_view.dart';

class CartView extends StatefulWidget {
  const CartView({super.key});

  @override
  State<CartView> createState() => _CartViewState();
}

class _CartViewState extends State<CartView> {
  int _metodoPagoSeleccionado = 6; // 6: PayPal, 4: QR Simple, 2: Efectivo

  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      if (!mounted) return;
      final cart = context.read<CartController>();
      if (cart.items.isNotEmpty) {
        context.read<RecommendationController>().fetchRecomendaciones(
          carritoIds: cart.items.keys.toList(),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final cartCtrl = Provider.of<CartController>(context);
    final authCtrl = Provider.of<AuthController>(context, listen: false);
    final resCtrl = Provider.of<ReservationController>(context, listen: false);
    final payCtrl = Provider.of<PaymentController>(context, listen: false);

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
                                                onTap: () {
                                                  final ok = cartCtrl.incrementar(item.product.id);
                                                  if (!ok) {
                                                    ScaffoldMessenger.of(context).hideCurrentSnackBar();
                                                    ScaffoldMessenger.of(context).showSnackBar(
                                                      SnackBar(
                                                        content: Text('Límite de stock alcanzado (${item.product.stock} uds. disponibles)'),
                                                        backgroundColor: Colors.orange.shade800,
                                                        duration: const Duration(seconds: 2),
                                                      ),
                                                    );
                                                  }
                                                },
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

                // CU18: Recomendaciones Stylist IA (Completa tu Outfit)
                Consumer<RecommendationController>(
                  builder: (_, recCtrl, __) {
                    if (recCtrl.recomendaciones.isEmpty) return const SizedBox.shrink();
                    return Container(
                      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: const Color(0xFFFAF5FF),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: const Color(0xFFE9D5FF)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Row(
                                children: [
                                  const Icon(Icons.auto_awesome, color: Color(0xFF7E22CE), size: 16),
                                  const SizedBox(width: 6),
                                  Text(
                                    'Stylist IA: Completa tu Outfit',
                                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.purple.shade900),
                                  ),
                                ],
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(color: Colors.purple.shade700, borderRadius: BorderRadius.circular(8)),
                                child: const Text('CU18 Gemini', style: TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.bold)),
                              ),
                            ],
                          ),
                          const SizedBox(height: 6),
                          SizedBox(
                            height: 80,
                            child: ListView.builder(
                              scrollDirection: Axis.horizontal,
                              itemCount: recCtrl.recomendaciones.length,
                              itemBuilder: (ctx, idx) {
                                final rec = recCtrl.recomendaciones[idx];
                                return Container(
                                  width: 180,
                                  margin: const EdgeInsets.only(right: 8),
                                  padding: const EdgeInsets.all(8),
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    borderRadius: BorderRadius.circular(8),
                                    border: Border.all(color: const Color(0xFFF3E8FF)),
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(
                                        rec.nombre,
                                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11),
                                        maxLines: 1,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      Text(
                                        rec.razonEstilo,
                                        style: TextStyle(fontSize: 9, color: Colors.purple.shade800),
                                        maxLines: 2,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      Text(
                                        'Bs. ${rec.precio.toStringAsFixed(2)}',
                                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: Color(0xFF7E22CE)),
                                      ),
                                    ],
                                  ),
                                );
                              },
                            ),
                          ),
                        ],
                      ),
                    );
                  },
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
                      // Selector de Sucursal para Retiro / Reserva
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        margin: const EdgeInsets.only(bottom: 12),
                        decoration: BoxDecoration(
                          color: const Color(0xFFF8FAFC),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: const Color(0xFFE2E8F0)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.storefront, size: 20, color: Color(0xFF0F172A)),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'SUCURSAL SELECCIONADA',
                                    style: TextStyle(fontSize: 10, color: Colors.grey, fontWeight: FontWeight.w700, letterSpacing: 0.5),
                                  ),
                                  Text(
                                    cartCtrl.sucursalNombre ?? 'Sucursal Central (Principal)',
                                    style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF0F172A)),
                                  ),
                                ],
                              ),
                            ),
                            PopupMenuButton<int>(
                              tooltip: 'Cambiar Sucursal',
                              icon: const Icon(Icons.swap_horiz, color: Color(0xFF0F172A)),
                              onSelected: (id) {
                                final sucursales = {
                                  1: 'Sucursal Central (Principal)',
                                  2: 'Sucursal Equipetrol',
                                  3: 'Sucursal Norte',
                                };
                                cartCtrl.setSucursal(id, sucursales[id] ?? 'Sucursal #$id');
                              },
                              itemBuilder: (ctx) => const [
                                PopupMenuItem(value: 1, child: Text('Sucursal Central (Principal)')),
                                PopupMenuItem(value: 2, child: Text('Sucursal Equipetrol')),
                                PopupMenuItem(value: 3, child: Text('Sucursal Norte')),
                              ],
                            ),
                          ],
                        ),
                      ),

                      // Selector de Método de Pago (CU16 - PayPal, QR, Efectivo)
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'MÉTODO DE PAGO:',
                            style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.grey, letterSpacing: 0.5),
                          ),
                          const SizedBox(height: 6),
                          Row(
                            children: [
                              _buildMetodoChip(6, 'PayPal', Icons.credit_card, const Color(0xFF003087)),
                              const SizedBox(width: 6),
                              _buildMetodoChip(4, 'QR Simple', Icons.qr_code_2, const Color(0xFF6D28D9)),
                              const SizedBox(width: 6),
                              _buildMetodoChip(2, 'Efectivo', Icons.payments_outlined, const Color(0xFF15803D)),
                            ],
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),

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

                      // Botón 1: Comprar Online (CU15 & CU16)
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

                            final order = await cartCtrl.procesarCompra(
                              "Av. Principal #123, Santa Cruz",
                              authToken: authCtrl.currentUser?.token,
                              metodoId: _metodoPagoSeleccionado,
                            );

                            if (!context.mounted) return;
                            Navigator.pop(context); // Cerrar spinner

                            if (order != null && order['id'] != null) {
                              final ventaId = order['id'] as int;
                              final pagoInfo = await payCtrl.iniciarPago(
                                ventaId: ventaId,
                                metodoId: _metodoPagoSeleccionado,
                                token: authCtrl.currentUser?.token,
                              );

                              if (!context.mounted) return;

                              if (_metodoPagoSeleccionado == 6) {
                                _mostrarDialogoPayPal(context, ventaId, pagoInfo, payCtrl);
                              } else if (_metodoPagoSeleccionado == 4) {
                                _mostrarDialogoQR(context, ventaId, pagoInfo, payCtrl);
                              } else {
                                _mostrarDialogoEfectivo(context, ventaId, pagoInfo, payCtrl);
                              }
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

  Widget _buildMetodoChip(int id, String label, IconData icon, Color activeColor) {
    final isSelected = _metodoPagoSeleccionado == id;
    return Expanded(
      child: InkWell(
        onTap: () => setState(() => _metodoPagoSeleccionado = id),
        borderRadius: BorderRadius.circular(10),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? activeColor.withAlpha(25) : const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: isSelected ? activeColor : const Color(0xFFE2E8F0),
              width: isSelected ? 2 : 1,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 20, color: isSelected ? activeColor : Colors.grey[700]),
              const SizedBox(height: 2),
              Text(
                label,
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                  color: isSelected ? activeColor : Colors.grey[800],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _mostrarDialogoPayPal(BuildContext context, int ventaId, Map<String, dynamic>? pagoInfo, PaymentController payCtrl) {
    final paypalUrl = pagoInfo?['paypal_url'] ?? 'https://www.sandbox.paypal.com/checkoutnow';
    final montoUsd = pagoInfo?['monto_usd'] ?? '0.00';

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.payment, color: Color(0xFF003087)),
            SizedBox(width: 10),
            Text('PayPal Checkout', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Serás redirigido a la pasarela segura de PayPal para iniciar sesión o pagar con tu tarjeta de débito/crédito.',
              style: TextStyle(fontSize: 13, color: Colors.black87),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: const Color(0xFFEFF6FF), borderRadius: BorderRadius.circular(8)),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Total a pagar (USD):', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                  Text('\$$montoUsd USD', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF003087))),
                ],
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(ctx);
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const OrdersHistoryView()));
            },
            child: const Text('Ver Mis Pedidos'),
          ),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF003087),
              foregroundColor: Colors.white,
            ),
            icon: const Icon(Icons.open_in_new, size: 16),
            label: const Text('Ir a Pagar en PayPal'),
            onPressed: () async {
              await payCtrl.abrirPayPal(paypalUrl);
            },
          ),
        ],
      ),
    );
  }

  void _mostrarDialogoQR(BuildContext context, int ventaId, Map<String, dynamic>? pagoInfo, PaymentController payCtrl) {
    final qrBase64 = pagoInfo?['qr_base64'] as String?;
    final expiracion = pagoInfo?['tiempo_expiracion_minutos'] ?? 15;

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.qr_code_2, color: Color(0xFF6D28D9)),
            SizedBox(width: 8),
            Text('Pago Simple por QR', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Escanea este código desde la app de tu banco (BCP, BNB, etc.) para completar el pago.',
              style: TextStyle(fontSize: 12, color: Colors.black54),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            if (qrBase64 != null && qrBase64.contains(','))
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.memory(
                  base64Decode(qrBase64.split(',').last),
                  width: 180,
                  height: 180,
                  fit: BoxFit.contain,
                ),
              )
            else
              Container(
                width: 180,
                height: 180,
                color: Colors.grey[200],
                child: const Icon(Icons.qr_code, size: 80, color: Colors.grey),
              ),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(color: Colors.amber.shade50, borderRadius: BorderRadius.circular(20), border: Border.all(color: Colors.amber.shade300)),
              child: Text(
                '⏱️ Válido por $expiracion minutos',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.amber.shade900),
              ),
            ),
          ],
        ),
        actions: [
          OutlinedButton.icon(
            icon: const Icon(Icons.receipt, size: 16),
            label: const Text('Ver Recibo Fiscal'),
            onPressed: () async {
              final url = payCtrl.getComprobanteHtmlUrl(ventaId);
              await payCtrl.abrirPayPal(url);
            },
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF6D28D9), foregroundColor: Colors.white),
            onPressed: () {
              Navigator.pop(ctx);
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const OrdersHistoryView()));
            },
            child: const Text('¡Ya transferí! Continuar'),
          ),
        ],
      ),
    );
  }

  void _mostrarDialogoEfectivo(BuildContext context, int ventaId, Map<String, dynamic>? pagoInfo, PaymentController payCtrl) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.payments_outlined, color: Color(0xFF15803D)),
            SizedBox(width: 8),
            Text('Orden en Efectivo Registrada', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Tu orden ha sido reservada para pago en ventanilla.',
              style: TextStyle(fontSize: 13, color: Colors.black87),
            ),
            const SizedBox(height: 10),
            Text(
              'Código de Venta: ORD-$ventaId',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0F172A)),
            ),
            const SizedBox(height: 6),
            const Text(
              'Presenta este código al cajero al momento de recoger tus prendas para realizar el pago en efectivo.',
              style: TextStyle(fontSize: 12, color: Colors.black54),
            ),
          ],
        ),
        actions: [
          OutlinedButton.icon(
            icon: const Icon(Icons.receipt_long, size: 16),
            label: const Text('Ver Comprobante'),
            onPressed: () async {
              final url = payCtrl.getComprobanteHtmlUrl(ventaId);
              await payCtrl.abrirPayPal(url);
            },
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF15803D), foregroundColor: Colors.white),
            onPressed: () {
              Navigator.pop(ctx);
              Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const OrdersHistoryView()));
            },
            child: const Text('Entendido'),
          ),
        ],
      ),
    );
  }
}
