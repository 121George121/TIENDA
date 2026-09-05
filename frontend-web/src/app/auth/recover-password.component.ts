import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AuthService } from '../core/services/auth.service';

@Component({
  selector: 'app-recover-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  template: `
    <div class="auth-container">
      <div class="auth-left">
        <div class="brand-overlay">
          <h1>E-Commerce Tienda</h1>
          <p class="tagline">Premium T-Shirts & Apparel</p>
        </div>
      </div>
      
      <div class="auth-right">
        <div class="auth-card">
          <div class="auth-header">
            <h2>Recuperar Contraseña</h2>
            <p>Ingresa tu correo para enviarte las instrucciones.</p>
          </div>

          <div *ngIf="successMessage" class="alert alert-success">
            {{ successMessage }}
          </div>
          
          <div *ngIf="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <form *ngIf="!successMessage" [formGroup]="recoverForm" (ngSubmit)="onSubmit()" class="auth-form">
            <div class="form-group">
              <label for="email">Correo Electrónico</label>
              <div class="input-container">
                <input 
                  type="email" 
                  id="email" 
                  formControlName="email" 
                  placeholder="tu@correo.com"
                >
              </div>
            </div>

            <button type="submit" class="btn-primary" [disabled]="isLoading">
              <span *ngIf="!isLoading">Enviar Instrucciones</span>
              <span *ngIf="isLoading" class="spinner"></span>
            </button>
          </form>

          <div class="auth-footer">
            <p>¿Recordaste tu contraseña? <a routerLink="/login">Volver a inicio de sesión</a></p>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./login/login.component.css']
})
export class RecoverPasswordComponent {
  recoverForm: FormGroup;
  isLoading = false;
  successMessage = '';
  errorMessage = '';

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.recoverForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onSubmit() {
    if (this.recoverForm.invalid) return;
    this.isLoading = true;
    this.errorMessage = '';
    
    this.authService.requestPasswordRecovery(this.recoverForm.value.email).subscribe({
      next: (res: any) => {
        this.isLoading = false;
        this.successMessage = res.mensaje;
      },
      error: (err: any) => {
        this.isLoading = false;
        this.errorMessage = err.error?.detail || 'No se pudo procesar la solicitud.';
      }
    });
  }
}
