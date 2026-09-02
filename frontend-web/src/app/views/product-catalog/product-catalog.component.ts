import { Component, OnInit } from '@angular/core';
import { ProductControllerService } from '../../controllers/product.service';
import { Producto } from '../../models/product.model';
import { CartItem } from '../../models/cart.model';

@Component({
  selector: 'app-product-catalog',
  templateUrl: './product-catalog.component.html',
  styleUrls: ['./product-catalog.component.css']
})
export class ProductCatalogComponent implements OnInit {
  productos: Producto[] = [];
  cartItems: CartItem[] = [];
  loading = true;

  constructor(private productController: ProductControllerService) {}

  ngOnInit(): void {
    // 1. Cargar productos desde el Controlador
    this.productController.getProductos().subscribe({
      next: (data) => {
        this.productos = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al conectar con la API:', err);
        this.loading = false;
      }
    });

    // 2. Suscribirse a los cambios del carrito
    this.productController.cartItems$.subscribe(items => {
      this.cartItems = items;
    });
  }

  agregarAlCarrito(producto: Producto): void {
    this.productController.addToCart(producto);
  }

  get totalItems(): number {
    return this.cartItems.reduce((acc, item) => acc + item.cantidad, 0);
  }

  get totalPrice(): number {
    return this.cartItems.reduce((acc, item) => acc + item.subtotal, 0);
  }
}
