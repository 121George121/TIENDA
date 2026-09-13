import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Usuario, UsuarioCreateDTO, UsuarioUpdateDTO } from '../../models/cu2_gestionar_usuarios_roles/user.model';
import { UserService } from '../../services/cu2_gestionar_usuarios_roles/user.service';

@Injectable({
  providedIn: 'root'
})
export class UserController {
  private usersSubject = new BehaviorSubject<Usuario[]>([]);
  public users$: Observable<Usuario[]> = this.usersSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private userService: UserService) {}

  loadUsers(search?: string, rolId?: number, activo?: boolean): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.userService.getUsers(search, rolId, activo).subscribe({
      next: (users) => {
        this.usersSubject.next(users);
        this.loadingSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar usuarios:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los usuarios');
        this.loadingSubject.next(false);
      }
    });
  }

  createUser(userData: UsuarioCreateDTO): Observable<Usuario> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.userService.createUser(userData).subscribe({
        next: (newUser) => {
          const currentUsers = this.usersSubject.value;
          this.usersSubject.next([newUser, ...currentUsers]);
          this.loadingSubject.next(false);
          subscriber.next(newUser);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al crear el usuario';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  updateUser(id: number, userData: UsuarioUpdateDTO): Observable<Usuario> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.userService.updateUser(id, userData).subscribe({
        next: (updatedUser) => {
          const updatedList = this.usersSubject.value.map(u => u.id === id ? { ...u, ...updatedUser } : u);
          this.usersSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next(updatedUser);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al actualizar el usuario';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Usuario> {
    const nextStatus = !currentStatus;
    return new Observable((subscriber) => {
      this.userService.toggleUserStatus(id, nextStatus).subscribe({
        next: (updatedUser) => {
          const updatedList = this.usersSubject.value.map(u => u.id === id ? { ...u, activo: nextStatus } : u);
          this.usersSubject.next(updatedList);
          subscriber.next(updatedUser);
          subscriber.complete();
        },
        error: (err) => {
          const errorMsg = err?.error?.detail || 'Error al cambiar estado';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  assignRole(id: number, rolId: number): Observable<Usuario> {
    return new Observable((subscriber) => {
      this.userService.assignUserRole(id, rolId).subscribe({
        next: (updatedUser) => {
          const updatedList = this.usersSubject.value.map(u => u.id === id ? { ...u, rol_id: rolId, rolid: rolId } : u);
          this.usersSubject.next(updatedList);
          subscriber.next(updatedUser);
          subscriber.complete();
        },
        error: (err) => {
          const errorMsg = err?.error?.detail || 'Error al asignar rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  deleteUser(id: number): Observable<void> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.userService.deleteUser(id).subscribe({
        next: () => {
          const updatedList = this.usersSubject.value.filter(u => u.id !== id);
          this.usersSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next();
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al eliminar el usuario';
          subscriber.error(errorMsg);
        }
      });
    });
  }
}
