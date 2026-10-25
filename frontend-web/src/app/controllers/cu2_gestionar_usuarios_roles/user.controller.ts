import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Usuario, UsuarioCreateDTO, UsuarioUpdateDTO } from '../../models/cu2_gestionar_usuarios_roles/user.model';
import { UserService } from '../../services/cu2_gestionar_usuarios_roles/user.service';

@Injectable({
  providedIn: 'root'
})
export class UserController {
  private usuariosSubject = new BehaviorSubject<Usuario[]>([]);
  public usuarios$: Observable<Usuario[]> = this.usuariosSubject.asObservable();
  public users$: Observable<Usuario[]> = this.usuarios$;

  private cargandoSubject = new BehaviorSubject<boolean>(false);
  public cargando$: Observable<boolean> = this.cargandoSubject.asObservable();
  public loading$: Observable<boolean> = this.cargando$;

  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$: Observable<string | null> = this.errorSubject.asObservable();

  constructor(private userService: UserService) {}

  /**
   * Carga los usuarios desde el servicio filtrando por criterios opcionales.
   */
  cargarUsuarios(search?: string, rolId?: number, activo?: boolean): void {
    this.cargandoSubject.next(true);
    this.errorSubject.next(null);

    this.userService.obtenerUsuarios(search, rolId, activo).subscribe({
      next: (usuarios) => {
        this.usuariosSubject.next(usuarios);
        this.cargandoSubject.next(false);
      },
      error: (err) => {
        console.error('Error al cargar usuarios:', err);
        this.errorSubject.next(err?.error?.detail || 'No se pudieron cargar los usuarios');
        this.cargandoSubject.next(false);
      }
    });
  }

  /**
   * Registra un nuevo usuario en la lista del controlador.
   */
  crearUsuario(userData: UsuarioCreateDTO): Observable<Usuario> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.userService.crearUsuario(userData).subscribe({
        next: (nuevoUsuario) => {
          const actuales = this.usuariosSubject.value;
          this.usuariosSubject.next([nuevoUsuario, ...actuales]);
          this.cargandoSubject.next(false);
          subscriber.next(nuevoUsuario);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al crear el usuario';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Actualiza los datos de un usuario en el estado observable.
   */
  actualizarUsuario(id: number, userData: UsuarioUpdateDTO): Observable<Usuario> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.userService.actualizarUsuario(id, userData).subscribe({
        next: (usuarioActualizado) => {
          const listaActualizada = this.usuariosSubject.value.map(u => 
            u.id === id ? { ...u, ...usuarioActualizado } : u
          );
          this.usuariosSubject.next(listaActualizada);
          this.cargandoSubject.next(false);
          subscriber.next(usuarioActualizado);
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al actualizar el usuario';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Cambia el estado activo/suspendido de un usuario.
   */
  cambiarEstado(id: number, estadoActual: boolean): Observable<Usuario> {
    const nuevoEstado = !estadoActual;
    return new Observable((subscriber) => {
      this.userService.cambiarEstadoUsuario(id, nuevoEstado).subscribe({
        next: (usuarioActualizado) => {
          const listaActualizada = this.usuariosSubject.value.map(u => 
            u.id === id ? { ...u, activo: nuevoEstado } : u
          );
          this.usuariosSubject.next(listaActualizada);
          subscriber.next(usuarioActualizado);
          subscriber.complete();
        },
        error: (err) => {
          const errorMsg = err?.error?.detail || 'Error al cambiar estado';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Asigna un nuevo rol al usuario en el estado local.
   */
  asignarRol(id: number, rolId: number): Observable<Usuario> {
    return new Observable((subscriber) => {
      this.userService.asignarRolUsuario(id, rolId).subscribe({
        next: (usuarioActualizado) => {
          const listaActualizada = this.usuariosSubject.value.map(u => 
            u.id === id ? { ...u, rol_id: rolId, rolid: rolId } : u
          );
          this.usuariosSubject.next(listaActualizada);
          subscriber.next(usuarioActualizado);
          subscriber.complete();
        },
        error: (err) => {
          const errorMsg = err?.error?.detail || 'Error al asignar rol';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  /**
   * Elimina un usuario del estado local tras confirmación de la API.
   */
  eliminarUsuario(id: number): Observable<void> {
    this.cargandoSubject.next(true);
    return new Observable((subscriber) => {
      this.userService.eliminarUsuario(id).subscribe({
        next: () => {
          const listaActualizada = this.usuariosSubject.value.filter(u => u.id !== id);
          this.usuariosSubject.next(listaActualizada);
          this.cargandoSubject.next(false);
          subscriber.next();
          subscriber.complete();
        },
        error: (err) => {
          this.cargandoSubject.next(false);
          const errorMsg = err?.error?.detail || 'Error al eliminar el usuario';
          subscriber.error(errorMsg);
        }
      });
    });
  }

  // ============================================================================
  // ALIASES DE RETROCOMPATIBILIDAD
  // ============================================================================
  loadUsers(search?: string, rolId?: number, activo?: boolean): void {
    this.cargarUsuarios(search, rolId, activo);
  }

  createUser(userData: UsuarioCreateDTO): Observable<Usuario> {
    return this.crearUsuario(userData);
  }

  updateUser(id: number, userData: UsuarioUpdateDTO): Observable<Usuario> {
    return this.actualizarUsuario(id, userData);
  }

  toggleStatus(id: number, currentStatus: boolean): Observable<Usuario> {
    return this.cambiarEstado(id, currentStatus);
  }

  assignRole(id: number, rolId: number): Observable<Usuario> {
    return this.asignarRol(id, rolId);
  }

  deleteUser(id: number): Observable<void> {
    return this.eliminarUsuario(id);
  }
}

export { UserController as UsuarioController };
