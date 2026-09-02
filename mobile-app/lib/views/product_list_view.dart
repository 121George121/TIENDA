// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de la Interfaz de Usuario para mostrar el catálogo móvil
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/product_controller.dart';
import '../controllers/cart_controller.dart';

class ProductListView extends StatefulWidget {
  const ProductListView({Key? key}) : super(key: key);

  @override
  State<ProductListView> createState() => _ProductListViewState();
}

class _ProductListViewState extends State<ProductListView> {
  @override
  void initState() {
    super.initState();
    // 1. Invoca al Controlador para obtener los datos desde FastAPI al cargar la pantalla
    Future.microtask(() =>
      Provider.of<ProductController>(context, listen: false).fetchProductos()
    );
  }

  @override
  Widget build(BuildContext context) {
    final productCtrl = Provider.of<ProductController>(context);
    final cartCtrl = Provider.of<CartController>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('🛍️ E-Commerce Móvil (Flutter)'),
        backgroundColor: Colors.indigo,
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
          )
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
                        leading: prod.imagenUrl != null
                            ? Image.network(prod.imagenUrl!, width: 50, fit: CoverBox.fitWidth)
                            : const Icon(Icons.shopping_bag, size: 40),
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
