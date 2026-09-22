import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { VentaCompleta } from '../../../../models/cu14_registrar_ventas_presenciales/venta.model';

export interface ReceiptDialogData {
  venta: VentaCompleta;
  items: Array<{
    nombre: string;
    variante?: string;
    cantidad: number;
    precio: number;
    subtotal: number;
  }>;
  montoRecibido?: number;
  cambio?: number;
}

@Component({
  selector: 'app-receipt-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule
  ],
  templateUrl: './receipt-dialog.component.html',
  styleUrls: ['./receipt-dialog.component.css']
})
export class ReceiptDialogComponent {
  venta: VentaCompleta;
  items: ReceiptDialogData['items'];
  montoRecibido?: number;
  cambio?: number;

  constructor(
    public dialogRef: MatDialogRef<ReceiptDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ReceiptDialogData
  ) {
    this.venta = data.venta;
    this.items = data.items;
    this.montoRecibido = data.montoRecibido;
    this.cambio = data.cambio;
  }

  printReceipt(): void {
    const printContent = this.buildReceiptHtml();
    
    // Use an invisible iframe for reliable printing across all browsers
    let iframe = document.getElementById('receipt-print-iframe') as HTMLIFrameElement;
    if (iframe) {
      iframe.remove();
    }
    iframe = document.createElement('iframe');
    iframe.id = 'receipt-print-iframe';
    iframe.style.position = 'fixed';
    iframe.style.right = '0';
    iframe.style.bottom = '0';
    iframe.style.width = '0px';
    iframe.style.height = '0px';
    iframe.style.border = 'none';
    document.body.appendChild(iframe);

    const doc = iframe.contentWindow?.document || iframe.contentDocument;
    if (!doc) {
      window.print();
      return;
    }

    doc.open();
    doc.write(printContent);
    doc.close();

    setTimeout(() => {
      try {
        iframe.contentWindow?.focus();
        iframe.contentWindow?.print();
      } catch (e) {
        console.error('Error al imprimir recibo vía iframe:', e);
        window.print();
      }
    }, 300);
  }

