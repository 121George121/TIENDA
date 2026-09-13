import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDividerModule } from '@angular/material/divider';

import { CompraDigitalController } from '../../../controllers/cu15_realizar_compras_digitales/compra-digital.controller';
import { OrdenResponseDTO } from '../../../services/cu15_realizar_compras_digitales/compra-digital.service';

@Component({
  selector: 'app-mis-pedidos-web',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatDividerModule
  ],
  templateUrl: './mis-pedidos-web.component.html',
  styleUrls: ['./mis-pedidos-web.component.css']
})
export class MisPedidosWebComponent implements OnInit {
  ordenes: OrdenResponseDTO[] = [];
  loading = true;

  constructor(
    public compraCtrl: CompraDigitalController,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.compraCtrl.misOrdenes$.subscribe(ord => {
      this.ordenes = ord;
    });
    this.cargar();
  }

  cargar(): void {
    this.loading = true;
    this.compraCtrl.loadMisOrdenes();
    setTimeout(() => this.loading = false, 600);
  }

  volverATienda(): void {
    this.router.navigate(['/catalogo']);
  }

  getOrderStep(estado: string): number {
    const s = (estado || '').toUpperCase();
    if (s.includes('PREPAR') || s.includes('CONFIRMAD')) return 1;
    if (s.includes('CAMINO') || s.includes('ENVIAD') || s.includes('TRANSITO')) return 2;
    if (s.includes('ENTREGAD') || s.includes('COMPLETAD') || s.includes('FINALIZAD')) return 3;
    return 0; // REGISTRADO
  }
}
