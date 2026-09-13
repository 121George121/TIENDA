// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de la Interfaz de Usuario para Revisar Carrito y Confirmar Pedido
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/cart_controller.dart';
import '../controllers/auth_controller.dart';

class CartView extends StatelessWidget {
  const CartView({super.key});

  @override
  Widget build(BuildContext context) {
    final cartCtrl = Provider.of<CartController>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('🛒 Tu Carrito de Compras'),
        backgroundColor: Colors.indigo,
      ),
      body: cartCtrl.items.isEmpty
          ? const Center(child: Text('El carrito está vacío', style: TextStyle(fontSize: 18)))
          : Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: cartCtrl.items.length,
                    itemBuilder: (ctx, i) {
                      final item = cartCtrl.items.values.toList()[i];
                      return ListTile(
                        title: Text(item.product.nombre),
                        subtitle: Text('Cantidad: ${item.cantidad} x \$${item.product.precio}'),
                        trailing: Text(
                          '\$${item.subtotal.toStringAsFixed(2)}',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                        ),
                      );
                    },
                  ),
                ),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.grey[200],
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('TOTAL:', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                          Text(
                            '\$${cartCtrl.totalMonto.toStringAsFixed(2)}',
                            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.green),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            padding: const EdgeInsets.symmetric(vertical: 14),
                          ),
                          onPressed: () async {
                            final authCtrl = Provider.of<AuthController>(context, listen: false);
                            if (!authCtrl.isLoggedIn || authCtrl.currentUser?.token == null) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('Debes iniciar sesión para confirmar tu compra.'),
                                  backgroundColor: Colors.orange,
                                )
                              );
                              Navigator.pushNamed(context, '/login');
                              return;
                            }

                            bool exito = await cartCtrl.procesarCompra(
                              "Av. Principal #123, Santa Cruz",
                              authToken: authCtrl.currentUser?.token
                            );
                            if (!context.mounted) return;
                            if (exito) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('¡Pedido realizado con éxito!'),
                                  backgroundColor: Colors.green,
                                )
                              );
                              Navigator.pop(context);
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('No se pudo procesar la orden. Verifica tu sesión o stock.'),
                                  backgroundColor: Colors.red,
                                )
                              );
                            }
                          },
                          child: const Text('Confirmar Pedido', style: TextStyle(fontSize: 16)),
                        ),
                      )
                    ],
                  ),
                )
              ],
            ),
    );
  }
}
