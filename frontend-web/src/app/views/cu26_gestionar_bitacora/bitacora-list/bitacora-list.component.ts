import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BitacoraListComponent as LegacyBitacoraListComponent } from '../../cu20_gestionar_bitacora/bitacora/bitacora-list/bitacora-list.component';

@Component({
  selector: 'app-cu26-bitacora-list',
  standalone: true,
  imports: [CommonModule, LegacyBitacoraListComponent],
  template: `<app-bitacora-list></app-bitacora-list>`
})
export class BitacoraListComponent {}
