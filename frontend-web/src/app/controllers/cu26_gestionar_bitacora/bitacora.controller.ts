// CU26 - GESTIONAR BITÁCORA Y AUDITORÍA -> CONTROLLER
import { Injectable } from '@angular/core';
import { BitacoraController as LegacyBitacoraController } from '../cu20_gestionar_bitacora/bitacora.controller';

@Injectable({
  providedIn: 'root'
})
export class BitacoraController extends LegacyBitacoraController {}
