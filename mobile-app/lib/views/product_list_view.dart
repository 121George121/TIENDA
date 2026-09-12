// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de Catálogo y Disponibilidad de Inventario (CU08)
// Ubicación: mobile-app/lib/views/product_list_view.dart
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/product_controller.dart';
import '../controllers/cart_controller.dart';
import '../controllers/auth_controller.dart';
import '../models/inventory_model.dart';
import '../models/product_model.dart';

class ProductListView extends StatefulWidget {
  const ProductListView({Key? key}) : super(key: key);

  @override
  State<ProductListView> createState() => _ProductListViewState();
}

class _ProductListViewState extends State<ProductListView> {
  final TextEditingController _searchCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      if (mounted) {
        context.read<ProductController>().fetchProductos();
      }
    });
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final productCtrl = Provider.of<ProductController>(context);
    final cartCtrl = Provider.of<CartController>(context);
    final authCtrl = Provider.of<AuthController>(context, listen: false);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Boutique Retail (CU08)'),
        backgroundColor: const Color(0xFF0F172A),
        foregroundColor: Colors.white,
        elevation: 2,
        actions: [
          Stack(
            alignment: Alignment.center,
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_bag_outlined),
                onPressed: () {
                  Navigator.pushNamed(context, '/cart');
                },
              ),
              if (cartCtrl.totalItemCount > 0)
                Positioned(
                  right: 8,
                  top: 8,
                  child: CircleAvatar(
                    radius: 9,
                    backgroundColor: const Color(0xFF38BDF8),
                    child: Text(
                      '${cartCtrl.totalItemCount}',
                      style: const TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                  ),
                )
            ],
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Cerrar Sesión',
            onPressed: () {
              authCtrl.logout();
              cartCtrl.limpiarCarrito();
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Banner Selector de Sucursal Física (CU08)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            color: const Color(0xFF1E293B),
            child: Row(
              children: [
                const Icon(Icons.storefront, color: Color(0xFF38BDF8), size: 24),
                const SizedBox(width: 10),
                const Text(
                  'Tienda:',
                  style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<int>(
                      dropdownColor: const Color(0xFF1E293B),
                      value: productCtrl.sucursalSeleccionadaId,
                      icon: const Icon(Icons.keyboard_arrow_down, color: Color(0xFF38BDF8)),
                      isExpanded: true,
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                      items: productCtrl.sucursales.map((b) {
                        return DropdownMenuItem<int>(
                          value: b.id,
                          child: Text('${b.nombre} (${b.ciudad})', overflow: TextOverflow.ellipsis),
                        );
                      }).toList(),
                      onChanged: (newId) {
                        productCtrl.seleccionarSucursal(newId);
                      },
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Barra de Búsqueda
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 6),
            child: TextField(
              controller: _searchCtrl,
              decoration: InputDecoration(
                hintText: 'Buscar poleras, modelos, marcas...',
                prefixIcon: const Icon(Icons.search, color: Colors.grey),
                suffixIcon: _searchCtrl.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _searchCtrl.clear();
                          productCtrl.fetchCatalogoConDisponibilidad(search: '');
                        },
                      )
                    : null,
                filled: true,
                fillColor: Colors.white,
                contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                ),
              ),
              onSubmitted: (term) {
                productCtrl.fetchCatalogoConDisponibilidad(search: term);
              },
            ),
          ),

          // Lista de Productos con Disponibilidad
          Expanded(
            child: productCtrl.cargando
                ? const Center(child: CircularProgressIndicator())
                : productCtrl.error != null
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.cloud_off, size: 48, color: Colors.grey),
                            const SizedBox(height: 12),
                            Text(productCtrl.error!, textAlign: TextAlign.center),
                            const SizedBox(height: 12),
                            ElevatedButton(
                              onPressed: () => productCtrl.fetchProductos(),
                              child: const Text('Reintentar'),
                            )
                          ],
                        ),
                      )
                    : productCtrl.catalogo.isEmpty
                        ? const Center(
                            child: Text('No hay productos disponibles con estos filtros.'),
                          )
                        : ListView.builder(
                            padding: const EdgeInsets.all(12),
                            itemCount: productCtrl.catalogo.length,
                            itemBuilder: (ctx, i) {
                              final prod = productCtrl.catalogo[i];
                              return _buildProductCard(context, prod, cartCtrl);
                            },
                          ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductCard(BuildContext context, CatalogProductModel prod, CartController cartCtrl) {
    bool enStock = prod.stockSucursal > 0;

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Imagen del Producto
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: prod.imagenprincipal != null
                  ? Image.network(
                      prod.imagenprincipal!,
                      width: 90,
                      height: 105,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => Container(
                        width: 90,
                        height: 105,
                        color: Colors.grey[200],
                        child: const Icon(Icons.image_not_supported, color: Colors.grey),
                      ),
                    )
                  : Container(
                      width: 90,
                      height: 105,
                      color: Colors.grey[200],
                      child: const Icon(Icons.checkroom, size: 40, color: Colors.grey),
                    ),
            ),
            const SizedBox(width: 14),

            // Detalles y Stock
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (prod.marca != null)
                    Text(
                      prod.marca!.toUpperCase(),
                      style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 0.5,
                        color: Colors.grey[600],
                      ),
                    ),
                  Text(
                    prod.nombre,
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Bs. ${prod.preciobase.toStringAsFixed(2)}',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w800,
                      color: Color(0xFF0F172A),
                    ),
                  ),
                  const SizedBox(height: 6),

                  // Badge de disponibilidad por tienda
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(
                      color: enStock ? const Color(0xFFDCFCE7) : const Color(0xFFFEE2E2),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          enStock ? Icons.check_circle : Icons.cancel,
                          size: 14,
                          color: enStock ? const Color(0xFF16A34A) : const Color(0xFFDC2626),
                        ),
                        const SizedBox(width: 4),
                        Text(
                          enStock
                              ? 'Stock en tienda: ${prod.stockSucursal} uds'
                              : 'Agotado en esta tienda',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: enStock ? const Color(0xFF16A34A) : const Color(0xFFDC2626),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Botón Agregar al Carrito
                  Align(
                    alignment: Alignment.centerRight,
                    child: SizedBox(
                      height: 34,
                      child: ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF0F172A),
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                        ),
                        icon: const Icon(Icons.add_shopping_cart, size: 16),
                        label: Text(enStock ? 'Agregar' : 'Sin stock', style: const TextStyle(fontSize: 12)),
                        onPressed: enStock
                            ? () {
                                final pmodel = ProductModel(
                                  id: prod.id,
                                  nombre: prod.nombre,
                                  descripcion: prod.descripcion,
                                  precio: prod.preciobase,
                                  stock: prod.stockSucursal,
                                  activo: prod.disponible,
                                );
                                cartCtrl.agregarProducto(pmodel);
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    content: Text('${prod.nombre} añadido al carrito'),
                                    duration: const Duration(milliseconds: 900),
                                    backgroundColor: const Color(0xFF0F172A),
                                  ),
                                );
                              }
                            : null,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
