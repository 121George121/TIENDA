import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Cliente, ClienteCreate, ClienteUpdate } from '../models/customer.model';
import { CustomerService } from '../services/customer.service';

@Injectable({
  providedIn: 'root'
})
export class CustomerController {
  private customersSubject = new BehaviorSubject<Cliente[]>([]);
  public customers$: Observable<Cliente[]> = this.customersSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private customerService: CustomerService) {}

  loadClientes(search?: string, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.customerService.getClientes(search, activo).subscribe({
      next: (clientes) => {
        this.customersSubject.next(clientes);
        this.loadingSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar clientes:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los clientes');
        this.loadingSubject.next(false);
      }
    });
  }

  createCliente(clienteData: ClienteCreate): Observable<Cliente> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.customerService.createCliente(clienteData).subscribe({
        next: (newCliente) => {
          const currentList = this.customersSubject.value;
          this.customersSubject.next([newCliente, ...currentList]);
          this.loadingSubject.next(false);
          subscriber.next(newCliente);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al registrar cliente';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  updateCliente(id: number, clienteData: ClienteUpdate): Observable<Cliente> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.customerService.updateCliente(id, clienteData).subscribe({
        next: (updatedCliente) => {
          const updatedList = this.customersSubject.value.map(c => c.id === id ? { ...c, ...updatedCliente } : c);
          this.customersSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next(updatedCliente);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al actualizar cliente';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Cliente> {
    const nextStatus = !currentStatus;
    return new Observable((subscriber) => {
      this.customerService.toggleClienteEstado(id, nextStatus).subscribe({
        next: (updatedCliente) => {
          const updatedList = this.customersSubject.value.map(c => c.id === id ? { ...c, activo: nextStatus } : c);
          this.customersSubject.next(updatedList);
          subscriber.next(updatedCliente);
          subscriber.complete();
        },
        error: (err) => {
          const errorMsg = err?.error?.detail || 'Error al cambiar estado del cliente';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  deleteCliente(id: number): Observable<void> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.customerService.deleteCliente(id).subscribe({
        next: () => {
          const updatedList = this.customersSubject.value.filter(c => c.id !== id);
          this.customersSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next();
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al realizar baja lógica';
          subscriber.error(errorMsg);
        }
      });
    });
  }
}
