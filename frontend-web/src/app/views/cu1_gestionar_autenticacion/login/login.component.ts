import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm: FormGroup;
  isLoading = false;
  errorMessage = '';
  showPassword = false;

  constructor(
    private fb: FormBuilder, 
    private router: Router,
    private authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }
    this.isLoading = true;
    this.errorMessage = '';
    
    const { email, password } = this.loginForm.value;

    this.authService.login(email, password).subscribe({
      next: (response) => {
        this.isLoading = false;
        
        const token = response.access_token;
        const userStr = JSON.stringify(response.usuario);
        const rol = response.rol || (response.usuario && response.usuario.rol ? response.usuario.rol.nombre : 'CLIENTE');

        // Guardar todas las llaves posibles para compatibilidad
        localStorage.setItem('access_token', token);
        localStorage.setItem('token', token);
        localStorage.setItem('usuario', userStr);
        localStorage.setItem('user', userStr);
        localStorage.setItem('rol', rol);
        localStorage.setItem('user_role', rol);
        
        // Redirigir según el rol
        const rolUpper = (rol || '').toUpperCase();
        if (rolUpper === 'ADMIN' || rolUpper === 'ADMINISTRADOR') {
          this.router.navigate(['/admin/users']);
        } else {
          this.router.navigate(['/catalogo']);
        }
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error de login:', err);
        this.errorMessage = err.error?.detail || 'Error al iniciar sesión. Verifique sus credenciales.';
      }
    });
  }
}
