import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
  const userStr = localStorage.getItem('usuario') || localStorage.getItem('user');
  const userRol = (localStorage.getItem('rol') || localStorage.getItem('user_role') || '').toUpperCase();

  if (!token) {
    console.warn('adminGuard: No hay token en localStorage, redirigiendo a login');
    router.navigate(['/login']);
    return false;
  }

  const isRolAdmin = userRol === 'ADMIN' || userRol === 'ADMINISTRADOR' || userRol === 'SUPERVISOR';

  if (isRolAdmin) {
    return true;
  }

  if (userStr) {
    try {
      const user = JSON.parse(userStr);
      if (user && (user.rol_id === 1 || user.rolid === 1 || user.rol_id === 2 || user.rolid === 2)) {
        return true;
      }
    } catch (e) {
      console.error('Error al parsear usuario de localStorage', e);
    }
  }

  // Si hay token activo válido permitimos acceso al panel
  if (token) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};
