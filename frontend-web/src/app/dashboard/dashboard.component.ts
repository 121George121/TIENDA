import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard-container">
      <div class="welcome-card">
        <div class="user-badge">
          <span class="icon">👤</span>
        </div>
        <h1>¡Bienvenido, {{ nombre }}!</h1>
        <p class="role-text">Tu rol en el sistema es: <strong>{{ rol }}</strong></p>

        <div class="action-buttons" *ngIf="isAdmin">
          <button (click)="goToAdmin()" class="btn-admin">
            ⚙️ Gestionar Usuarios y Roles
          </button>
        </div>

        <button (click)="logout()" class="btn-logout">Cerrar Sesión</button>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
      font-family: 'Inter', system-ui, sans-serif;
    }
    .welcome-card {
      background: white;
      padding: 3.5rem 3rem;
      border-radius: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
      text-align: center;
      max-width: 480px;
      width: 90%;
    }
    .user-badge {
      width: 70px;
      height: 70px;
      background: #eef2ff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1.5rem auto;
      font-size: 2.2rem;
    }
    h1 { 
      color: #0f172a; 
      margin-bottom: 0.5rem; 
      font-size: 1.8rem;
      font-weight: 700;
    }
    .role-text { 
      margin-bottom: 2rem; 
      color: #64748b; 
      font-size: 1.05rem;
    }
    .role-text strong {
      color: #4f46e5;
    }
    .action-buttons {
      margin-bottom: 1.2rem;
    }
    .btn-admin {
      width: 100%;
      padding: 0.9rem 1.5rem;
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      color: white;
      border: none;
      border-radius: 12px;
      font-weight: 600;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .btn-admin:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(99, 102, 241, 0.45);
    }
    .btn-logout {
      width: 100%;
      padding: 0.8rem 1.5rem;
      background-color: #fee2e2;
      color: #dc2626;
      border: none;
      border-radius: 12px;
      font-weight: 600;
      font-size: 0.95rem;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .btn-logout:hover {
      background-color: #fca5a5;
    }
  `]
})
export class DashboardComponent implements OnInit {
  nombre = '';
  rol = '';
  isAdmin = false;

  constructor(private router: Router) {}

  ngOnInit() {
    const userStr = localStorage.getItem('usuario');
    const rolStr = localStorage.getItem('rol');
    if (userStr) {
      const user = JSON.parse(userStr);
      this.nombre = user.nombre;
      this.rol = rolStr || 'Usuario';
      this.isAdmin = this.rol.toUpperCase() === 'ADMIN' || this.rol.toUpperCase() === 'ADMINISTRADOR';

      // Redirigir automáticamente si es admin
      if (this.isAdmin) {
        this.router.navigate(['/admin/users']);
      }
    } else {
      this.router.navigate(['/login']);
    }
  }

  goToAdmin() {
    this.router.navigate(['/admin/users']);
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}
