import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { Usuario } from '../../../../models/user.model';
import { Rol } from '../../../../models/role.model';

export interface UserDetailDialogData {
  usuario: Usuario;
  rolNombre: string;
}

@Component({
  selector: 'app-user-detail-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatDividerModule
  ],
  template: `
    <div class="user-detail-container">
      <div class="user-header">
        <div class="avatar-large" [ngClass]="{'avatar-inactive': !data.usuario.activo}">
          {{ data.usuario.nombre.charAt(0).toUpperCase() }}
        </div>
        <div class="user-main-info">
          <h2>{{ data.usuario.nombre }} {{ data.usuario.apellido || '' }}</h2>
          <p class="user-email">{{ data.usuario.email }}</p>
          <div class="badges">
            <mat-chip-option [selected]="true" [color]="data.rolNombre === 'ADMIN' ? 'warn' : 'accent'">
              {{ data.rolNombre }}
            </mat-chip-option>
            <span class="status-badge" [ngClass]="data.usuario.activo ? 'active' : 'inactive'">
              {{ data.usuario.activo ? 'Cuenta Activa' : 'Cuenta Inactiva' }}
            </span>
          </div>
        </div>
      </div>

      <mat-divider class="divider"></mat-divider>

      <div class="detail-grid">
        <div class="detail-item">
          <mat-icon class="icon">badge</mat-icon>
          <div>
            <label>ID de Usuario</label>
            <span>#{{ data.usuario.id }}</span>
          </div>
        </div>

        <div class="detail-item">
          <mat-icon class="icon">phone</mat-icon>
          <div>
            <label>Teléfono</label>
            <span>{{ data.usuario.telefono || 'No registrado' }}</span>
          </div>
        </div>

        <div class="detail-item">
          <mat-icon class="icon">event</mat-icon>
          <div>
            <label>Fecha de Creación</label>
            <span>{{ (data.usuario.created_at || data.usuario.fechacreacion) | date:'dd/MM/yyyy HH:mm' }}</span>
          </div>
        </div>

        <div class="detail-item">
          <mat-icon class="icon">security</mat-icon>
          <div>
            <label>Permisos de Acceso</label>
            <span>{{ data.rolNombre === 'ADMIN' ? 'Acceso Total Administrador' : 'Acceso Restringido según Rol' }}</span>
          </div>
        </div>
      </div>

      <mat-dialog-actions align="end" class="actions">
        <button mat-raised-button color="primary" (click)="onClose()">Cerrar</button>
      </mat-dialog-actions>
    </div>
  `,
  styles: [`
    .user-detail-container {
      padding: 8px 4px;
      min-width: 440px;
    }
    .user-header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 16px;
    }
    .avatar-large {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: linear-gradient(135deg, #6366f1, #4f46e5);
      color: white;
      font-size: 2rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .avatar-inactive {
      background: #94a3b8 !important;
    }
    .user-main-info h2 {
      margin: 0;
      font-weight: 700;
      font-size: 1.3rem;
      color: #0f172a;
    }
    .user-email {
      margin: 2px 0 8px 0;
      color: #64748b;
      font-size: 0.9rem;
    }
    .badges {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .status-badge {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 20px;
    }
    .status-badge.active {
      background-color: #dcfce7;
      color: #166534;
    }
    .status-badge.inactive {
      background-color: #fee2e2;
      color: #991b1b;
    }
    .divider {
      margin: 16px 0;
    }
    .detail-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }
    .detail-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      background: #f8fafc;
      padding: 12px;
      border-radius: 10px;
      border: 1px solid #f1f5f9;
    }
    .detail-item .icon {
      color: #6366f1;
    }
    .detail-item label {
      display: block;
      font-size: 0.75rem;
      color: #94a3b8;
      text-transform: uppercase;
      font-weight: 600;
    }
    .detail-item span {
      font-size: 0.9rem;
      font-weight: 600;
      color: #334155;
    }
    .actions {
      padding-top: 12px;
      margin: 0;
    }
  `]
})
export class UserDetailDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<UserDetailDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: UserDetailDialogData
  ) {}

  onClose(): void {
    this.dialogRef.close();
  }
}
