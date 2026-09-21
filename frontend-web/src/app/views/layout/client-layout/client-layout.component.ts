import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatBadgeModule } from '@angular/material/badge';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';
import { MatTooltipModule } from '@angular/material/tooltip';

import { AuthService } from '../../../core/services/auth.service';
import { CartService } from '../../../services/cu9_gestionar_carrito_compras/cart.service';

@Component({
  selector: 'app-client-layout',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatBadgeModule,
    MatMenuModule,
    MatDividerModule,
    MatTooltipModule
  ],
  templateUrl: './client-layout.component.html',
  styleUrls: ['./client-layout.component.css']
})
export class ClientLayoutComponent implements OnInit {
  userName = 'Cliente';
  userEmail = '';
  userRole = 'CLIENTE';
  isAdmin = false;
  isLoggedIn = false;
  currentUser: any = null;
  mostrarModalPerfil = false;

  constructor(
    public authService: AuthService,
    public cartService: CartService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.refreshUserState();
  }

  refreshUserState(): void {
    this.isLoggedIn = this.authService.isAuthenticated();
    this.isAdmin = this.authService.isAdmin();
    this.userRole = this.authService.getUserRole() || 'CLIENTE';

    const user = this.authService.getCurrentUser();
    this.currentUser = user;
    if (user) {
      this.userName = `${user.nombre || ''} ${user.apellido || ''}`.trim() || user.nombre || 'Cliente';
      this.userEmail = user.email || '';
    }
  }

  abrirModalPerfil(): void {
    this.refreshUserState();
    this.mostrarModalPerfil = true;
  }

  cerrarModalPerfil(): void {
    this.mostrarModalPerfil = false;
  }

  get userInitial(): string {
    return (this.userName.charAt(0) || 'C').toUpperCase();
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}

