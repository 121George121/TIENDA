# 🚀 GUÍA SENIOR DE DESPLIEGUE EN LA NUBE - SHOPYN GOLDEN STORE
### Arquitectura 3-Tier: Supabase (DB) + Railway (Backend) + Vercel (Frontend)

Esta guía documenta la infraestructura en la nube para **Shopyn Golden Store**, garantizando alta disponibilidad, seguridad SSL de extremo a extremo y configuración en minutos sin costos (100% Free Tiers).

---

## 📐 Diagrama de Arquitectura

```
                        +---------------------------------------------+
                        |           USUARIOS / NAVEGADORES            |
                        +---------------------------------------------+
                                       |              |
                                 (HTTPS/Web)     (HTTPS/Móvil)
                                       v              v
+-------------------------------+              +--------------------------------+
|       VERCEL (Frontend)       |              |      FLUTTER (App Móvil)       |
| Angular 19 SPA                |              | Android / iOS                  |
| https://[tu-app].vercel.app   |              | ApiConfig.useCloud = true      |
+-------------------------------+              +--------------------------------+
               |                                               |
               +-----------------------+-----------------------+
                                       |
                                (REST API / JSON)
                                       v
                        +---------------------------------------------+
                        |              RAILWAY (Backend)              |
                        | FastAPI + Uvicorn (Python 3.11)            |
                        | https://[tu-api].up.railway.app            |
                        | Healthcheck: /health | Swagger: /docs       |
                        +---------------------------------------------+
                                       |
                           (PostgreSQL Pooler / SSL)
                                       v
                        +---------------------------------------------+
                        |             SUPABASE (Database)             |
                        | PostgreSQL 16 Administrado en AWS           |
                        | 27 Tablas | 23 Prendas con Fotos Cloud      |
                        | 69 Inventarios Multitienda | 20 Cuentas     |
                        +---------------------------------------------+
```

---

## 1️⃣ FASE 1: BASE DE DATOS EN SUPABASE

