import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente, ClienteCreate, ClienteUpdate, HistorialCompra, HistorialReserva } from '../../models/cu3_gestionar_clientes/customer.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private apiUrl = `${environment.apiUrl}/clientes`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de clientes del tenant con filtros opcionales.
   */
  obtenerClientes(search?: string, activo?: boolean): Observable<Cliente[]> {
    let params = new HttpParams();
    if (search) {
      params = params.set('search', search);
    }
    if (activo !== undefined && activo !== null) {
      params = params.set('activo', activo.toString());
    }
    return this.http.get<Cliente[]>(this.apiUrl, { params });
  }

  /**
   * Obtiene el detalle de un cliente por su identificador.
   */
  obtenerClientePorId(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/${id}`);
  }

  /**
   * Registra un nuevo cliente en el tenant.
   */
  crearCliente(cliente: ClienteCreate): Observable<Cliente> {
    return this.http.post<Cliente>(this.apiUrl, cliente);
  }

  /**
   * Actualiza los datos personales o de contacto del cliente.
   */
  actualizarCliente(id: number, cliente: ClienteUpdate): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/${id}`, cliente);
  }

  /**
   * Cambia el estado activo/inactivo del cliente.
   */
  cambiarEstadoCliente(id: number, activo: boolean): Observable<Cliente> {
    return this.http.patch<Cliente>(`${this.apiUrl}/${id}/estado`, { activo });
  }

  /**
   * Da de baja lógica al cliente en el tenant.
   */
  eliminarCliente(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }

  /**
   * Consulta las órdenes y compras realizadas por el cliente.
   */
  obtenerHistorialCompras(id: number): Observable<HistorialCompra[]> {
    return this.http.get<HistorialCompra[]>(`${this.apiUrl}/${id}/compras`);
  }

  /**
   * Consulta las reservas de prendas efectuadas por el cliente.
   */
  obtenerHistorialReservas(id: number): Observable<HistorialReserva[]> {
    return this.http.get<HistorialReserva[]>(`${this.apiUrl}/${id}/reservas`);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  getClientes(search?: string, activo?: boolean): Observable<Cliente[]> {
    return this.obtenerClientes(search, activo);
  }

  getClienteById(id: number): Observable<Cliente> {
    return this.obtenerClientePorId(id);
  }

  createCliente(cliente: ClienteCreate): Observable<Cliente> {
    return this.crearCliente(cliente);
  }

  updateCliente(id: number, cliente: ClienteUpdate): Observable<Cliente> {
    return this.actualizarCliente(id, cliente);
  }

  toggleClienteEstado(id: number, activo: boolean): Observable<Cliente> {
    return this.cambiarEstadoCliente(id, activo);
  }

  deleteCliente(id: number): Observable<any> {
    return this.eliminarCliente(id);
  }

  getHistorialCompras(id: number): Observable<HistorialCompra[]> {
    return this.obtenerHistorialCompras(id);
  }

  getHistorialReservas(id: number): Observable<HistorialReserva[]> {
    return this.obtenerHistorialReservas(id);
  }
}

export { CustomerService as ClienteService };
