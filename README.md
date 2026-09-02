# 🛒 E-Commerce System (FastAPI + Angular + PostgreSQL + Flutter)

Este proyecto implementa un sistema completo de **Tienda Virtual / E-Commerce** multi-plataforma organizado bajo el patrón de arquitectura **Modelo-Vista-Controlador (MVC)** para facilitar su comprensión y estudio académico.

---

## 🏗️ Arquitectura General del Sistema

```
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
| - Controller: ProductService    |      | - Controller: ProductController   |
| - View: HTML/CSS Components     |      | - View: Flutter Widget Screens    |
+---------------------------------+      +-----------------------------------+
```

PROYECTO_SI2_EXAMEN/
├── backend/                    # ⚡ BACKEND (FastAPI - Python + Base de Datos)
│   ├── database/               # 🗄️ BASE DE DATOS (PostgreSQL)
│   │   └── init.sql            # Script DDL (Tablas, Claves Foráneas y Semilla)
│   ├── app/
│   │   ├── models/             # 🔹 MODEL: Clases ORM (SQLAlchemy)
│   │   │   └── models.py
│   │   ├── schemas/            # Schemas de Validación Pydantic (DTOs)
│   │   │   └── schemas.py
│   │   ├── controllers/        # 🔹 CONTROLLER: Lógica de negocio y transacciones DB
│   │   │   ├── product_controller.py
│   │   │   ├── order_controller.py
│   │   │   └── auth_controller.py
│   │   ├── views/              # 🔹 VIEW: Endpoints REST (FastAPI Routers -> JSON Views)
│   │   │   ├── product_views.py
│   │   │   ├── order_views.py
│   │   │   └── auth_views.py
│   │   ├── core/               # Conexión DB y Configuración
│   │   └── main.py             # Punto de entrada de FastAPI
│   ├── requirements.txt
│   └── .env.example
├── frontend-web/               # 🅰️ FRONTEND WEB (Angular)
│   └── src/app/
│       ├── models/             # 🔹 MODEL: Interfaces TypeScript (`product.model.ts`, `cart.model.ts`)
│       ├── controllers/        # 🔹 CONTROLLER: Servicios de Estado y HTTP (`product.service.ts`)
│       └── views/              # 🔹 VIEW: Componentes HTML/CSS (`product-catalog.component.html/ts/css`)
├── mobile-app/                 # 📱 APP MÓVIL (Flutter / Dart)
│   └── lib/
│       ├── models/             # 🔹 MODEL: Clases Dart y Deserialización JSON (`product_model.dart`)
│       ├── controllers/        # 🔹 CONTROLLER: State Controllers con ChangeNotifier (`product_controller.dart`)
│       └── views/              # 🔹 VIEW: Pantallas / Widgets (`product_list_view.dart`, `cart_view.dart`)
└── README.md                   # 📖 Documentación explicativa completa del Patrón MVC

---

## 📚 Mapeo Detallado del Patrón MVC

### 1. 🗄️ Base de Datos (PostgreSQL)
* Archivo: `backend/database/init.sql`
* Define el esquema relacional con tablas para `usuarios`, `roles`, `categorias`, `productos`, `ordenes` y `orden_detalles`.

---

### 2. ⚡ Backend: FastAPI (Python)
* Ubicación: `backend/app/`

| Componente MVC | Capa en FastAPI | Descripción y Archivos |
| :--- | :--- | :--- |
| **Modelo (Model)** | `app/models/models.py` | Clases ORM de SQLAlchemy que mapean exactamente a las tablas de PostgreSQL. |
| **Controlador (Controller)** | `app/controllers/` | Contiene la **lógica de negocio**, validaciones de stock, cálculo de totales de orden y transacciones DB. (`product_controller.py`, `order_controller.py`, `auth_controller.py`). |
| **Vista (View)** | `app/views/` | Endpoints REST de FastAPI (`APIRouter`) que envían y reciben JSON desde los clientes web y móviles. (`product_views.py`, `order_views.py`, `auth_views.py`). |

---

### 3. 🅰️ Frontend Web: Angular (TypeScript)
* Ubicación: `frontend-web/`

| Componente MVC | Capa en Angular | Descripción y Archivos |
| :--- | :--- | :--- |
| **Modelo (Model)** | `src/app/models/` | Interfaces TypeScript que definen la forma de los objetos. (`product.model.ts`, `cart.model.ts`). |
| **Controlador (Controller)** | `src/app/controllers/` | Servicios de Angular (`ProductControllerService`) encargados de realizar las llamadas HTTP a FastAPI y manejar el estado del Carrito. |
| **Vista (View)** | `src/app/views/` | Componentes de la interfaz de usuario con plantillas HTML y estilos CSS. (`product-catalog.component.html/ts/css`). |

---

### 4. 📱 App Móvil: Flutter (Dart)
* Ubicación: `mobile-app/`

| Componente MVC | Capa en Flutter | Descripción y Archivos |
| :--- | :--- | :--- |
| **Modelo (Model)** | `lib/models/` | Clases Dart con métodos de serialización JSON `fromJson` / `toJson`. (`product_model.dart`, `cart_item_model.dart`). |
| **Controlador (Controller)** | `lib/controllers/` | Controladores de estado `ChangeNotifier` (`ProductController`, `CartController`) que conectan con la API y refrescan la UI. |
| **Vista (View)** | `lib/views/` | Pantallas y Widgets reactivos de la app móvil (`product_list_view.dart`, `cart_view.dart`). |

---

## 🚀 Guía de Ejecución

### 1️⃣ Ejecutar la Base de Datos (PostgreSQL)
Asegúrate de tener PostgreSQL corriendo e importa la estructura:
```bash
psql -U postgres -d ecommerce_db -f database/init.sql
```

### 2️⃣ Ejecutar el Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
> Documentación interactiva de la API disponible en: `http://localhost:8000/docs`

### 3️⃣ Ejecutar el Frontend Web (Angular)
```bash
cd frontend-web
npm install
ng serve --open
```

### 4️⃣ Ejecutar la App Móvil (Flutter)
```bash
cd mobile-app
flutter pub get
flutter run
```

---

## 📌 Resumen de Cambios Git
Todos los componentes han sido creados de forma modular para fácil estudio.
- Commit local registrado en la rama `main`.
- Origen remoto enlazado a: `https://github.com/DiogoMars777/ECOMMERCE_TIENDA.git`.
