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

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private roleService: RoleService) {}

  /**
   * Carga el catálogo de roles y permisos desde el servicio.
   */
  cargarRoles(): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);

    this.roleService.obtenerRoles().subscribe({
      next: (roles) => {
        this.rolesSubject.next(roles);
        this.cargandoSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar roles:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los roles');
        this.cargandoSubject.next(false);
      }
    });
  }

  /**
   * Registra un nuevo rol con sus permisos correspondientes.
   */
  crearRol(roleData: RolCreateDTO): Observable<Rol> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.crearRol(roleData).subscribe({
        next: (newRole) => {
          const currentRoles = this.rolesSubject.value;
          this.rolesSubject.next([...currentRoles, newRole]);
          this.cargandoSubject.next(false);
          subscriber.next(newRole);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al crear el rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Actualiza el nombre y descripción de un rol existente.
   */
  actualizarRol(id: number, roleData: RolCreateDTO): Observable<Rol> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.actualizarRol(id, roleData).subscribe({
        next: (updatedRole) => {
          const updatedList = this.rolesSubject.value.map(r => r.id === id ? updatedRole : r);
          this.rolesSubject.next(updatedList);
          this.cargandoSubject.next(false);
          subscriber.next(updatedRole);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al actualizar el rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Actualiza la matriz de permisos de seguridad de un rol.
   */
  actualizarPermisos(id: number, permisos: string[]): Observable<Rol> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.actualizarPermisosRol(id, permisos).subscribe({
        next: (updatedRole) => {
          const updatedList = this.rolesSubject.value.map(r => r.id === id ? updatedRole : r);
          this.rolesSubject.next(updatedList);
          this.cargandoSubject.next(false);
          subscriber.next(updatedRole);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al guardar los permisos';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Elimina un rol si no tiene dependencias activas.
   */
  eliminarRol(id: number): Observable<void> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.roleService.eliminarRol(id).subscribe({
        next: () => {
          const updatedList = this.rolesSubject.value.filter(r => r.id !== id);
          this.rolesSubject.next(updatedList);
          this.cargandoSubject.next(false);
          subscriber.next();
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al eliminar el rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadRoles(): void {
    this.cargarRoles();
  }

  createRole(roleData: RolCreateDTO): Observable<Rol> {
    return this.crearRol(roleData);
  }

  updateRole(id: number, roleData: RolCreateDTO): Observable<Rol> {
    return this.actualizarRol(id, roleData);
  }

  updatePermissions(id: number, permisos: string[]): Observable<Rol> {
    return this.actualizarPermisos(id, permisos);
  }

  deleteRole(id: number): Observable<void> {
    return this.eliminarRol(id);
  }
}

export { RoleController as RolController };
