// ==============================================================================
// CU22 - REGISTRAR COBROS DE CONTADO SIN CONEXIÓN -> COMPONENTE VISTA
// Ubicación: frontend-web/src/app/views/cu22_registrar_cobros_contado_offline/cobro-offline-list/cobro-offline-list.component.ts
// ==============================================================================

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { CobroOfflineController } from '../../../controllers/cu22_registrar_cobros_contado_offline/cobro-offline.controller';
import {
  RegistroCobroOfflineRequest,
  ItemCobroOfflineDTO,
  CobroOfflineDTO
} from '../../../models/cu22_registrar_cobros_contado_offline/cobro-offline.model';

@Component({
  selector: 'app-cobro-offline-list',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './cobro-offline-list.component.html',
  styleUrls: ['./cobro-offline-list.component.css']
})
export class CobroOfflineListComponent implements OnInit {

  // Catálogo rápido de prendas en mostrador para ventas en contingencia
  catalogoPrendas = [
    { variante_id: 1, nombre: 'Polera Heavyweight Negra', talla: 'L', color: 'Negro', precio: 130.00 },
    { variante_id: 2, nombre: 'Polera Acid Wash Gris', talla: 'M', color: 'Gris', precio: 120.00 },
    { variante_id: 3, nombre: 'Polera Boxy Fit Blanca', talla: 'M', color: 'Blanco', precio: 110.00 },
    { variante_id: 4, nombre: 'Polera Oversize Beige', talla: 'XL', color: 'Beige', precio: 125.00 },
    { variante_id: 5, nombre: 'Polera Classic Graphic Street', talla: 'S', color: 'Negro', precio: 115.00 },
    { variante_id: 6, nombre: 'Polera Minimalist Dark Blue', talla: 'L', color: 'Azul Marino', precio: 105.00 }
  ];

  itemSeleccionadoIdx: number = 0;

  // Formulario de Cobro en Contingencia
  cobroForm: RegistroCobroOfflineRequest = {
    sucursal_id: 1,
    monto: 0,
    moneda: 'BOB',
    nro_recibo_provisional: '',
    uuid_operacion: '',
    cliente_nombre: 'Cliente Mostrador',
    cliente_nit: '0',
    efectivo_recibido: 0,
    cambio: 0,
    observaciones: 'Cobro de contado generado bajo régimen de contingencia offline',
    items: []
  };

  constructor(public ctrl: CobroOfflineController) {}

  ngOnInit(): void {
    this.ctrl.cargarTodo();
  }

  actualizarFiltro(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;
    this.ctrl.filtroTexto.set(valor);
  }

  abrirModalNuevoCobro(): void {
    const ahora = new Date();
    const fechaStr = ahora.toISOString().slice(0, 10).replace(/-/g, '');
    const randNum = Math.floor(1000 + Math.random() * 9000);

    this.cobroForm = {
      sucursal_id: 1,
      monto: 0,
      moneda: 'BOB',
      nro_recibo_provisional: `REC-OFF-${fechaStr}-${randNum}`,
      uuid_operacion: `pos-off-${Date.now()}-${randNum}`,
      cliente_nombre: 'Cliente Mostrador',
      cliente_nit: '0',
      efectivo_recibido: 0,
      cambio: 0,
      observaciones: 'Cobro de contado emitido bajo contingencia de red',
      items: []
    };

    // Agregar prenda inicial por conveniencia
    this.agregarPrendaSeleccionada();
    this.ctrl.abrirModalNuevoCobro();
  }

  agregarPrendaSeleccionada(): void {
    const sel = this.catalogoPrendas[this.itemSeleccionadoIdx];
    if (!sel) return;

    if (!this.cobroForm.items) {
      this.cobroForm.items = [];
    }

    const itemExistente = this.cobroForm.items.find(it => it.variante_id === sel.variante_id);
    if (itemExistente) {
      itemExistente.cantidad += 1;
      itemExistente.subtotal = itemExistente.cantidad * itemExistente.precio_unitario;
    } else {
      this.cobroForm.items.push({
        variante_id: sel.variante_id,
        producto_nombre: sel.nombre,
        talla: sel.talla,
        color: sel.color,
        cantidad: 1,
        precio_unitario: sel.precio,
        subtotal: sel.precio
      });
    }

    this.recalcularTotales();
  }

  eliminarItem(index: number): void {
    if (!this.cobroForm.items) return;
    this.cobroForm.items.splice(index, 1);
    this.recalcularTotales();
  }

  recalcularTotales(): void {
    if (!this.cobroForm.items || this.cobroForm.items.length === 0) {
      this.cobroForm.monto = 0;
      this.calcularCambio();
      return;
    }

    let total = 0;
    for (const it of this.cobroForm.items) {
      it.subtotal = it.cantidad * it.precio_unitario;
      total += it.subtotal;
    }
    this.cobroForm.monto = total;

    // Si aún no se ingresó efectivo o es menor, ajustar sugerencia
    if (!this.cobroForm.efectivo_recibido || this.cobroForm.efectivo_recibido < total) {
      this.cobroForm.efectivo_recibido = Math.ceil(total / 10) * 10;
    }
    this.calcularCambio();
  }

  calcularCambio(): void {
    const recibido = this.cobroForm.efectivo_recibido || 0;
    const monto = this.cobroForm.monto || 0;
    this.cobroForm.cambio = Math.max(0, recibido - monto);
  }

  confirmarCobroOffline(): void {
    this.ctrl.registrarCobro(this.cobroForm, (cobroCreado: CobroOfflineDTO) => {
      // Abrir inmediatamente la vista de ticket para entrega al cliente
      this.ctrl.verTicket(cobroCreado);
    });
  }

  calcularTotalMonto(): number {
    return this.ctrl.cobros().reduce((sum, c) => sum + (Number(c.monto) || 0), 0);
  }

  calcularPendientesCount(): number {
    return this.ctrl.cobros().filter(c => !c.sincronizado).length;
  }
}
