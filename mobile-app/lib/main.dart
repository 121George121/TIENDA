// ==============================================================================
// ENTRY POINT - FLUTTER / DART MOBILE APPLICATION
// Integración del Patrón MVC con Providers de Estado
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'controllers/product_controller.dart';
import 'controllers/cart_controller.dart';
import 'views/product_list_view.dart';
import 'views/cart_view.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ProductController()),
        ChangeNotifierProvider(create: (_) => CartController()),
      ],
      child: const ECommerceMobileApp(),
    ),
  );
}

class ECommerceMobileApp extends StatelessWidget {
  const ECommerceMobileApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'E-Commerce Mobile MVC',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const ProductListView(),
        '/cart': (context) => const CartView(),
      },
    );
  }
}
