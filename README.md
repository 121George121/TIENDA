# 🛒 T-Shirt Boutique ERP & E-Commerce System
## (FastAPI + PostgreSQL + Angular + Flutter)

Bienvenido al repositorio del proyecto **T-Shirt Boutique ERP & E-Commerce System**. Este sistema es una plataforma completa multi-plataforma para la gestión ERP web y la venta minorista móvil de ropa boutique, construida bajo el patrón de arquitectura **Modelo-Vista-Controlador (MVC)**.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado el siguiente software en tu equipo:

- **PostgreSQL** (v14 o superior)
- **Python** (v3.10 o superior)
- **Node.js** (v18 o superior) y `npm`
- **Flutter SDK** (v3.19 o superior) y **Android Studio** (con Emulador Android o dispositivo físico)
- **Git**

---

## 🏗️ Arquitectura General del Sistema (MVC)

```text
                               +-----------------------------------+
                               |      PostgreSQL Database          |
                               |  (Tablas, Claves, Relaciones)     |
                               +-----------------------------------+
                                                ^
                                                | SQLAlchemy ORM
                                                v
      +-----------------------------------------------------------------------------------+
      |                            FASTAPI BACKEND (Python)                               |
      |                                                                                   |
      |   +-----------------------+     +--------------------------+     +------------+   |
      |   |   MODEL (Modelos)     | <-> | CONTROLLER (Controlador) | <-> | VIEW (API) |   |
      |   | app/models/models.py  |     | app/controllers/         |     | app/views/ |   |
      |   +-----------------------+     +--------------------------+     +------------+   |
      +------------------------------------------------------------------------^----------+
                                                                               |
                                                       HTTP / REST (JSON API)  |
                                             +---------------------------------+
                                             |
                         +-------------------+-------------------+
                         |                                       |
      +------------------v--------------+      +-----------------v-----------------+
      |     ANGULAR WEB FRONTEND        |      |     FLUTTER MOBILE APP (Dart)     |
      |                                 |      |                                   |
      | - Model: TypeScript Interfaces  |      | - Model: Dart Data Classes        |
      | - Controller: Angular Services  |      | - Controller: State Controllers   |
      | - View: Material Components     |      | - View: Flutter Widget Screens    |
      +---------------------------------+      +-----------------------------------+
```

---

## 🚀 Guía de Instalación y Levantamiento Paso a Paso

### 1️⃣ Base de Datos (PostgreSQL)

1. Abre tu gestor de base de datos (DBeaver, pgAdmin o terminal `psql`).
2. Crea la base de datos llamada `ecommerce_db`:
   ```sql
   CREATE DATABASE ecommerce_db;
   ```
3. Ejecuta el script de inicialización con las tablas y datos iniciales:
   ```bash
   psql -U postgres -d ecommerce_db -f backend/database/init.sql
   ```

---

### 2️⃣ Backend (FastAPI - Python)

1. Entra a la carpeta del backend:
   ```bash
   cd backend
   ```
2. (Opcional recomendado) Crea y activa un entorno virtual:
   - **En Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **En Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Instala todas las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura el archivo de variables de entorno `.env` en la carpeta `backend/`:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecommerce_db
   SECRET_KEY=TU_CLAVE_SECRETA_SUPER_SEGURA
   SMTP_USER=tu_correo@gmail.com
   SMTP_PASSWORD=tu_app_password
   ```
5. Inicia el servidor backend FastAPI:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   > 🌐 **API REST activa en**: `http://localhost:8000`  
   > 📑 **Documentación interactiva Swagger**: `http://localhost:8000/docs`

---

### 3️⃣ Frontend Web (Angular)

1. Entra a la carpeta del frontend web:
   ```bash
   cd frontend-web
   ```
2. Instala los paquetes y dependencias de Node.js:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo de Angular:
   ```bash
   npm start
   ```
   > 🌐 **Aplicación Web ERP activa en**: `http://localhost:4200`

---

### 4️⃣ App Móvil (Flutter / Dart)

1. Entra a la carpeta de la app móvil:
   ```bash
   cd mobile-app
   ```
2. Descarga las dependencias de Flutter:
   ```bash
   flutter pub get
   ```
3. Asegúrate de tener un emulador Android o dispositivo móvil conectado:
   ```bash
   flutter devices
   ```
4. Ejecuta la aplicación móvil:
   ```bash
   flutter run
   ```

---

## 🛠️ Estructura del Código del Proyecto

```text
PROYECTO_SI2_EXAMEN/
├── backend/                    # ⚡ BACKEND (FastAPI - Python + PostgreSQL)
│   ├── database/               # 🗄️ Script DDL (init.sql)
│   ├── app/
│   │   ├── models/             # ORM SQLAlchemy
│   │   ├── schemas/            # DTOs y validaciones Pydantic
│   │   ├── controllers/        # Lógica de negocio (Auth, Clientes, Productos, etc.)
│   │   ├── views/              # Endpoints API REST (FastAPI Routers)
│   │   └── main.py             # Entrada principal del servidor
│   ├── requirements.txt        # Dependencias de Python
│   └── .env                    # Variables de entorno
├── frontend-web/               # 🅰️ FRONTEND WEB (Angular)
│   └── src/app/
│       ├── models/             # Interfaces TypeScript
│       ├── controllers/        # Servicios HTTP Angular
│       └── views/              # Componentes UI (Dashboard, Clientes, Poleras, etc.)
├── mobile-app/                 # 📱 APP MÓVIL (Flutter / Dart)
│   └── lib/
│       ├── models/             # Clases de datos Dart (fromJson / toJson)
│       ├── controllers/        # State Controllers (ChangeNotifier / Provider)
│       └── views/              # Pantallas (Login, Registro, OTP, Catálogo)
└── README.md                   # 📖 Guía completa para desarrolladores
```

---

## 🔐 Características Clave de Seguridad Implementadas
- **Hashing de Contraseñas y OTP**: Hashing seguro con `Bcrypt` para contraseñas de usuario y códigos de verificación OTP de 6 dígitos.
- **Autenticación JWT**: Tokens `access_token` y `refresh_token` firmados criptográficamente.
- **Verificación de Correo Case-Insensitive**: Prevención estricta de cuentas duplicadas y re-envío de códigos OTP para cuentas no verificadas.

---

## 🤝 Repositorio Remoto en GitHub
- **URL del Repositorio**: [https://github.com/DiogoMars777/ECOMMERCE_TIENDA.git](https://github.com/DiogoMars777/ECOMMERCE_TIENDA.git)
- **Rama Principal**: `main`
