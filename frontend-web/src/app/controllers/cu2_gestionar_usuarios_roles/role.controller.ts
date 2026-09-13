import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Rol, RolCreateDTO } from '../../models/cu2_gestionar_usuarios_roles/role.model';
import { RoleService } from '../../services/cu2_gestionar_usuarios_roles/role.service';

@Injectable({
  providedIn: 'root'
})
export class RoleController {
  private rolesSubject = new BehaviorSubject<Rol[]>([]);
  public roles$: Observable<Rol[]> = this.rolesSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private roleService: RoleService) {}

  loadRoles(): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.roleService.getRoles().subscribe({
      next: (roles) => {
        this.rolesSubject.next(roles);
        this.loadingSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar roles:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los roles');
        this.loadingSubject.next(false);
      }
    });
  }

  createRole(roleData: RolCreateDTO): Observable<Rol> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.createRole(roleData).subscribe({
        next: (newRole) => {
          const currentRoles = this.rolesSubject.value;
          this.rolesSubject.next([...currentRoles, newRole]);
          this.loadingSubject.next(false);
          subscriber.next(newRole);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al crear el rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  updateRole(id: number, roleData: RolCreateDTO): Observable<Rol> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.updateRole(id, roleData).subscribe({
        next: (updatedRole) => {
          const updatedList = this.rolesSubject.value.map(r => r.id === id ? updatedRole : r);
          this.rolesSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next(updatedRole);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al actualizar el rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  updatePermissions(id: number, permisos: string[]): Observable<Rol> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.updateRolePermissions(id, permisos).subscribe({
        next: (updatedRole) => {
          const updatedList = this.rolesSubject.value.map(r => r.id === id ? updatedRole : r);
          this.rolesSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next(updatedRole);
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al guardar los permisos';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  deleteRole(id: number): Observable<void> {
    this.loadingSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.deleteRole(id).subscribe({
        next: () => {
          const updatedList = this.rolesSubject.value.filter(r => r.id !== id);
          this.rolesSubject.next(updatedList);
          this.loadingSubject.next(false);
          subscriber.next();
          subscriber.complete();
        },
        error: (err) => {
          this.loadingSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al eliminar el rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }
}
