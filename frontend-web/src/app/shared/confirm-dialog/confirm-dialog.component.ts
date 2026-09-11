import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

export interface ConfirmDialogData {
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  icon?: string;
  color?: 'warn' | 'primary' | 'accent';
}

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule, MatDialogModule, MatButtonModule, MatIconModule],
  template: `
    <div class="confirm-dialog-container">
      <div class="header-icon" [ngClass]="data.color || 'warn'">
        <mat-icon>{{ data.icon || 'warning' }}</mat-icon>
      </div>
      <h2 mat-dialog-title class="title">{{ data.title }}</h2>
      <mat-dialog-content class="content">
        <p>{{ data.message }}</p>
      </mat-dialog-content>
      <mat-dialog-actions align="end" class="actions">
        <button mat-button (click)="onCancel()">{{ data.cancelText || 'Cancelar' }}</button>
        <button mat-raised-button [color]="data.color || 'warn'" (click)="onConfirm()">
          {{ data.confirmText || 'Confirmar' }}
        </button>
      </mat-dialog-actions>
    </div>
  `,
  styles: [`
    .confirm-dialog-container {
      padding: 12px 8px;
      text-align: center;
    }
    .header-icon {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16px auto;
    }
    .header-icon mat-icon {
      font-size: 32px;
      width: 32px;
      height: 32px;
    }
    .header-icon.warn {
      background-color: #fee2e2;
      color: #dc2626;
    }
    .header-icon.primary {
      background-color: #e0e7ff;
      color: #4f46e5;
    }
    .title {
      font-weight: 700;
      font-size: 1.25rem;
      color: #0f172a;
      margin-bottom: 8px;
    }
    .content p {
      color: #64748b;
      font-size: 0.95rem;
      margin: 0;
    }
    .actions {
      margin-top: 24px;
      padding-bottom: 0;
    }
  `]
})
export class ConfirmDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ConfirmDialogData
  ) {}

  onConfirm(): void {
    this.dialogRef.close(true);
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}
