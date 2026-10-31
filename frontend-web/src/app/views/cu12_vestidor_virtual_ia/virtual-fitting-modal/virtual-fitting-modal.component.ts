// ==============================================================================
// CAPA VISTA (MVC - VIEW EN ANGULAR 18)
// Módulo: CU12 - Utilizar Vestidor Virtual mediante IA
// Ubicación: frontend-web/src/app/views/cu12_vestidor_virtual_ia/virtual-fitting-modal/virtual-fitting-modal.component.ts
// ==============================================================================

import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';

import { VestidorService } from '../../../services/cu12_vestidor_virtual_ia/vestidor.service';
import { AnalisisFisonomiaResponse, TryOnResponse } from '../../../models/cu12_vestidor_virtual_ia/vestidor.model';

@Component({
  selector: 'app-virtual-fitting-modal',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule
  ],
  templateUrl: './virtual-fitting-modal.component.html',
  styleUrls: ['./virtual-fitting-modal.component.css']
})
export class VirtualFittingModalComponent implements OnInit {
  @Input() visible = false;
  @Input() producto: any = null;
  @Input() varianteInicial: any = null;

  @Output() cerrar = new EventEmitter<void>();
  @Output() agregarAlCarrito = new EventEmitter<any>();

  tallaSeleccionada = 'M';
  colorSeleccionado = 'Grafito';
  codigoHexSeleccionado = '#333333';

  // Foto de usuario
  fotoUsuarioPreview: string | null = null;
  fotoUsuarioFile: File | null = null;
  usarManiqui = false;

  // Estados de IA
  analizandoFisonomia = false;
  generandoTryon = false;
  analisisResultado: AnalisisFisonomiaResponse | null = null;
  tryonResultado: TryOnResponse | null = null;
  pasoGeneracionTexto = '';

  constructor(public vestidorService: VestidorService) {}

  ngOnInit(): void {
    if (this.varianteInicial) {
      this.tallaSeleccionada = this.varianteInicial.talla || 'M';
      this.colorSeleccionado = this.varianteInicial.color || 'Grafito';
      this.codigoHexSeleccionado = this.varianteInicial.codigohex || '#333333';
    }
  }

  onFileSelected(event: any): void {
    const file = event.target.files?.[0];
    if (file) {
      this.fotoUsuarioFile = file;
      this.usarManiqui = false;
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.fotoUsuarioPreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  usarModeloEjemplo(): void {
    this.usarManiqui = true;
    this.fotoUsuarioPreview = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500';
    // Crear un blob dummy para enviar si es necesario
    fetch(this.fotoUsuarioPreview)
      .then(res => res.blob())
      .then(blob => {
        this.fotoUsuarioFile = new File([blob], 'modelo_ejemplo.jpg', { type: 'image/jpeg' });
      })
      .catch(() => {
        // Fallback en caso de CORS
        this.fotoUsuarioFile = null;
      });
  }

  ejecutarAnalisisFisonomia(): void {
    if (!this.producto) return;
    this.analizandoFisonomia = true;
    this.analisisResultado = null;

    this.vestidorService.analizarFisonomia(
      this.producto.nombre,
      this.tallaSeleccionada,
      this.colorSeleccionado,
      this.fotoUsuarioFile || undefined
    ).subscribe({
      next: (res) => {
        this.analisisResultado = res;
        this.analizandoFisonomia = false;
      },
      error: (err: any) => {
        this.analizandoFisonomia = false;
        alert(err.error?.detail || 'No se pudo completar el análisis fisonómico con IA');
      }
    });
  }

  aplicarTallaSugerida(talla: string): void {
    this.tallaSeleccionada = talla;
  }

  ejecutarTryOn(): void {
    if (!this.producto) return;
    if (!this.fotoUsuarioFile && !this.fotoUsuarioPreview) {
      alert('Por favor sube una fotografía tuya o selecciona el avatar modelo para probar la prenda.');
      return;
    }

    this.generandoTryon = true;
    this.tryonResultado = null;
    this.pasoGeneracionTexto = 'Aislando prenda textil con IA...';

    setTimeout(() => {
      if (this.generandoTryon) this.pasoGeneracionTexto = 'Detectando anatomía y ajuste ergonómico...';
    }, 1500);

    setTimeout(() => {
      if (this.generandoTryon) this.pasoGeneracionTexto = 'Sintetizando caída fotorrealista y drapeado...';
    }, 3500);

    const imagenUrl = this.producto.imagen_url || 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500';

    // Si no tenemos un file real pero tenemos preview, creamos un archivo dummy
    let fileToSend = this.fotoUsuarioFile;
    if (!fileToSend) {
      const dummyCanvas = document.createElement('canvas');
      dummyCanvas.width = 300;
      dummyCanvas.height = 400;
      const ctx = dummyCanvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#f0ebe1';
        ctx.fillRect(0, 0, 300, 400);
      }
      dummyCanvas.toBlob(blob => {
        if (blob) {
          fileToSend = new File([blob], 'avatar.jpg', { type: 'image/jpeg' });
          this.enviarPeticionTryOn(imagenUrl, fileToSend);
        }
      });
    } else {
      this.enviarPeticionTryOn(imagenUrl, fileToSend);
    }
  }

  private enviarPeticionTryOn(prendaUrl: string, file: File): void {
    this.vestidorService.generarTryOn(
      prendaUrl,
      this.producto.nombre,
      this.tallaSeleccionada,
      this.colorSeleccionado,
      file
    ).subscribe({
      next: (res) => {
        this.tryonResultado = res;
        this.generandoTryon = false;
      },
      error: (err: any) => {
        this.generandoTryon = false;
        alert(err.error?.detail || 'No se pudo generar la prueba virtual de ropa');
      }
    });
  }

  agregarPrendaProbada(): void {
    if (!this.producto) return;
    this.agregarAlCarrito.emit({
      producto: this.producto,
      talla: this.tallaSeleccionada,
      color: this.colorSeleccionado
    });
    this.onCerrar();
  }

  onCerrar(): void {
    this.cerrar.emit();
  }
}
