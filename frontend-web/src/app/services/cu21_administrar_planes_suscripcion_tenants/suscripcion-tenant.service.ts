// CU21 - ADMINISTRAR PLANES DE SUSCRIPCIÓN Y TENANTS -> SERVICE
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { PlanSuscripcionDTO, TenantDTO, NuevoTenantRequest } from '../../models/cu21_administrar_planes_suscripcion_tenants/suscripcion-tenant.model';

@Injectable({
  providedIn: 'root'
})
export class SuscripcionTenantService {
  private readonly apiUrl = `${environment.apiUrl}/suscripciones-tenants`;

  constructor(private http: HttpClient) {}

  listarPlanes(): Observable<{ exito: boolean; planes: PlanSuscripcionDTO[] }> {
    return this.http.get<{ exito: boolean; planes: PlanSuscripcionDTO[] }>(`${this.apiUrl}/planes`);
  }

  listarTenants(): Observable<{ exito: boolean; tenants: TenantDTO[] }> {
    return this.http.get<{ exito: boolean; tenants: TenantDTO[] }>(`${this.apiUrl}/tenants`);
  }

  registrarTenant(payload: NuevoTenantRequest): Observable<{ exito: boolean; tenant: TenantDTO }> {
    return this.http.post<{ exito: boolean; tenant: TenantDTO }>(`${this.apiUrl}/tenants`, payload);
  }
}
