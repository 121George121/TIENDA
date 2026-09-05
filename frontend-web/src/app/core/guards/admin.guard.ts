import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
  const userStr = localStorage.getItem('usuario') || localStorage.getItem('user');
  const userRol = localStorage.getItem('rol') || localStorage.getItem('user_role');

  if (!token) {
    console.warn('adminGuard: No hay token en localStorage, redirigiendo a login');
    router.navigate(['/login']);
    return false;
  }

  const isRolAdmin = userRol && (userRol.toUpperCase() === 'ADMIN' || userRol.toUpperCase() === 'ADMINISTRADOR');
  
  // Si tenemos información de usuario en localStorage
  if (userStr) {
    try {
      const user = JSON.parse(userStr);
      if (user && (isRolAdmin || user.rol_id === 1 || user.rolid === 1)) {
        return true;
      }
    } catch (e) {
      console.error('Error al parsear usuario de localStorage', e);
    }
  }

  // Si hay token presente y no está explícitamente denegado
  if (token) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};
