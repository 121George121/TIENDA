import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente, ClienteCreate, ClienteUpdate, HistorialCompra, HistorialReserva } from '../../models/cu3_gestionar_clientes/customer.model';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private apiUrl = 'http://localhost:8000/api/v1/clientes';

  constructor(private http: HttpClient) {}

  getClientes(search?: string, activo?: boolean): Observable<Cliente[]> {
    let params = new HttpParams();
    if (search) {
      params = params.set('search', search);
    }
    if (activo !== undefined && activo !== null) {
      params = params.set('activo', activo.toString());
    }
    return this.http.get<Cliente[]>(this.apiUrl, { params });
  }

  getClienteById(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/${id}`);
  }

  createCliente(cliente: ClienteCreate): Observable<Cliente> {
    return this.http.post<Cliente>(this.apiUrl, cliente);
  }

  updateCliente(id: number, cliente: ClienteUpdate): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/${id}`, cliente);
  }

  toggleClienteEstado(id: number, activo: boolean): Observable<Cliente> {
    return this.http.patch<Cliente>(`${this.apiUrl}/${id}/estado`, { activo });
  }

  deleteCliente(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }

  getHistorialCompras(id: number): Observable<HistorialCompra[]> {
    return this.http.get<HistorialCompra[]>(`${this.apiUrl}/${id}/compras`);
  }

  getHistorialReservas(id: number): Observable<HistorialReserva[]> {
    return this.http.get<HistorialReserva[]>(`${this.apiUrl}/${id}/reservas`);
  }
}
