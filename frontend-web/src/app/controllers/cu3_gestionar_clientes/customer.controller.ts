import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Cliente, ClienteCreate, ClienteUpdate, HistorialCompra, HistorialReserva } from '../../models/cu3_gestionar_clientes/customer.model';
import { CustomerService } from '../../services/cu3_gestionar_clientes/customer.service';

@Injectable({
  providedIn: 'root'
})
export class CustomerController {
  private clientesSubject = new BehaviorSubject<Cliente[]>([]);
  public clientes$: Observable<Cliente[]> = this.clientesSubject.asObservable();
  public customers$: Observable<Cliente[]> = this.clientes$;

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private customerService: CustomerService) {}

  /**
   * Carga la lista de clientes del tenant con filtros opcionales.
   */
  cargarClientes(search?: string, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);

    this.customerService.obtenerClientes(search, activo).subscribe({
      next: (clientes) => {
        this.clientesSubject.next(clientes);
        this.cargandoSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar clientes:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los clientes');
        this.cargandoSubject.next(false);
      }
    });
  }

  /**
   * Registra un nuevo cliente y actualiza el estado reactivo.
   */
  crearCliente(clienteData: ClienteCreate): Observable<Cliente> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.customerService.crearCliente(clienteData).subscribe({
        next: (nuevoCliente) => {
          const actuales = this.clientesSubject.value;
          this.clientesSubject.next([nuevoCliente, ...actuales]);
          this.cargandoSubject.next(false);
          subscriber.next(nuevoCliente);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al registrar cliente';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Actualiza la información del cliente en el estado observable.
   */
  actualizarCliente(id: number, clienteData: ClienteUpdate): Observable<Cliente> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.customerService.actualizarCliente(id, clienteData).subscribe({
        next: (clienteActualizado) => {
          const listaActualizada = this.clientesSubject.value.map(c => 
            c.id === id ? { ...c, ...clienteActualizado } : c
          );
          this.clientesSubject.next(listaActualizada);
          this.cargandoSubject.next(false);
          subscriber.next(clienteActualizado);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al actualizar cliente';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Cambia el estado activo/suspendido del cliente.
   */
  cambiarEstado(id: number, estadoActual: boolean): Observable<Cliente> {
    const nuevoEstado = !estadoActual;
    return new Observable((subscriber) => {
      this.customerService.cambiarEstadoCliente(id, nuevoEstado).subscribe({
        next: (clienteActualizado) => {
          const listaActualizada = this.clientesSubject.value.map(c => 
            c.id === id ? { ...c, activo: nuevoEstado } : c
          );
          this.clientesSubject.next(listaActualizada);
          subscriber.next(clienteActualizado);
          subscriber.complete();
        },
        error: (err) => {
          const errorMsg = err?.error?.detail || 'Error al cambiar estado del cliente';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Da de baja lógica al cliente eliminándolo de la lista activa.
   */
  eliminarCliente(id: number): Observable<void> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.customerService.eliminarCliente(id).subscribe({
        next: () => {
          const listaActualizada = this.clientesSubject.value.filter(c => c.id !== id);
          this.clientesSubject.next(listaActualizada);
          this.cargandoSubject.next(false);
          subscriber.next();
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al realizar baja lógica';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Obtiene el historial de compras del cliente.
   */
  obtenerHistorialCompras(id: number): Observable<HistorialCompra[]> {
    return this.customerService.obtenerHistorialCompras(id);
  }

  /**
   * Obtiene el historial de reservas de prendas del cliente.
   */
  obtenerHistorialReservas(id: number): Observable<HistorialReserva[]> {
    return this.customerService.obtenerHistorialReservas(id);
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadClientes(search?: string, activo?: boolean): void {
    this.cargarClientes(search, activo);
  }

  createCliente(clienteData: ClienteCreate): Observable<Cliente> {
    return this.crearCliente(clienteData);
  }

  updateCliente(id: number, clienteData: ClienteUpdate): Observable<Cliente> {
    return this.actualizarCliente(id, clienteData);
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Cliente> {
    return this.cambiarEstado(id, currentStatus);
  }

  deleteCliente(id: number): Observable<void> {
    return this.eliminarCliente(id);
  }
}

export { CustomerController as ClienteController };
