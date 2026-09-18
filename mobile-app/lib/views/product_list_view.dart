// ==============================================================================
// CAPA VISTA (MVC - VIEW EN FLUTTER / DART)
// Pantalla de Catálogo y Disponibilidad de Inventario Multitienda (CU08 & CU15)
// Ubicación: mobile-app/lib/views/product_list_view.dart
// ==============================================================================

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/product_controller.dart';
import '../controllers/cart_controller.dart';
import '../controllers/auth_controller.dart';
import '../controllers/notification_controller.dart';
import '../models/product_model.dart';
import '../models/inventory_model.dart';
import 'my_reservations_view.dart';
import 'orders_history_view.dart';
import 'virtual_fitting_room_view.dart';

class ProductListView extends StatefulWidget {
  const ProductListView({super.key});

  @override
  State<ProductListView> createState() => _ProductListViewState();
}

class _ProductListViewState extends State<ProductListView> {
  final TextEditingController _searchCtrl = TextEditingController();
  Timer? _debounceTimer;

  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      if (mounted) {
        context.read<ProductController>().fetchProductos();
        final auth = context.read<AuthController>();
        context.read<NotificationController>().fetchNotificaciones(auth.currentUser?.token);
      }
    });
  }

  @override
  void dispose() {
    _debounceTimer?.cancel();
    _searchCtrl.dispose();
    super.dispose();
  }

  void _onSearchChanged(String query) {
    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 350), () {
      if (mounted) {
        context.read<ProductController>().fetchCatalogoConDisponibilidad(search: query);
      }
    });
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
          // Botón Notificaciones con Contador (CU19)
          Consumer<NotificationController>(
            builder: (ctx, notifCtrl, _) {
              return Stack(
                alignment: Alignment.center,
                children: [
                  IconButton(
                    icon: const Icon(Icons.notifications_none),
                    tooltip: 'Notificaciones (CU19)',
                    onPressed: () => _mostrarNotificacionesSheet(context),
                  ),
                  if (notifCtrl.noLeidasCount > 0)
                    Positioned(
                      right: 6,
                      top: 6,
                      child: CircleAvatar(
                        radius: 8,
                        backgroundColor: Colors.redAccent,
                        child: Text(
                          '${notifCtrl.noLeidasCount}',
                          style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                      ),
                    ),
                ],
              );
            },
          ),

          // Botón Carrito con Contador
          Stack(
            alignment: Alignment.center,
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_bag_outlined),
                tooltip: 'Carrito de Compras',
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

          // Botón Mis Reservas (CU10)
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

          // Botón Mis Pedidos Digitales (CU15)
          IconButton(
            icon: const Icon(Icons.receipt_long),
            tooltip: 'Mis Pedidos (CU15)',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const OrdersHistoryView()),
              );
            },
          ),

          // Botón Cerrar Sesión
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
              onChanged: _onSearchChanged,
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
                              final bool enStock = prod.disponible && prod.stockSucursal > 0;

                              return Card(
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                                elevation: 2,
                                margin: const EdgeInsets.symmetric(vertical: 7),
                                child: Padding(
                                  padding: const EdgeInsets.all(12),
                                  child: Row(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      // Imagen del producto
                                      ClipRRect(
                                        borderRadius: BorderRadius.circular(10),
                                        child: (prod.imagenprincipal != null && prod.imagenprincipal!.isNotEmpty)
                                            ? Image.network(
                                                prod.imagenprincipal!,
                                                width: 85,
                                                height: 95,
                                                fit: BoxFit.cover,
                                                errorBuilder: (_, __, ___) => Container(
                                                  width: 85,
                                                  height: 95,
                                                  color: Colors.grey[200],
                                                  child: const Icon(Icons.checkroom, size: 40, color: Colors.grey),
                                                ),
                                              )
                                            : Container(
                                                width: 85,
                                                height: 95,
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
                                            const SizedBox(height: 10),

                                            // Botones de Acción: CU12 (Vestidor Virtual), CU08 (Otras tiendas) y Agregar
                                            Wrap(
                                              alignment: WrapAlignment.end,
                                              crossAxisAlignment: WrapCrossAlignment.center,
                                              spacing: 6,
                                              runSpacing: 6,
                                              children: [
                                                // Botón CU12: Vestidor Virtual
                                                SizedBox(
                                                  height: 32,
                                                  child: OutlinedButton.icon(
                                                    style: OutlinedButton.styleFrom(
                                                      padding: const EdgeInsets.symmetric(horizontal: 7),
                                                      side: const BorderSide(color: Color(0xFF6366F1), width: 1.2),
                                                      foregroundColor: const Color(0xFF4F46E5),
                                                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                                    ),
                                                    icon: const Icon(Icons.checkroom, size: 13, color: Color(0xFF4F46E5)),
                                                    label: const Text('Vestidor', style: TextStyle(fontSize: 10.5, fontWeight: FontWeight.bold)),
                                                    onPressed: () {
                                                      final pmodel = ProductModel(
                                                        id: prod.id,
                                                        nombre: prod.nombre,
                                                        descripcion: prod.descripcion,
                                                        precio: prod.preciobase,
                                                        stock: prod.stockSucursal,
                                                        imagenUrl: prod.imagenprincipal,
                                                        activo: prod.disponible,
                                                      );
                                                      Navigator.push(
                                                        context,
                                                        MaterialPageRoute(
                                                          builder: (_) => VirtualFittingRoomView(producto: pmodel),
                                                        ),
                                                      );
                                                    },
                                                  ),
                                                ),

                                                // Botón Consultar Otras Tiendas
                                                SizedBox(
                                                  height: 32,
                                                  child: OutlinedButton.icon(
                                                    style: OutlinedButton.styleFrom(
                                                      padding: const EdgeInsets.symmetric(horizontal: 7),
                                                      side: const BorderSide(color: Color(0xFFCBD5E1)),
                                                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                                    ),
                                                    icon: const Icon(Icons.storefront, size: 13, color: Color(0xFF0F172A)),
                                                    label: const Text('Tiendas', style: TextStyle(fontSize: 10.5, color: Color(0xFF0F172A))),
                                                    onPressed: () => _mostrarDisponibilidadModal(context, prod),
                                                  ),
                                                ),

                                                // Botón Agregar
                                                SizedBox(
                                                  height: 32,
                                                  child: ElevatedButton.icon(
                                                    style: ElevatedButton.styleFrom(
                                                      backgroundColor: const Color(0xFF0F172A),
                                                      foregroundColor: Colors.white,
                                                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                                      padding: const EdgeInsets.symmetric(horizontal: 8),
                                                    ),
                                                    icon: const Icon(Icons.add_shopping_cart, size: 13),
                                                    label: Text(enStock ? 'Agregar' : 'Agotado', style: const TextStyle(fontSize: 10.5)),
                                                    onPressed: enStock
                                                        ? () {
                                                            final pmodel = ProductModel(
                                                              id: prod.id,
                                                              nombre: prod.nombre,
                                                              descripcion: prod.descripcion,
                                                              precio: prod.preciobase,
                                                              stock: prod.stockSucursal,
                                                              imagenUrl: prod.imagenprincipal,
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
        ],
      ),
    );
  }

  /// CU08: Modal interactivo que consulta la disponibilidad multitienda en tiempo real
  void _mostrarDisponibilidadModal(BuildContext context, CatalogProductModel prod) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return Container(
          height: MediaQuery.of(context).size.height * 0.72,
          decoration: const BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
          ),
          child: Column(
            children: [
              Container(
                margin: const EdgeInsets.only(top: 12, bottom: 8),
                width: 40,
                height: 5,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                child: Row(
                  children: [
                    const Icon(Icons.storefront, color: Color(0xFF0F172A), size: 26),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            prod.nombre,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const Text(
                            'Disponibilidad en Tiendas Físicas (CU08)',
                            style: TextStyle(fontSize: 12, color: Colors.grey),
                          ),
                        ],
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close),
                      onPressed: () => Navigator.pop(ctx),
                    ),
                  ],
                ),
              ),
              const Divider(height: 1),
              Expanded(
                child: FutureBuilder<ProductAvailabilityModel?>(
                  future: context.read<ProductController>().fetchDisponibilidadProducto(prod.id),
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator());
                    }
                    if (snapshot.hasError || snapshot.data == null) {
                      return const Center(
                        child: Text('No se pudo cargar la disponibilidad en otras tiendas.'),
                      );
                    }
                    final disp = snapshot.data!;
                    return ListView.separated(
                      padding: const EdgeInsets.all(16),
                      itemCount: disp.sucursales.length,
                      separatorBuilder: (_, __) => const SizedBox(height: 12),
                      itemBuilder: (context, index) {
                        final suc = disp.sucursales[index];
                        final bool hasStock = suc.stockTotal > 0;
                        return Container(
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: const Color(0xFFF8FAFC),
                            borderRadius: BorderRadius.circular(14),
                            border: Border.all(
                              color: hasStock ? const Color(0xFFCBD5E1) : const Color(0xFFF1F5F9),
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Expanded(
                                    child: Row(
                                      children: [
                                        Icon(
                                          Icons.store,
                                          size: 18,
                                          color: hasStock ? const Color(0xFF0F172A) : Colors.grey,
                                        ),
                                        const SizedBox(width: 8),
                                        Expanded(
                                          child: Text(
                                            '${suc.sucursalNombre} (${suc.ciudad ?? "Bolivia"})',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              fontSize: 14,
                                              color: hasStock ? const Color(0xFF0F172A) : Colors.grey,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: hasStock ? const Color(0xFFDCFCE7) : const Color(0xFFFEE2E2),
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: Text(
                                      hasStock ? '${suc.stockTotal} disponibles' : 'Agotado',
                                      style: TextStyle(
                                        fontSize: 12,
                                        fontWeight: FontWeight.bold,
                                        color: hasStock ? const Color(0xFF16A34A) : const Color(0xFFDC2626),
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              if (suc.direccion != null) ...[
                                const SizedBox(height: 4),
                                Text(
                                  suc.direccion!,
                                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                                ),
                              ],
                              if (hasStock && suc.variantes.isNotEmpty) ...[
                                const SizedBox(height: 10),
                                Wrap(
                                  spacing: 6,
                                  runSpacing: 6,
                                  children: suc.variantes.where((v) => v.stock > 0).map((v) {
                                    return Chip(
                                      labelPadding: const EdgeInsets.symmetric(horizontal: 4),
                                      visualDensity: VisualDensity.compact,
                                      label: Text(
                                        '${v.talla ?? "M"} - ${v.color ?? "Color"} (${v.stock} uds)',
                                        style: const TextStyle(fontSize: 11),
                                      ),
                                      backgroundColor: Colors.white,
                                      side: const BorderSide(color: Color(0xFFE2E8F0)),
                                    );
                                  }).toList(),
                                ),
                              ],
                            ],
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _mostrarNotificacionesSheet(BuildContext context) {
    final notifCtrl = Provider.of<NotificationController>(context, listen: false);
    final auth = Provider.of<AuthController>(context, listen: false);
    notifCtrl.fetchNotificaciones(auth.currentUser?.token);

    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return Consumer<NotificationController>(
          builder: (_, ctrl, __) {
            return Container(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.notifications, color: Color(0xFF0F172A)),
                          SizedBox(width: 8),
                          Text('Notificaciones (CU19)', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      if (ctrl.notificaciones.isNotEmpty)
                        TextButton(
                          onPressed: () => ctrl.marcarTodasLeidas(auth.currentUser?.token),
                          child: const Text('Marcar leídas', style: TextStyle(fontSize: 12)),
                        ),
                    ],
                  ),
                  const Divider(),
                  if (ctrl.cargando)
                    const Center(child: Padding(padding: EdgeInsets.all(20), child: CircularProgressIndicator()))
                  else if (ctrl.notificaciones.isEmpty)
                    const Padding(
                      padding: EdgeInsets.all(30),
                      child: Center(
                        child: Text('No tienes notificaciones pendientes', style: TextStyle(color: Colors.grey)),
                      ),
                    )
                  else
                    Flexible(
                      child: ListView.builder(
                        shrinkWrap: true,
                        itemCount: ctrl.notificaciones.length,
                        itemBuilder: (_, i) {
                          final n = ctrl.notificaciones[i];
                          return ListTile(
                            contentPadding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                            leading: CircleAvatar(
                              backgroundColor: n.tipo == 'RESERVA_EXPIRANDO'
                                  ? Colors.orange.shade100
                                  : (n.tipo == 'STOCK_CRITICO' ? Colors.red.shade100 : Colors.blue.shade100),
                              child: Icon(
                                n.tipo == 'RESERVA_EXPIRANDO'
                                    ? Icons.timer
                                    : (n.tipo == 'STOCK_CRITICO' ? Icons.warning : Icons.info_outline),
                                color: n.tipo == 'RESERVA_EXPIRANDO'
                                    ? Colors.orange.shade900
                                    : (n.tipo == 'STOCK_CRITICO' ? Colors.red.shade900 : Colors.blue.shade900),
                                size: 20,
                              ),
                            ),
                            title: Text(n.titulo, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                            subtitle: Text(n.mensaje, style: const TextStyle(fontSize: 12)),
                            trailing: Text(n.fecha, style: const TextStyle(fontSize: 10, color: Colors.grey)),
                            onTap: () {
                              ctrl.marcarLeida(n.id, auth.currentUser?.token);
                              Navigator.pop(ctx);
                              if (n.enlace == '/mis-reservas') {
                                Navigator.push(context, MaterialPageRoute(builder: (_) => const MyReservationsView()));
                              } else if (n.enlace == '/mis-pedidos') {
                                Navigator.push(context, MaterialPageRoute(builder: (_) => const OrdersHistoryView()));
                              }
                            },
                          );
                        },
                      ),
                    ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}
