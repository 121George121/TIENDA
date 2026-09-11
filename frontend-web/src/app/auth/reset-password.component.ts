import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../core/services/auth.service';

function passwordComplexityValidator(control: AbstractControl): ValidationErrors | null {
  const v = control.value || '';
  if (!v) return null;

  const hasMinLength = v.length >= 8;
  const hasUpper = /[A-Z]/.test(v);
  const hasLower = /[a-z]/.test(v);
  const hasNumber = /[0-9]/.test(v);
  const hasSpecial = /[\W_]/.test(v);

  const valid = hasMinLength && hasUpper && hasLower && hasNumber && hasSpecial;
  return valid ? null : { passwordComplexity: true };
}

function passwordMatchValidator(group: AbstractControl): ValidationErrors | null {
  const pass = group.get('newPassword')?.value;
  const confirm = group.get('confirmPassword')?.value;
  return pass === confirm ? null : { passwordMismatch: true };
}

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  template: `
    <div class="auth-container">
      <div class="auth-left">
        <div class="brand-overlay">
          <h1>E-Commerce Tienda</h1>
          <p class="tagline">Restablecer Contraseña</p>
        </div>
      </div>
      
      <div class="auth-right">
        <div class="auth-card">
          <div class="auth-header">
            <h2>Restablecer Contraseña</h2>
            <p>Ingresa tu nueva contraseña para actualizar tu cuenta.</p>
          </div>

          <div *ngIf="successMessage" class="alert alert-success">
            {{ successMessage }}
            <div style="margin-top: 15px;">
              <a routerLink="/login" class="btn-primary" style="display: inline-block; text-align: center; text-decoration: none;">Ir al Inicio de Sesión</a>
            </div>
          </div>
          
          <div *ngIf="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <form *ngIf="!successMessage" [formGroup]="resetForm" (ngSubmit)="onSubmit()" class="auth-form">
            <div class="form-group">
              <label for="token">Token de Recuperación</label>
              <div class="input-container">
                <input 
                  type="text" 
                  id="token" 
                  formControlName="token" 
                  placeholder="Pega tu token aquí"
                >
              </div>
              <small *ngIf="resetForm.get('token')?.touched && resetForm.get('token')?.invalid" class="error-text">
                El token es requerido.
              </small>
            </div>

            <div class="form-group">
              <label for="newPassword">Nueva Contraseña</label>
              <div class="input-container">
                <input 
                  type="password" 
                  id="newPassword" 
                  formControlName="newPassword" 
                  placeholder="Mínimo 8 caract., 1 Mayús, 1 Num, 1 Esp."
                >
              </div>
              <small *ngIf="resetForm.get('newPassword')?.touched && resetForm.get('newPassword')?.errors?.['passwordComplexity']" class="error-text">
                La contraseña debe tener mín. 8 caracteres, incluir mayúscula, minúscula, número y carácter especial (ej. Admin123.).
              </small>
            </div>

            <div class="form-group">
              <label for="confirmPassword">Confirmar Nueva Contraseña</label>
              <div class="input-container">
                <input 
                  type="password" 
                  id="confirmPassword" 
                  formControlName="confirmPassword" 
                  placeholder="Repite la nueva contraseña"
                >
              </div>
              <small *ngIf="resetForm.touched && resetForm.errors?.['passwordMismatch']" class="error-text">
                Las contraseñas no coinciden.
              </small>
            </div>

            <button type="submit" class="btn-primary" [disabled]="isLoading || resetForm.invalid">
              <span *ngIf="!isLoading">Cambiar Contraseña</span>
              <span *ngIf="isLoading" class="spinner"></span>
            </button>
          </form>

          <div class="auth-footer">
            <p><a routerLink="/login">Volver a inicio de sesión</a></p>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./login/login.component.css']
})
export class ResetPasswordComponent implements OnInit {
  resetForm: FormGroup;
  isLoading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder, 
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.resetForm = this.fb.group({
      token: ['', [Validators.required]],
      newPassword: ['', [Validators.required, passwordComplexityValidator]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: passwordMatchValidator });
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['token']) {
        this.resetForm.patchValue({ token: params['token'] });
      }
    });
  }

  onSubmit() {
    if (this.resetForm.invalid) {
      this.resetForm.markAllAsTouched();
      return;
    }
    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const { token, newPassword } = this.resetForm.value;

    this.authService.resetPassword(token, newPassword).subscribe({
      next: (res: any) => {
        this.isLoading = false;
        this.successMessage = res.mensaje || '¡Contraseña restablecida exitosamente!';
      },
      error: (err: any) => {
        this.isLoading = false;
        this.errorMessage = err.error?.detail || 'No se pudo restablecer la contraseña. Verifique que el token sea válido y no haya expirado.';
      }
    });
  }
}
