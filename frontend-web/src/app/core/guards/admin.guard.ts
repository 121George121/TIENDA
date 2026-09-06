import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');

  if (!token) {
    console.warn('adminGuard: No hay token en localStorage, redirigiendo a login');
    router.navigate(['/login']);
    return false;
  }

  const userRol = (localStorage.getItem('rol') || localStorage.getItem('user_role') || '').toUpperCase();
  const isRolAdmin = userRol === 'ADMIN' || userRol === 'ADMINISTRADOR';

  if (isRolAdmin) {
    return true;
  }

  // Autenticado pero sin rol de administrador: no debe entrar al panel admin
  router.navigate(['/dashboard']);
  return false;
};
