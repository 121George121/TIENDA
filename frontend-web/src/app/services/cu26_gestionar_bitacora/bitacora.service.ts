// CU26 - GESTIONAR BITÁCORA Y AUDITORÍA -> SERVICE
import { Injectable } from '@angular/core';
import { BitacoraService as LegacyBitacoraService } from '../cu20_gestionar_bitacora/bitacora.service';

@Injectable({
  providedIn: 'root'
})
export class BitacoraService extends LegacyBitacoraService {}
