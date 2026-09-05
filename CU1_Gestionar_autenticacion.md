# CU1: Gestionar Autenticación y Recuperación de Contraseña

> **Proyecto:** ECOMMERCE_TIENDA  
> **Patrón Arquitectónico:** MVC (Modelo - Vista - Controlador)  
> **Tecnologías:** FastAPI (Backend) | Angular (Web) | Flutter (Móvil) | PostgreSQL  

---

## 📋 1. Descripción del Caso de Uso

El caso de uso **CU1: Gestionar Autenticación** permite a los usuarios registrados (Clientes y Administradores) autenticarse de forma segura mediante JWT (JSON Web Tokens) y restablecer su contraseña en caso de olvido a través de un token temporal enviado a su correo electrónico.

### Sub-procesos Incluidos:
1. **CU1.1 - Iniciar Sesión (Login)**: Autenticación con email y contraseña, emisión de `access_token` y `refresh_token`.
2. **CU1.2 - Solicitar Recuperación de Contraseña**: Generación de token JWT temporal (15 min) y envío de correo SMTP vía Gmail.
3. **CU1.3 - Restablecer Contraseña**: Verificación del token y actualización de la contraseña hasheada (Bcrypt) en la base de datos PostgreSQL.

---

## 🏗️ 2. Arquitectura por Capas (Backend / Web / Móvil)

```
                       ┌──────────────────────────────┐
                       │    Clientes de Usuario       │
                       └──────────────┬───────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
   ┌──────────────────────┐                       ┌──────────────────────┐
   │   Web (Angular 17)   │                       │   Móvil (Flutter 3)  │
   │  - AuthService       │                       │  - AuthController    │
   │  - LoginComponent    │                       │  - LoginView         │
   │  - RecoverComponent  │                       │  - RecoverView       │
   │  - ResetComponent    │                       │  - ResetView         │
   └──────────┬───────────┘                       └──────────┬───────────┘
              │                                              │
              └───────────────────────┬──────────────────────┘
                                      │ REST API (HTTP/JSON)
                                      ▼
                       ┌──────────────────────────────┐
                       │   Backend (FastAPI - MVC)    │
                       ├──────────────────────────────┤
                       │ Vista: app/views/auth_views  │
                       │ Ctrl:  app/controllers/auth  │
                       │ Security: Bcrypt & JWT & SMTP│
                       └──────────────┬───────────────┘
                                      │ ORM (SQLAlchemy)
                                      ▼
                       ┌──────────────────────────────┐
                       │   Base de Datos PostgreSQL   │
                       └──────────────────────────────┘
```

---

## ⚙️ 3. Especificación Técnica por Plataforma

### 🅰️ Backend (FastAPI + PostgreSQL)
- **Rutas API (`app/views/auth_views.py`)**:
  - `POST /api/v1/auth/login`: Form-Data OAuth2 (`username`, `password`).
  - `POST /api/v1/auth/recuperar-password`: JSON (`email`).
  - `POST /api/v1/auth/reset-password`: JSON (`token`, `new_password`).
- **Controlador (`app/controllers/auth_controller.py`)**:
  - Validación de credenciales y estado activo del usuario.
  - Generación de hashes Bcrypt y verificación.
  - Firma y validación de tokens JWT.
- **Modelos y Esquemas (`app/models/models.py`, `app/schemas/schemas.py`)**:
  - Mapeo ORM `UsuarioModel` (`fechacreacion`, `rolid`).
  - Esquema Pydantic v2 `UsuarioResponse` con `AliasChoices` para compatibilidad completa.

---

### 🌐 Frontend Web (Angular 17)
- **Servicio Principal (`src/app/core/services/auth.service.ts`)**:
  - `login(email, password)`: Envía payload `application/x-www-form-urlencoded`.
  - `requestPasswordRecovery(email)`: Envía JSON con el correo destino.
  - `resetPassword(token, newPassword)`: Actualiza las credenciales.
- **Vistas y Componentes**:
  - `LoginComponent` (`/login`): Formulario reactivo con manejo de errores visuales.
  - `RecoverPasswordComponent` (`/recover-password`): Envío de instrucciones por correo.
  - `ResetPasswordComponent` (`/reset-password`): Captura del token vía parámetro `?token=` y validación de complejidad en tiempo real.

---

### 📱 App Móvil (Flutter 3)
- **Modelo (`lib/models/user_model.dart`)**:
  - Mapeo de JSON a objeto Dart `UserModel` incluyendo tokens y datos del usuario.
- **Controlador (`lib/controllers/auth_controller.dart`)**:
  - `ChangeNotifier` para gestión de estado global reactivo mediante `Provider`.
  - Resolución dinámica de IP (`http://10.0.2.2:8000` para Android Emulator, `localhost` para Desktop/iOS/Web).
- **Vistas (`lib/views/`)**:
  - `LoginView`: Interfaz móvil con Material 3, ocultamiento de contraseña y feedback con `SnackBar`.
  - `RecoverPasswordView`: Formulario móvil para solicitar token por correo.
  - `ResetPasswordView`: Interfaz de cambio de contraseña con validación estricta de seguridad.

---

## 🔒 4. Reglas de Validación de Contraseña
Para garantizar la máxima seguridad en todos los clientes (Web y Móvil), las nuevas contraseñas deben cumplir:
- Mínimo **8 caracteres**.
- Al menos **1 letra mayúscula** (`A-Z`).
- Al menos **1 letra minúscula** (`a-z`).
- Al menos **1 número** (`0-9`).
- Al menos **1 carácter especial** (`!@#$%^&*` etc.).

---

## 🧪 5. Verificación de Funcionamiento (Pruebas Realizadas)

| Caso de Prueba | Resultado | Detalle |
| :--- | :---: | :--- |
| **Login Exitoso** | ✅ PASÓ | Retorna JWT token, datos de usuario y rol. |
| **Login Credenciales Incorrectas** | ✅ PASÓ | Retorna HTTP 401 "Credenciales incorrectas". |
| **Solicitud de Recuperación** | ✅ PASÓ | Envía correo HTML/Texto vía Gmail SMTP en puerto 465. |
| **Restablecer Contraseña con Token** | ✅ PASÓ | Actualiza hash en PostgreSQL y permite inicio de sesión inmediato. |
