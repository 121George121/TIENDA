// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de Historial de Compras y Pedidos del Cliente (CU15)
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/order_controller.dart';
import '../controllers/auth_controller.dart';
import '../controllers/payment_controller.dart';
import '../models/order_model.dart';

class OrdersHistoryView extends StatefulWidget {
  const OrdersHistoryView({super.key});

  @override
  State<OrdersHistoryView> createState() => _OrdersHistoryViewState();
}

class _OrdersHistoryViewState extends State<OrdersHistoryView> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => _cargarOrdenes());
  }

  void _cargarOrdenes() {
    final authCtrl = Provider.of<AuthController>(context, listen: false);
    final token = authCtrl.currentUser?.token;
    Provider.of<OrderController>(context, listen: false).fetchMisOrdenes(token);
  }

  Widget _buildPurchasedItems(List<OrderItemModel> items) {
    if (items.isEmpty) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 4.0),
        child: Text(
          'Detalle de prendas registrado en el comprobante digital.',
          style: TextStyle(fontSize: 12, color: Colors.grey.shade600, fontStyle: FontStyle.italic),
        ),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 6),
          child: Text(
            'PRENDAS COMPRADAS (${items.length}):',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              letterSpacing: 0.5,
              color: Colors.grey.shade600,
            ),
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: Colors.grey.shade50,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.grey.shade200),
          ),
          child: ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: items.length,
            separatorBuilder: (_, __) => Divider(height: 1, color: Colors.grey.shade200),
            itemBuilder: (context, idx) {
              final it = items[idx];
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    // Miniatura o icono de prenda
                    ClipRRect(
                      borderRadius: BorderRadius.circular(6),
                      child: Container(
                        width: 42,
                        height: 42,
                        color: Colors.white,
                        child: it.imagenUrl != null && it.imagenUrl!.isNotEmpty
                            ? Image.network(
                                it.imagenUrl!,
                                fit: BoxFit.cover,
                                errorBuilder: (_, __, ___) => const Icon(Icons.checkroom, color: Colors.indigo, size: 24),
                              )
                            : const Icon(Icons.checkroom, color: Colors.indigo, size: 24),
                      ),
                    ),
                    const SizedBox(width: 10),
                    // Descripción y variantes
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            it.productoNombre,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF1E293B),
                            ),
                          ),
                          const SizedBox(height: 2),
                          Row(
                            children: [
                              if (it.talla != null && it.talla!.isNotEmpty)
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                                  margin: const EdgeInsets.only(right: 6),
                                  decoration: BoxDecoration(
                                    color: Colors.indigo.shade50,
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: Text(
                                    'Talla: ${it.talla}',
                                    style: TextStyle(fontSize: 10, color: Colors.indigo.shade700, fontWeight: FontWeight.w600),
                                  ),
                                ),
                              if (it.color != null && it.color!.isNotEmpty)
                                Text(
                                  it.color!,
                                  style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    // Cantidad y subtotal
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          '${it.cantidad}x Bs. ${it.precioUnitario.toStringAsFixed(2)}',
                          style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Bs. ${it.subtotal.toStringAsFixed(2)}',
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w700,
                            color: Color(0xFF0F172A),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final orderCtrl = Provider.of<OrderController>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('📦 Mis Pedidos'),
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
        elevation: 1,
      ),
      body: RefreshIndicator(
        onRefresh: () async => _cargarOrdenes(),
        child: orderCtrl.cargando
            ? const Center(child: CircularProgressIndicator())
            : orderCtrl.error != null
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.error_outline, size: 56, color: Colors.red),
                          const SizedBox(height: 12),
                          Text(
                            orderCtrl.error!,
                            textAlign: TextAlign.center,
                            style: const TextStyle(fontSize: 16, color: Colors.black87),
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton.icon(
                            onPressed: _cargarOrdenes,
                            icon: const Icon(Icons.refresh),
                            label: const Text('Reintentar'),
                          )
                        ],
                      ),
                    ),
                  )
                : orderCtrl.ordenes.isEmpty
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.all(32.0),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.receipt_long_outlined, size: 72, color: Colors.grey.shade400),
                              const SizedBox(height: 16),
                              const Text(
                                'Aún no tienes pedidos registrados',
                                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Tus compras online aparecerán aquí con su estado y desglose en tiempo real.',
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 14, color: Colors.grey.shade600),
                              ),
                              const SizedBox(height: 24),
                              ElevatedButton(
                                style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo, foregroundColor: Colors.white),
                                onPressed: () => Navigator.pop(context),
                                child: const Text('Explorar Catálogo'),
                              ),
                            ],
                          ),
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        itemCount: orderCtrl.ordenes.length,
                        itemBuilder: (ctx, index) {
                          final orden = orderCtrl.ordenes[index];
                          final fechaStr = orden.fecha != null
                              ? '${orden.fecha!.day.toString().padLeft(2, '0')}/${orden.fecha!.month.toString().padLeft(2, '0')}/${orden.fecha!.year} ${orden.fecha!.hour.toString().padLeft(2, '0')}:${orden.fecha!.minute.toString().padLeft(2, '0')}'
                              : 'Reciente';

                          return Card(
                            elevation: 2,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                            margin: const EdgeInsets.symmetric(vertical: 8),
                            child: Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                        decoration: BoxDecoration(
                                          color: Colors.indigo.shade50,
                                          borderRadius: BorderRadius.circular(6),
                                        ),
                                        child: Text(
                                          orden.codigoVenta,
                                          style: TextStyle(
                                            fontFamily: 'monospace',
                                            fontWeight: FontWeight.bold,
                                            color: Colors.indigo.shade800,
                                            fontSize: 13,
                                          ),
                                        ),
                                      ),
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                        decoration: BoxDecoration(
                                          color: orden.estado.toUpperCase().contains('ENTREGAD')
                                              ? Colors.green.shade100
                                              : Colors.blue.shade100,
                                          borderRadius: BorderRadius.circular(20),
                                        ),
                                        child: Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            Icon(
                                              orden.estado.toUpperCase().contains('ENTREGAD')
                                                  ? Icons.done_all
                                                  : Icons.check_circle,
                                              size: 14,
                                              color: orden.estado.toUpperCase().contains('ENTREGAD')
                                                  ? Colors.green.shade800
                                                  : Colors.blue.shade800,
                                            ),
                                            const SizedBox(width: 4),
                                            Text(
                                              orden.estado.toUpperCase().contains('ENTREGAD') ? 'Entregado' : 'Comprado',
                                              style: TextStyle(
                                                color: orden.estado.toUpperCase().contains('ENTREGAD')
                                                    ? Colors.green.shade900
                                                    : Colors.blue.shade900,
                                                fontWeight: FontWeight.w700,
                                                fontSize: 12,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 12),
                                  Row(
                                    children: [
                                      Icon(Icons.access_time, size: 16, color: Colors.grey.shade600),
                                      const SizedBox(width: 6),
                                      Text(
                                        fechaStr,
                                        style: TextStyle(fontSize: 13, color: Colors.grey.shade700),
                                      ),
                                      const Spacer(),
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                        decoration: BoxDecoration(
                                          color: Colors.grey.shade200,
                                          borderRadius: BorderRadius.circular(4),
                                        ),
                                        child: Text(
                                          orden.tipoVenta,
                                          style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: Colors.grey.shade800),
                                        ),
                                      )
                                    ],
                                  ),
                                  const SizedBox(height: 14),
                                  // Detalle de Prendas Compradas
                                  _buildPurchasedItems(orden.items),
                                  const Divider(height: 20),
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      const Text(
                                        'Total Pagado:',
                                        style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: Colors.black54),
                                      ),
                                      Text(
                                        'Bs. ${orden.total.toStringAsFixed(2)}',
                                        style: const TextStyle(
                                          fontSize: 18,
                                          fontWeight: FontWeight.w800,
                                          color: Colors.indigo,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 10),
                                  SizedBox(
                                    width: double.infinity,
                                    child: OutlinedButton.icon(
                                      style: OutlinedButton.styleFrom(
                                        foregroundColor: Colors.indigo.shade800,
                                        side: BorderSide(color: Colors.indigo.shade200),
                                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                      ),
                                      icon: const Icon(Icons.receipt_long, size: 16),
                                      label: const Text('Ver Recibo Oficial (PDF / QR)', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                                      onPressed: () async {
                                        final payCtrl = Provider.of<PaymentController>(context, listen: false);
                                        final url = payCtrl.getComprobanteHtmlUrl(orden.id);
                                        await payCtrl.abrirPayPal(url);
                                      },
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
      ),
    );
  }
}
