import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatBadgeModule } from '@angular/material/badge';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

import { CompraDigitalService } from '../../../services/cu15_realizar_compras_digitales/compra-digital.service';
import { CompraDigitalController } from '../../../controllers/cu15_realizar_compras_digitales/compra-digital.controller';
import { CarritoCheckoutDialogComponent } from '../carrito-checkout-dialog/carrito-checkout-dialog.component';

@Component({
  selector: 'app-tienda-online',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatBadgeModule,
    MatProgressBarModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './tienda-online.component.html',
  styleUrls: ['./tienda-online.component.css']
})
export class TiendaOnlineComponent implements OnInit {
  productos: any[] = [];
  productosFiltrados: any[] = [];
  loading = true;
  searchControl = new FormControl('');

  tallasDisponibles: string[] = ['S', 'M', 'L', 'XL'];
  tallaSeleccionadaMap: { [prodId: number]: string } = {};

  constructor(
    private service: CompraDigitalService,
    public cartCtrl: CompraDigitalController,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarCatalogo();

    this.searchControl.valueChanges
      .pipe(debounceTime(250), distinctUntilChanged())
      .subscribe(term => this.filtrar(term || ''));
  }

  cargarCatalogo(): void {
    this.loading = true;
    this.service.getProductos().subscribe({
      next: (prods) => {
        this.productos = prods;
        this.productosFiltrados = prods;
        prods.forEach(p => {
          this.tallaSeleccionadaMap[p.id] = 'M';
        });
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar catálogo:', err);
        this.loading = false;
      }
    });
  }

  filtrar(term: string): void {
    const q = term.toLowerCase().trim();
    if (!q) {
      this.productosFiltrados = [...this.productos];
    } else {
      this.productosFiltrados = this.productos.filter(p =>
        p.nombre.toLowerCase().includes(q) ||
        (p.descripcion && p.descripcion.toLowerCase().includes(q))
      );
    }
  }

  selectTalla(prodId: number, talla: string): void {
    this.tallaSeleccionadaMap[prodId] = talla;
  }

  agregar(producto: any): void {
    const talla = this.tallaSeleccionadaMap[producto.id] || 'M';
    this.cartCtrl.addToCart(producto, 1, talla, 'Negro');
    this.snackBar.open(`¡${producto.nombre} (${talla}) añadido a tu bolsa!`, 'Ver Bolsa', { duration: 2500 })
      .onAction().subscribe(() => this.abrirCarrito());
  }

  abrirCarrito(): void {
    this.dialog.open(CarritoCheckoutDialogComponent, {
      width: '620px'
    });
  }

  irAMisPedidos(): void {
    this.router.navigate(['/tienda/mis-pedidos']);
  }

  volverAlPanel(): void {
    this.router.navigate(['/admin/users']);
  }
}
