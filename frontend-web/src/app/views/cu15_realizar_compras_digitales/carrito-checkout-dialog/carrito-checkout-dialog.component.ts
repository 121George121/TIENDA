import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

import { CompraDigitalController, CartWebItem } from '../../../controllers/cu15_realizar_compras_digitales/compra-digital.controller';
import { SucursalController } from '../../../controllers/cu4_gestionar_sucursales/sucursal.controller';
import { Sucursal } from '../../../models/cu4_gestionar_sucursales/sucursal.model';
import { OrdenResponseDTO } from '../../../services/cu15_realizar_compras_digitales/compra-digital.service';

@Component({
  selector: 'app-carrito-checkout-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatDividerModule,
    MatProgressBarModule,
    MatSnackBarModule
  ],
  templateUrl: './carrito-checkout-dialog.component.html',
  styleUrls: ['./carrito-checkout-dialog.component.css']
})
export class CarritoCheckoutDialogComponent implements OnInit {
  form!: FormGroup;
  sucursales: Sucursal[] = [];
  procesando = false;
  ordenConfirmada?: OrdenResponseDTO;

  constructor(
    private fb: FormBuilder,
    public cartCtrl: CompraDigitalController,
    private sucursalCtrl: SucursalController,
    public dialogRef: MatDialogRef<CarritoCheckoutDialogComponent>,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      direccion: ['Av. Principal #450, Barrio Equipetrol', [Validators.required, Validators.minLength(5)]],
      sucursal_id: [null, [Validators.required]],
      metodo_pago: ['Pago Online / Tarjeta de Débito', [Validators.required]]
    });

    this.sucursalCtrl.sucursales$.subscribe(sucursales => {
      this.sucursales = sucursales;
      if (sucursales.length > 0 && !this.form.get('sucursal_id')?.value) {
        this.form.patchValue({ sucursal_id: sucursales[0].id });
      }
    });

    this.sucursalCtrl.loadSucursales();
  }

  increment(item: CartWebItem): void {
    this.cartCtrl.updateQuantity(item, 1);
  }

  decrement(item: CartWebItem): void {
    this.cartCtrl.updateQuantity(item, -1);
  }

  remove(item: CartWebItem): void {
    this.cartCtrl.removeFromCart(item);
  }

  confirmarCompra(): void {
    if (this.cartCtrl.cart.length === 0) {
      this.snackBar.open('La bolsa de compra está vacía', 'Cerrar', { duration: 3000 });
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.procesando = true;
    const { direccion, sucursal_id } = this.form.value;

    this.cartCtrl.procesarOrden(direccion, sucursal_id).subscribe({
      next: (orden) => {
        this.procesando = false;
        this.ordenConfirmada = orden;
        this.snackBar.open('¡Compra digital confirmada con éxito!', 'Genial', { duration: 4000 });
      },
      error: (err) => {
        this.procesando = false;
        const msg = err.error?.detail || 'Error al procesar la compra digital';
        this.snackBar.open(`Error: ${msg}`, 'Cerrar', { duration: 5000 });
      }
    });
  }

  cerrar(): void {
    this.dialogRef.close(this.ordenConfirmada);
  }
}