  private formatDate(dateStr?: string): string {
    if (!dateStr) return new Date().toLocaleString('es-BO', { timeZone: 'America/La_Paz' });
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('es-BO', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
        timeZone: 'America/La_Paz'
      });
    } catch {
      return dateStr;
    }
  }

  private buildReceiptHtml(): string {
    const fechaFormatted = this.formatDate(this.venta.fecha);
    const clienteNombre = this.venta.cliente_nombre || 'Consumidor Final';
    const metodoPago = this.venta.metodo_pago_nombre || 'Efectivo';
    const sucursalNombre = this.venta.sucursal_nombre || 'Sucursal Principal';

    const itemsHtml = this.items.map(it => `
      <tr>
        <td style="padding: 6px 4px; vertical-align: top; border-bottom: 1px dashed #e2e8f0;">
          <div style="font-weight: 700; color: #0f172a;">${it.nombre}</div>
          ${it.variante ? `<div style="font-size: 11px; color: #64748b;">${it.variante}</div>` : ''}
        </td>
        <td style="padding: 6px 4px; text-align: center; vertical-align: top; border-bottom: 1px dashed #e2e8f0;">
          ${it.cantidad}
        </td>
        <td style="padding: 6px 4px; text-align: right; vertical-align: top; border-bottom: 1px dashed #e2e8f0;">
          Bs. ${Number(it.precio).toFixed(2)}
        </td>
        <td style="padding: 6px 4px; text-align: right; vertical-align: top; font-weight: 700; border-bottom: 1px dashed #e2e8f0;">
          Bs. ${Number(it.subtotal).toFixed(2)}
        </td>
      </tr>
    `).join('');

    let efectivoHtml = '';
    if (this.montoRecibido && this.montoRecibido > 0) {
      efectivoHtml += `
        <div style="display: flex; justify-content: space-between; padding: 2px 0; font-size: 12px; color: #64748b;">
          <span>Efectivo Recibido:</span>
          <span>Bs. ${Number(this.montoRecibido).toFixed(2)}</span>
        </div>
      `;
    }
    if (this.cambio !== undefined && this.cambio > 0) {
      efectivoHtml += `
        <div style="display: flex; justify-content: space-between; padding: 3px 0; font-size: 13px; font-weight: 700; color: #1e40af;">
          <span>Cambio / Vuelto:</span>
          <span>Bs. ${Number(this.cambio).toFixed(2)}</span>
        </div>
      `;
    }

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>Recibo ${this.venta.codigoventa} - Shopyn Golden Store</title>
        <style>
          @page {
            size: auto;
            margin: 6mm;
          }
          * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
          }
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            color: #0f172a;
            background: #ffffff;
            margin: 0;
            padding: 10px;
            font-size: 12px;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
          }
          .ticket-card {
            max-width: 420px;
            margin: 0 auto;
            padding: 20px;
            border: 1px dashed #94a3b8;
            border-radius: 8px;
            background: #ffffff;
          }
          .header {
            text-align: center;
            margin-bottom: 12px;
          }
          .brand {
            font-size: 17px;
            font-weight: 900;
            letter-spacing: 1px;
            color: #0f172a;
            margin-bottom: 2px;
          }
          .sub {
            font-size: 11px;
            color: #64748b;
            margin-bottom: 6px;
          }
          .code-box {
            display: inline-block;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 3px 12px;
            border-radius: 6px;
            font-family: monospace;
            font-weight: 800;
            font-size: 13px;
            color: #1e293b;
          }
          .divider {
            border: none;
            border-top: 1px dashed #cbd5e1;
            margin: 10px 0;
          }
          .meta-grid {
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 11.5px;
            margin-bottom: 8px;
          }
          .meta-row {
            display: flex;
            justify-content: space-between;
          }
          .meta-label {
            color: #64748b;
          }
          .meta-val {
            font-weight: 600;
            color: #0f172a;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11.5px;
            margin: 8px 0;
          }
          th {
            border-bottom: 1.5px solid #0f172a;
            padding: 4px;
            font-size: 10.5px;
            text-transform: uppercase;
            color: #475569;
          }
          .totals-box {
            margin-top: 6px;
            display: flex;
            flex-direction: column;
            gap: 3px;
          }
          .total-row {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #334155;
          }
          .grand-total {
            font-size: 15px;
            font-weight: 900;
            color: #0f172a;
            border-top: 2px solid #0f172a;
            padding-top: 6px;
            margin-top: 4px;
          }
          .footer {
            text-align: center;
            margin-top: 16px;
            padding-top: 10px;
            border-top: 1px dashed #cbd5e1;
            font-size: 10.5px;
            color: #64748b;
          }
          .footer strong {
            display: block;
            font-size: 11.5px;
            color: #0f172a;
            margin-bottom: 2px;
          }
        </style>
      </head>
      <body>
        <div class="ticket-card">
          <div class="header">
            <div class="brand">SHOPYN GOLDEN STORE</div>
            <div class="sub">Comprobante de Venta Presencial (POS)</div>
            <div class="code-box">${this.venta.codigoventa}</div>
          </div>

          <div class="meta-grid">
            <div class="meta-row">
              <span class="meta-label">Fecha / Hora (BOT):</span>
              <span class="meta-val">${fechaFormatted}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Sucursal:</span>
              <span class="meta-val">${sucursalNombre}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Cliente:</span>
              <span class="meta-val">${clienteNombre}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Método de Pago:</span>
              <span class="meta-val">${metodoPago}</span>
            </div>
          </div>

          <hr class="divider">

          <table>
            <thead>
              <tr>
                <th style="text-align: left;">Producto</th>
                <th style="text-align: center; width: 45px;">Cant.</th>
                <th style="text-align: right; width: 75px;">P. Unit</th>
                <th style="text-align: right; width: 85px;">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              ${itemsHtml}
            </tbody>
          </table>

          <hr class="divider">

          <div class="totals-box">
            <div class="total-row">
              <span>Subtotal:</span>
              <span>Bs. ${Number(this.venta.subtotal).toFixed(2)}</span>
            </div>
            ${this.venta.descuento > 0 ? `
              <div class="total-row" style="color: #15803d;">
                <span>Descuento:</span>
                <span>- Bs. ${Number(this.venta.descuento).toFixed(2)}</span>
              </div>
            ` : ''}
            <div class="total-row grand-total">
              <span>TOTAL PAGADO:</span>
              <span>Bs. ${Number(this.venta.total).toFixed(2)}</span>
            </div>
            ${efectivoHtml}
          </div>

          <div class="footer">
            <strong>¡Gracias por su preferencia!</strong>
            <p>Shopyn Golden Store &bull; Mostrador &bull; Caja Presencial</p>
            <p style="margin-top: 3px; font-size: 9.5px; color: #94a3b8;">Sistema ERP &bull; PostgreSQL Transaccional</p>
          </div>
        </div>
      </body>
      </html>
    `;
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
