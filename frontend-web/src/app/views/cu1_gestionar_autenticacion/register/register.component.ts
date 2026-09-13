import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../services/cu1_gestionar_autenticacion/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  otpForm: FormGroup;
  
  step: 'FORM' | 'OTP' = 'FORM';
  isLoading = false;
  errorMessage = '';
  successMessage = '';
  registeredEmail = '';
  demoOtpCode = '';
  showPassword = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      apellido: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.pattern('^[0-9+ ]{7,15}$')]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });

    this.otpForm = this.fb.group({
      codigo: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(6)]]
    });
  }

  passwordMatchValidator(g: FormGroup) {
    const pass = g.get('password')?.value;
    const confirm = g.get('confirmPassword')?.value;
    return pass === confirm ? null : { mismatch: true };
  }

  onRegisterSubmit(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const val = this.registerForm.value;
    const payload = {
      nombre: val.nombre.trim(),
      apellido: val.apellido.trim(),
      email: val.email.trim().toLowerCase(),
      telefono: val.telefono ? val.telefono.trim() : '',
      password: val.password
    };

    this.authService.registro(payload).subscribe({
      next: (res: any) => {
        this.isLoading = false;
        this.registeredEmail = payload.email;
        this.demoOtpCode = res.codigo_demo || '';
        this.step = 'OTP';
        this.successMessage = '¡Código de verificación enviado! Revisa tu correo o usa el código de prueba.';
      },
      error: (err: any) => {
        this.isLoading = false;
        this.errorMessage = err.error?.detail || 'No se pudo completar el registro. Verifica los datos.';
      }
    });
  }

  onOtpSubmit(): void {
    if (this.otpForm.invalid) {
      this.otpForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const codigo = this.otpForm.get('codigo')?.value.trim();

    this.authService.verificarCodigo(this.registeredEmail, codigo).subscribe({
      next: (res: any) => {
        this.isLoading = false;
        if (res.access_token) {
          localStorage.setItem('access_token', res.access_token);
        }
        alert('¡Cuenta verificada con éxito! Bienvenido a la plataforma.');
        this.router.navigate(['/catalogo']);
      },
      error: (err: any) => {
        this.isLoading = false;
        this.errorMessage = err.error?.detail || 'Código de verificación incorrecto o expirado.';
      }
    });
  }

  autoFillDemoOtp(): void {
    if (this.demoOtpCode) {
      this.otpForm.patchValue({ codigo: this.demoOtpCode });
    }
  }
}
