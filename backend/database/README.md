# 🛍️ Base de Datos - Shopyn Golden Store

Este directorio contiene el respaldo completo y las herramientas automatizadas para sincronizar y restaurar la base de datos PostgreSQL con **todos los datos actuales**, prendas, variantes, stock multitienda, categorías y links de imágenes en la nube.

---

## 📁 Archivos Disponibles

* **`backup_completo.sql`**: Volcado SQL completo (DDL + DML) con todas las 27 tablas, claves foráneas, secuencias y datos cargados (compatible con PostgreSQL 14, 15, 16 y 17).
* **`restaurar_base_datos.py`**: Script inteligente en Python que detecta la configuración, crea la base de datos si no existe, carga los datos y valida el contenido.
* **`restaurar_base_datos.bat`**: Script para Windows de **1 solo clic** para ejecutar la restauración sin usar la consola.

---

## 🚀 ¿Cómo restaurar la base de datos en tu computadora?

### Opción 1: En Windows con 1 Clic (Recomendada)
Haz doble clic sobre el archivo:
```
backend/database/restaurar_base_datos.bat
```
¡Y listo! El script detectará el entorno virtual o el Python instalado, creará `ecommerce_db` y cargará todas las prendas e inventarios.

---

### Opción 2: Desde la Terminal con Python
En tu terminal, dentro de la carpeta `backend`:
```bash
python database/restaurar_base_datos.py
```
O usando el entorno virtual:
```bash
.\venv\Scripts\python.exe database\restaurar_base_datos.py
```

---

### Opción 3: Con la herramienta `psql` de PostgreSQL
Si prefieres restaurar manualmente desde la línea de comandos de PostgreSQL:
```bash
psql -U postgres -d ecommerce_db -f backend/database/backup_completo.sql
```

---

## 📊 Datos Incluidos en el Respaldo

* **Poleras y Prendas:** 23 productos completos con fotos reales en la nube (PostImage/ImgBB).
* **Variantes de Producto:** 23 variantes vinculadas por talla (S, M, L, XL, XXL) y color.
* **Inventario Multitienda:** 69 registros de stock repartidos en las 3 sucursales:
  * Sucursal Central (Principal)
  * Sucursal Equipetrol
  * Sucursal Norte
* **Usuarios y Roles:** 20 usuarios (Administradores, Cajeros, Clientes) con contraseñas encriptadas con bcrypt.
* **Métodos de Pago:** Efectivo, Tarjeta Visa/Mastercard, QR Simple y PayPal.
* **Bitácora del Sistema (CU20):** 51 registros de auditoría y rastreo de operadores en Hora Boliviana (BOT).
