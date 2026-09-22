// ==============================================================================
// ENTRY POINT - FLUTTER / DART MOBILE APPLICATION
// Integración del Patrón MVC con Providers de Estado
// ==============================================================================

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'controllers/auth_controller.dart';
import 'controllers/product_controller.dart';
import 'controllers/cart_controller.dart';
import 'controllers/order_controller.dart';
import 'controllers/reservation_controller.dart';
import 'controllers/payment_controller.dart';
import 'controllers/notification_controller.dart';
import 'controllers/recommendation_controller.dart';
import 'views/login_view.dart';
import 'views/register_view.dart';
import 'views/recover_password_view.dart';
import 'views/reset_password_view.dart';
import 'views/product_list_view.dart';
import 'views/cart_view.dart';
import 'views/orders_history_view.dart';
import 'views/my_reservations_view.dart';

void main() {
  runApp(const ECommerceMobileApp());
}

class ECommerceMobileApp extends StatelessWidget {
  const ECommerceMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthController()),
        ChangeNotifierProvider(create: (_) => ProductController()),
        ChangeNotifierProvider(create: (_) => CartController()),
        ChangeNotifierProvider(create: (_) => OrderController()),
        ChangeNotifierProvider(create: (_) => ReservationController()),
        ChangeNotifierProvider(create: (_) => PaymentController()),
        ChangeNotifierProvider(create: (_) => NotificationController()),
        ChangeNotifierProvider(create: (_) => RecommendationController()),
      ],
      child: MaterialApp(
        title: 'Shopyn Golden Store',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorSchemeSeed: const Color(0xFFE11D48),
          useMaterial3: true,
          fontFamily: 'Roboto',
        ),
        initialRoute: '/login',
        routes: {
          '/login': (context) => const LoginView(),
          '/register': (context) => const RegisterView(),
          '/recover-password': (context) => const RecoverPasswordView(),
          '/reset-password': (context) => const ResetPasswordView(),
          '/': (context) => const ProductListView(),
          '/cart': (context) => const CartView(),
          '/orders': (context) => const OrdersHistoryView(),
          '/reservas': (context) => const MyReservationsView(),
        },
      ),
    );
  }
}