### Paso 1.1: Crear el Proyecto
1. Ingresa a [supabase.com](https://supabase.com) e inicia sesión (o crea cuenta con GitHub).
2. Haz clic en **"New Project"**.
3. Completa los datos:
   - **Name**: `shopyn-golden-store`
   - **Database Password**: Genera una contraseña segura y **anótala** (la necesitarás en la URL de conexión).
   - **Region**: Selecciona `South America (São Paulo)` para menor latencia en Bolivia/LATAM, o `US East (N. Virginia)`.
4. Haz clic en **"Create new project"** y espera ~1-2 minutos mientras Supabase provisiona tu instancia PostgreSQL.

### Paso 1.2: Cargar la Estructura y Datos (Backup Completo)
Tienes **dos opciones** súper sencillas:

#### Opción A (Desde el navegador con SQL Editor - Recomendada):
1. En tu panel de Supabase, en el menú izquierdo haz clic en el ícono de **SQL Editor** (o presiona `Ctrl + K` y escribe `SQL`).
2. Haz clic en **"New query"**.
3. Abre en tu editor el archivo [`backend/database/backup_completo.sql`](file:///c:/Users/HP/OneDrive/Escritorio/proyecto_tienda/TIENDA/backend/database/backup_completo.sql), copia todo su contenido (`Ctrl + A`, `Ctrl + C`) y pégalo en el editor de Supabase.
4. Haz clic en el botón verde **"Run"** (o presiona `Ctrl + Enter`).
5. Verás el mensaje `Success. No rows returned`. En 2 segundos habrás cargado todas las 27 tablas, prendas con fotos en la nube, usuarios, roles, inventarios y bitácora.

#### Opción B (Desde tu terminal con el script automatizado):
1. Copia tu cadena de conexión URI de Supabase (ver Paso 1.3).
2. En tu terminal dentro de la carpeta `backend`, ejecuta:
   ```bash
   python database/restaurar_base_datos.py --url "postgresql://postgres:[TU_PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres"
   ```
3. El script se conectará con SSL, cargará todos los datos y te mostrará el resumen en pantalla.

### Paso 1.3: Copiar la Cadena de Conexión para Railway
1. En Supabase, ve a **Project Settings** (ícono de engranaje) > **Database**.
2. Desplázate hasta la sección **Connection parameters** o **Connection string**.
3. Selecciona la pestaña **URI**.
4. Verás algo como:
   `postgresql://postgres.[PROJECT_REF]:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres`
   *(O la conexión directa en el puerto 5432)*.
5. Reemplaza `[YOUR-PASSWORD]` por la contraseña real que definiste en el Paso 1.1.

---

## 2️⃣ FASE 2: BACKEND EN RAILWAY

### Paso 2.1: Crear el Servicio en Railway
1. Ingresa a [railway.app](https://railway.app) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New Project"** (o **"+ New"**).
3. Selecciona **"Deploy from GitHub repo"**.
4. Elige tu repositorio: `121George121/TIENDA`.
5. Railway analizará el repositorio. Haz clic en el servicio recién creado y ve a la pestaña **"Settings"**.
6. En la sección **"Source / Root Directory"**:
   - Haz clic en **Edit**.
   - Escribe: `/backend`
   - Guarda los cambios (**Save**).

### Paso 2.2: Configurar Variables de Entorno
1. En el servicio de Railway, ve a la pestaña **"Variables"**.
2. Haz clic en **"New Variable"** y añade las siguientes:

| Variable | Valor | Descripción |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres` | URI copiada de Supabase en la Fase 1 |
| `SECRET_KEY` | `shopyn_ultra_secret_jwt_key_prod_2026_x89` | Llave secreta para tokens JWT |
| `ALGORITHM` | `HS256` | Algoritmo criptográfico de tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | 24 horas de vigencia de sesión |

> **Nota Senior:** No necesitas configurar `PORT`. Railway inyecta la variable `$PORT` dinámicamente y nuestro archivo `Procfile` / `railway.json` ya lo enlaza con `0.0.0.0:${PORT}` automáticamente.

### Paso 2.3: Generar Dominio Público HTTPS
1. En la pestaña **"Settings"** del servicio en Railway, desplázate hasta la sección **"Networking"**.
2. En **"Public Networking"**, haz clic en el botón **"Generate Domain"**.
3. Railway te generará un dominio seguro con certificado SSL automático, por ejemplo:
   `https://tienda-backend-production-xxxx.up.railway.app`
4. **Verificación inmediata:**
   - Abre en tu navegador: `https://[TU-DOMINIO-RAILWAY]/health` ➔ Debe responder `{"status":"healthy","service":"Shopyn Golden Store API"}`.
   - Abre: `https://[TU-DOMINIO-RAILWAY]/docs` ➔ Abrirá la interfaz interactiva de Swagger UI con todos los Casos de Uso (CU1 a CU20).

---

## 3️⃣ FASE 3: FRONTEND WEB EN VERCEL

### Paso 3.1: Importar el Proyecto en Vercel
1. Ingresa a [vercel.com](https://vercel.com) e inicia sesión con GitHub.
2. Haz clic en **"Add New..."** > **"Project"**.
3. Busca y selecciona el repositorio `TIENDA`.
4. Configuración del proyecto (**Configure Project**):
   - **Framework Preset**: Selecciona `Angular`.
   - **Root Directory**: Haz clic en **Edit** y selecciona `frontend-web`.
   - **Build and Output Settings**:
     - *Build Command*: `npm run build` (o `ng build`)
     - *Output Directory*: `dist/tienda-frontend/browser` *(Crítico para Angular 18/19)*
     - *Install Command*: `npm install`
5. Haz clic en **"Deploy"**.

### Paso 3.2: Conectar Vercel con la URL de Railway
Para que el frontend desplegado consuma tu backend de Railway:
1. En tu archivo local [`frontend-web/src/environments/environment.prod.ts`](file:///c:/Users/HP/OneDrive/Escritorio/proyecto_tienda/TIENDA/frontend-web/src/environments/environment.prod.ts), actualiza la URL con el dominio real de Railway:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://[TU-DOMINIO-RAILWAY]/api/v1'
   };
   ```
2. Haz un `git commit` y `git push`. Vercel detectará el push y volverá a compilar en 40 segundos automáticamente.

> **Tip Senior (Cambio en vivo sin re-compilar):**
> Nuestro frontend incluye detección dinámica. Si quieres probar al instante cualquier backend sin esperar el build de Vercel, abre la consola de desarrollador del navegador (`F12`) en tu página de Vercel y ejecuta:
> ```javascript
> localStorage.setItem('API_URL', 'https://[TU-DOMINIO-RAILWAY]/api/v1');
> location.reload();
> ```
> ¡La aplicación cambiará inmediatamente su conexión al nuevo backend!

---

## 4️⃣ FASE 4: APP MÓVIL (FLUTTER)

1. Abre [`mobile-app/lib/config/api_config.dart`](file:///c:/Users/HP/OneDrive/Escritorio/proyecto_tienda/TIENDA/mobile-app/lib/config/api_config.dart).
2. Actualiza la variable `cloudBaseUrl` con tu URL de Railway:
   ```dart
   static const bool useCloud = true; // <-- Cambiar a true
   static const String cloudBaseUrl = 'https://[TU-DOMINIO-RAILWAY]/api/v1';
   ```
3. ¡Listo! Ahora puedes instalar la APK en tu teléfono o ejecutar `flutter run` y funcionará con datos móviles (4G/5G) o cualquier red Wi-Fi en cualquier parte del mundo sin depender de tu PC.

---

## 5️⃣ VERIFICACIÓN INTEGRAL DE FUNCIONAMIENTO (CHECKLIST)

- [ ] **Supabase**: Las 27 tablas están creadas y la tabla `producto` tiene 23 prendas con fotos en `imagenprincipal`.
- [ ] **Railway**: El servicio está en estado `Active` / `Deployed` y el endpoint `/health` responde con código 200.
- [ ] **Railway Swagger**: Ingresar a `https://[railway-url]/docs`, autenticar en `/api/v1/auth/login` con `operador@boutique.com` / `admin123`.
- [ ] **Vercel**: El sitio carga en `https://[vercel-url]`, navega fluidamente a `/admin/pos`, `/catalogo` y `/admin/bitacora` sin errores 404 al recargar.
- [ ] **CORS**: Las peticiones de Vercel al backend de Railway se ejecutan con cabeceras `Access-Control-Allow-Origin: *`.
