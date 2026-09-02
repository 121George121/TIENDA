// ==============================================================================
// CAPA MODELO (MVC - MODEL EN FLUTTER / DART)
// Modelo del Item dentro del Carrito de Compras Móvil
// ==============================================================================

import 'product_model.dart';

class CartItemModel {
  final ProductModel product;
  int cantidad;

  CartItemModel({
    required this.product,
    this.cantidad = 1,
  });

  double get subtotal => product.precio * cantidad;
}
