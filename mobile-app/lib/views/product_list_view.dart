// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de la Interfaz de Usuario para mostrar el catálogo móvil
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/product_controller.dart';
import '../controllers/cart_controller.dart';
import '../controllers/auth_controller.dart';

class ProductListView extends StatefulWidget {
  const ProductListView({super.key});

  @override
  State<ProductListView> createState() => _ProductListViewState();
}

class _ProductListViewState extends State<ProductListView> {
  @override
  void initState() {
    super.initState();
    // 1. Invoca al Controlador para obtener los datos desde FastAPI al cargar la pantalla
    Future.microtask(() {
      if (mounted) {
        Provider.of<ProductController>(context, listen: false).fetchProductos();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final productCtrl = Provider.of<ProductController>(context);
    final cartCtrl = Provider.of<CartController>(context);
    final authCtrl = Provider.of<AuthController>(context, listen: false);

    return Scaffold(
      appBar: AppBar(
        title: const Text('🛍️ E-Commerce Móvil'),
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
        actions: [
          Stack(
            alignment: Alignment.center,
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_cart),
                onPressed: () {
                  // Navegar a la Vista del Carrito
                  Navigator.pushNamed(context, '/cart');
                },
              ),
              if (cartCtrl.totalItemCount > 0)
                Positioned(
                  right: 8,
                  top: 8,
                  child: CircleAvatar(
                    radius: 9,
                    backgroundColor: Colors.red,
                    child: Text(
                      '${cartCtrl.totalItemCount}',
                      style: const TextStyle(fontSize: 11, color: Colors.white),
                    ),
                  ),
                )
            ],
          ),
          IconButton(
            icon: const Icon(Icons.receipt_long),
            tooltip: 'Mis Pedidos',
            onPressed: () {
              Navigator.pushNamed(context, '/orders');
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Cerrar Sesión',
            onPressed: () {
              authCtrl.logout();
              cartCtrl.limpiarCarrito();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Sesión cerrada correctamente'),
                  duration: Duration(seconds: 2),
                ),
              );
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: productCtrl.cargando
          ? const Center(child: CircularProgressIndicator())
          : productCtrl.error != null
              ? Center(child: Text(productCtrl.error!))
              : ListView.builder(
                  padding: const EdgeInsets.all(12),
                  itemCount: productCtrl.productos.length,
                  itemBuilder: (ctx, i) {
                    final prod = productCtrl.productos[i];
                    return Card(
                      elevation: 3,
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      child: ListTile(
                        leading: (prod.imagenUrl != null && prod.imagenUrl!.isNotEmpty)
                            ? Image.network(
                                prod.imagenUrl!,
                                width: 50,
                                height: 50,
                                fit: BoxFit.cover,
                                errorBuilder: (ctx, err, stack) => const Icon(Icons.checkroom, size: 40, color: Colors.indigo),
                              )
                            : const Icon(Icons.checkroom, size: 40, color: Colors.indigo),
                        title: Text(prod.nombre, style: const TextStyle(fontWeight: FontWeight.bold)),
                        subtitle: Text('\$${prod.precio.toStringAsFixed(2)} | Stock: ${prod.stock}'),
                        trailing: ElevatedButton(
                          style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo),
                          onPressed: prod.stock > 0
                              ? () {
                                  cartCtrl.agregarProducto(prod);
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text('${prod.nombre} añadido al carrito'),
                                      duration: const Duration(seconds: 1),
                                    )
                                  );
                                }
                              : null,
                          child: const Text('Agregar'),
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
