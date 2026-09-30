-- ==============================================================================
-- ACTUALIZACIÓN DE VARIANTES MULTICOLOR Y STOCK DIFERENCIADO POR SUCURSAL
-- Proyecto: ECOMMERCE_TIENDA (Shopyn Golden Store)
-- Base de Datos: PostgreSQL 16 (Supabase / AWS)
-- ==============================================================================

BEGIN;

-- 1. Asegurar catálogo de 10 colores con códigos HEX
INSERT INTO public.color (id, nombre, codigohex, activo) VALUES
  (1, 'Verde Oriente', '#007A3D', true),
  (2, 'Blanco Tajibo', '#FFFFFF', true),
  (3, 'Negro Azabache', '#111827', true),
  (4, 'Azul Marino Camba', '#1E3A8A', true),
  (5, 'Beige Chiquitano', '#D4B996', true),
  (6, 'Terracota Guarayos', '#B45309', true),
  (7, 'Gris Melange Urbano', '#64748B', true),
  (8, 'Amarillo Patujú', '#F59E0B', true),
  (9, 'Verde Olivo Chaco', '#556B2F', true),
  (10, 'Rojo Borgoña', '#991B1B', true)
ON CONFLICT (id) DO UPDATE SET
  nombre = EXCLUDED.nombre,
  codigohex = EXCLUDED.codigohex,
  activo = EXCLUDED.activo;

-- 2. Asegurar tallas estándar S, M, L, XL
INSERT INTO public.talla (id, nombre, grupoedad, orden, activo) VALUES
  (1, 'S', 'Adultos', 1, true),
  (2, 'M', 'Adultos', 2, true),
  (3, 'L', 'Adultos', 3, true),
  (4, 'XL', 'Adultos', 4, true)
ON CONFLICT (id) DO UPDATE SET
  nombre = EXCLUDED.nombre,
  orden = EXCLUDED.orden,
  activo = EXCLUDED.activo;

-- 3. Actualizar la primera variante de cada producto (IDs 1 a 23) con color y talla adecuados
UPDATE public.variante_producto SET colorid = 3, tallaid = 2, sku = 'POL-1-3-2' WHERE id = 1;   -- Canguro: Negro M
UPDATE public.variante_producto SET colorid = 4, tallaid = 2, sku = 'POL-2-4-2' WHERE id = 2;   -- Dep: Azul Marino M
UPDATE public.variante_producto SET colorid = 8, tallaid = 2, sku = 'POL-3-8-2' WHERE id = 3;   -- Grad: Amarillo M
UPDATE public.variante_producto SET colorid = 1, tallaid = 2, sku = 'POL-4-1-2' WHERE id = 4;   -- Grad V: Verde M
UPDATE public.variante_producto SET colorid = 4, tallaid = 2, sku = 'POL-5-4-2' WHERE id = 5;   -- Dyn: Azul Marino M
UPDATE public.variante_producto SET colorid = 2, tallaid = 2, sku = 'POL-6-2-2' WHERE id = 6;   -- Mangas: Blanco M
UPDATE public.variante_producto SET colorid = 2, tallaid = 1, sku = 'POL-7-2-1' WHERE id = 7;   -- Floral: Blanco S
UPDATE public.variante_producto SET colorid = 2, tallaid = 2, sku = 'POL-8-2-2' WHERE id = 8;   -- Estampada: Blanco M
UPDATE public.variante_producto SET colorid = 3, tallaid = 2, sku = 'POL-9-3-2' WHERE id = 9;   -- Mano: Negro M
UPDATE public.variante_producto SET colorid = 3, tallaid = 2, sku = 'POL-10-3-2' WHERE id = 10; -- Leopardo: Negro M
UPDATE public.variante_producto SET colorid = 2, tallaid = 2, sku = 'POL-11-2-2' WHERE id = 11; -- Estilista: Blanco M
UPDATE public.variante_producto SET colorid = 2, tallaid = 2, sku = 'POL-12-2-2' WHERE id = 12; -- Filipina: Blanco M
UPDATE public.variante_producto SET colorid = 3, tallaid = 2, sku = 'POL-13-3-2' WHERE id = 13; -- Corazon: Negro M
UPDATE public.variante_producto SET colorid = 9, tallaid = 2, sku = 'POL-14-9-2' WHERE id = 18; -- Bicolor: Verde Olivo M
UPDATE public.variante_producto SET colorid = 9, tallaid = 2, sku = 'POL-15-9-2' WHERE id = 19; -- Militar: Verde Olivo M
UPDATE public.variante_producto SET colorid = 3, tallaid = 1, sku = 'POL-16-3-1' WHERE id = 20; -- Crop Top: Negro S
UPDATE public.variante_producto SET colorid = 3, tallaid = 2, sku = 'POL-17-3-2' WHERE id = 21; -- Harley: Negro M
UPDATE public.variante_producto SET colorid = 5, tallaid = 2, sku = 'POL-18-5-2' WHERE id = 22; -- Institucional: Beige M
UPDATE public.variante_producto SET colorid = 5, tallaid = 2, sku = 'POL-19-5-2' WHERE id = 14; -- Rustica: Beige M
UPDATE public.variante_producto SET colorid = 2, tallaid = 2, sku = 'POL-20-2-2' WHERE id = 15; -- Patuju: Blanco M
UPDATE public.variante_producto SET colorid = 2, tallaid = 2, sku = 'POL-21-2-2' WHERE id = 16; -- Angel: Blanco M
UPDATE public.variante_producto SET colorid = 5, tallaid = 2, sku = 'POL-22-5-2' WHERE id = 17; -- Barroco: Beige M
UPDATE public.variante_producto SET colorid = 10, tallaid = 2, sku = 'POL-23-10-2' WHERE id = 23; -- Basica Roja: Rojo Borgoña M

-- 4. Insertar las 2da y 3ra variantes (colores y tallas alternativos)
INSERT INTO public.variante_producto (id, productoid, colorid, tallaid, sku, precioventa, activo) VALUES
  -- Canguro (Prod 1)
  (24, 1, 7, 3, 'POL-1-7-3', 130.00, true),   -- Gris Melange L
  (25, 1, 4, 4, 'POL-1-4-4', 130.00, true),   -- Azul Marino XL
  -- Polera Deportiva (Prod 2)
  (26, 2, 3, 1, 'POL-2-3-1', 100.00, true),   -- Negro S
  (27, 2, 2, 3, 'POL-2-2-3', 100.00, true),   -- Blanco L
  -- Polera Gradientes (Prod 3)
  (28, 3, 6, 3, 'POL-3-6-3', 100.00, true),   -- Terracota L
  (29, 3, 3, 1, 'POL-3-3-1', 100.00, true),   -- Negro S
  -- Polera Gradientes V (Prod 4)
  (30, 4, 3, 3, 'POL-4-3-3', 100.00, true),   -- Negro L
  (31, 4, 2, 1, 'POL-4-2-1', 100.00, true),   -- Blanco S
  -- Dynamic Stroke V-Neck (Prod 5)
  (32, 5, 10, 3, 'POL-5-10-3', 130.00, true), -- Rojo Borgoña L
  (33, 5, 3, 4, 'POL-5-3-4', 130.00, true),   -- Negro XL
  -- Polera Mangas Negras (Prod 6)
  (34, 6, 7, 3, 'POL-6-7-3', 150.00, true),   -- Gris Melange L
  (35, 6, 5, 1, 'POL-6-5-1', 150.00, true),   -- Beige S
  -- Polera Rosa Floral Degradé (Prod 7)
  (36, 7, 5, 2, 'POL-7-5-2', 110.00, true),   -- Beige M
  (37, 7, 3, 2, 'POL-7-3-2', 110.00, true),   -- Negro M
  -- Polera Estampada (Prod 8)
  (38, 8, 3, 3, 'POL-8-3-3', 150.00, true),   -- Negro L
  (39, 8, 10, 1, 'POL-8-10-1', 150.00, true), -- Rojo Borgoña S
  -- Polera con diseño de mano (Prod 9)
  (40, 9, 2, 1, 'POL-9-2-1', 115.00, true),   -- Blanco S
  (41, 9, 6, 3, 'POL-9-6-3', 115.00, true),   -- Terracota L
  -- Polera Negra Leopardo (Prod 10)
  (42, 10, 5, 3, 'POL-10-5-3', 150.00, true), -- Beige L
  (43, 10, 2, 1, 'POL-10-2-1', 150.00, true), -- Blanco S
  -- Polera Estilista (Prod 11)
  (44, 11, 3, 1, 'POL-11-3-1', 90.00, true),  -- Negro S
  (45, 11, 7, 2, 'POL-11-7-2', 90.00, true),  -- Gris Melange M
  -- Filipina Estética Manicura (Prod 12)
  (46, 12, 4, 3, 'POL-12-4-3', 90.00, true),  -- Azul Marino L
  (47, 12, 3, 1, 'POL-12-3-1', 90.00, true),  -- Negro S
  -- Polera Negra Corazón Pincelada (Prod 13)
  (48, 13, 2, 1, 'POL-13-2-1', 170.00, true), -- Blanco S
  (49, 13, 10, 2, 'POL-13-10-2', 170.00, true), -- Rojo Borgoña M
  -- Polera Básica Bicolor Verde Olivo (Prod 14)
  (50, 14, 5, 3, 'POL-14-5-3', 120.00, true), -- Beige L
  (51, 14, 2, 1, 'POL-14-2-1', 120.00, true), -- Blanco S
  -- Polera Básica Verde Militar (Prod 15)
  (52, 15, 3, 3, 'POL-15-3-3', 115.00, true), -- Negro L
  (53, 15, 7, 1, 'POL-15-7-1', 115.00, true), -- Gris Melange S
  -- Crop Top Negro (Prod 16)
  (54, 16, 2, 2, 'POL-16-2-2', 80.00, true),  -- Blanco M
  (55, 16, 10, 1, 'POL-16-10-1', 80.00, true),-- Rojo Borgoña S
  -- Polera Negra Harley Quinn (Prod 17)
  (56, 17, 2, 1, 'POL-17-2-1', 150.00, true), -- Blanco S
  (57, 17, 10, 3, 'POL-17-10-3', 150.00, true),-- Rojo Borgoña L
  -- Institucional Artesanal (Prod 18)
  (58, 18, 2, 3, 'POL-18-2-3', 150.00, true), -- Blanco L
  (59, 18, 1, 1, 'POL-18-1-1', 150.00, true), -- Verde Oriente S
  -- Polera Rústica con Bordado Tradicional (Prod 19)
  (60, 19, 1, 1, 'POL-19-1-1', 140.00, true), -- Verde Oriente S
  (61, 19, 2, 3, 'POL-19-2-3', 140.00, true), -- Blanco L
  -- Camisa Patujú Santa Cruz (Prod 20)
  (62, 20, 1, 3, 'POL-20-1-3', 180.00, true), -- Verde Oriente L
  (63, 20, 5, 4, 'POL-20-5-4', 180.00, true), -- Beige XL
  -- Camisa Típica Blanca Ángel Chiquitano (Prod 21)
  (64, 21, 5, 3, 'POL-21-5-3', 180.00, true), -- Beige L
  (65, 21, 2, 1, 'POL-21-2-1', 180.00, true), -- Blanco S
  -- Polera Típica Beige Cordón Barroco (Prod 22)
  (66, 22, 2, 3, 'POL-22-2-3', 199.50, true), -- Blanco L
  (67, 22, 6, 1, 'POL-22-6-1', 199.50, true), -- Terracota S
  -- Polera Básica Roja Cuello Redondo (Prod 23)
  (68, 23, 3, 3, 'POL-23-3-3', 120.00, true), -- Negro L
  (69, 23, 2, 1, 'POL-23-2-1', 120.00, true)  -- Blanco S
ON CONFLICT (id) DO UPDATE SET
  colorid = EXCLUDED.colorid,
  tallaid = EXCLUDED.tallaid,
  sku = EXCLUDED.sku,
  precioventa = EXCLUDED.precioventa,
  activo = true;

-- 5. Resincronizar secuencia de variantes
SELECT setval('variante_producto_id_seq', (SELECT MAX(id) FROM public.variante_producto), true);

-- 6. Actualizar inventario con stock variado y realista para las 3 sucursales
-- Sucursal 1: Boutique Central Equipetrol (Alto)
-- Sucursal 2: Boutique Mall Ventura (Medio)
-- Sucursal 3: Boutique Las Brisas (Boutique / Exclusivo)

-- Limpiar o actualizar stocks
INSERT INTO public.inventario (sucursalid, varianteid, stockfisico, stockreservado, stockminimo) VALUES
  -- Prod 1: Canguro
  (1, 1, 8, 0, 3), (2, 1, 4, 0, 2), (3, 1, 2, 0, 1),
  (1, 24, 6, 0, 3), (2, 24, 3, 0, 2), (3, 24, 1, 0, 1),
  (1, 25, 4, 0, 2), (2, 25, 2, 0, 1), (3, 25, 0, 0, 1),

  -- Prod 2: Deportiva
  (1, 2, 10, 0, 4), (2, 2, 5, 0, 2), (3, 2, 3, 0, 1),
  (1, 26, 7, 0, 3), (2, 26, 4, 0, 2), (3, 26, 2, 0, 1),
  (1, 27, 5, 0, 2), (2, 27, 2, 0, 1), (3, 27, 0, 0, 1),

  -- Prod 3: Gradientes
  (1, 3, 6, 0, 3), (2, 3, 3, 0, 2), (3, 3, 1, 0, 1),
  (1, 28, 5, 0, 2), (2, 28, 2, 0, 1), (3, 28, 1, 0, 1),
  (1, 29, 4, 0, 2), (2, 29, 2, 0, 1), (3, 29, 0, 0, 1),

  -- Prod 4: Gradientes V
  (1, 4, 7, 0, 3), (2, 4, 4, 0, 2), (3, 4, 2, 0, 1),
  (1, 30, 5, 0, 2), (2, 30, 3, 0, 2), (3, 30, 1, 0, 1),
  (1, 31, 4, 0, 2), (2, 31, 1, 0, 1), (3, 31, 0, 0, 1),

  -- Prod 5: Dynamic
  (1, 5, 9, 0, 3), (2, 5, 4, 0, 2), (3, 5, 2, 0, 1),
  (1, 32, 6, 0, 2), (2, 32, 3, 0, 2), (3, 32, 1, 0, 1),
  (1, 33, 4, 0, 2), (2, 33, 2, 0, 1), (3, 33, 0, 0, 1),

  -- Prod 6: Mangas Negras
  (1, 6, 12, 0, 4), (2, 6, 6, 0, 2), (3, 6, 3, 0, 1),
  (1, 34, 8, 0, 3), (2, 34, 4, 0, 2), (3, 34, 2, 0, 1),
  (1, 35, 5, 0, 2), (2, 35, 2, 0, 1), (3, 35, 1, 0, 1),

  -- Prod 7: Rosa Floral
  (1, 7, 7, 0, 3), (2, 7, 3, 0, 2), (3, 7, 1, 0, 1),
  (1, 36, 9, 0, 3), (2, 36, 4, 0, 2), (3, 36, 2, 0, 1),
  (1, 37, 4, 0, 2), (2, 37, 2, 0, 1), (3, 37, 0, 0, 1),

  -- Prod 8: Estampada
  (1, 8, 8, 0, 3), (2, 8, 5, 0, 2), (3, 8, 2, 0, 1),
  (1, 38, 6, 0, 2), (2, 38, 3, 0, 2), (3, 38, 1, 0, 1),
  (1, 39, 4, 0, 2), (2, 39, 2, 0, 1), (3, 39, 0, 0, 1),

  -- Prod 9: Mano
  (1, 9, 7, 0, 3), (2, 9, 4, 0, 2), (3, 9, 2, 0, 1),
  (1, 40, 5, 0, 2), (2, 40, 2, 0, 1), (3, 40, 1, 0, 1),
  (1, 41, 4, 0, 2), (2, 41, 1, 0, 1), (3, 41, 0, 0, 1),

  -- Prod 10: Leopardo
  (1, 10, 10, 0, 4), (2, 10, 5, 0, 2), (3, 10, 3, 0, 1),
  (1, 42, 6, 0, 2), (2, 42, 3, 0, 2), (3, 42, 1, 0, 1),
  (1, 43, 4, 0, 2), (2, 43, 1, 0, 1), (3, 43, 0, 0, 1),

  -- Prod 11: Estilista
  (1, 11, 8, 0, 3), (2, 11, 4, 0, 2), (3, 11, 2, 0, 1),
  (1, 44, 6, 0, 2), (2, 44, 3, 0, 2), (3, 44, 1, 0, 1),
  (1, 45, 4, 0, 2), (2, 45, 2, 0, 1), (3, 45, 0, 0, 1),

  -- Prod 12: Filipina
  (1, 12, 9, 0, 3), (2, 12, 5, 0, 2), (3, 12, 2, 0, 1),
  (1, 46, 6, 0, 2), (2, 46, 3, 0, 2), (3, 46, 1, 0, 1),
  (1, 47, 5, 0, 2), (2, 47, 2, 0, 1), (3, 47, 0, 0, 1),

  -- Prod 13: Corazón
  (1, 13, 8, 0, 3), (2, 13, 4, 0, 2), (3, 13, 2, 0, 1),
  (1, 48, 6, 0, 2), (2, 48, 3, 0, 1), (3, 48, 1, 0, 1),
  (1, 49, 4, 0, 2), (2, 49, 1, 0, 1), (3, 49, 0, 0, 1),

  -- Prod 14: Bicolor Verde Olivo (id var 18)
  (1, 18, 11, 0, 4), (2, 18, 6, 0, 2), (3, 18, 3, 0, 1),
  (1, 50, 7, 0, 3), (2, 50, 4, 0, 2), (3, 50, 2, 0, 1),
  (1, 51, 5, 0, 2), (2, 51, 2, 0, 1), (3, 51, 1, 0, 1),

  -- Prod 15: Militar (id var 19)
  (1, 19, 10, 0, 3), (2, 19, 5, 0, 2), (3, 19, 2, 0, 1),
  (1, 52, 7, 0, 2), (2, 52, 3, 0, 1), (3, 52, 1, 0, 1),
  (1, 53, 4, 0, 2), (2, 53, 2, 0, 1), (3, 53, 0, 0, 1),

  -- Prod 16: Crop Top (id var 20)
  (1, 20, 5, 0, 2), (2, 20, 3, 0, 1), (3, 20, 1, 0, 1),
  (1, 54, 4, 0, 2), (2, 54, 2, 0, 1), (3, 54, 0, 0, 1),
  (1, 55, 3, 0, 1), (2, 55, 1, 0, 1), (3, 55, 0, 0, 1),

  -- Prod 17: Harley (id var 21)
  (1, 21, 8, 0, 3), (2, 21, 4, 0, 2), (3, 21, 2, 0, 1),
  (1, 56, 5, 0, 2), (2, 56, 2, 0, 1), (3, 56, 1, 0, 1),
  (1, 57, 4, 0, 2), (2, 57, 1, 0, 1), (3, 57, 0, 0, 1),

  -- Prod 18: Artesanal (id var 22)
  (1, 22, 9, 0, 3), (2, 22, 5, 0, 2), (3, 22, 2, 0, 1),
  (1, 58, 7, 0, 2), (2, 58, 3, 0, 2), (3, 58, 1, 0, 1),
  (1, 59, 5, 0, 2), (2, 59, 2, 0, 1), (3, 59, 0, 0, 1),

  -- Prod 19: Rústica (id var 14)
  (1, 14, 12, 0, 4), (2, 14, 6, 0, 2), (3, 14, 3, 0, 1),
  (1, 60, 8, 0, 3), (2, 60, 4, 0, 2), (3, 60, 1, 0, 1),
  (1, 61, 6, 0, 2), (2, 61, 2, 0, 1), (3, 61, 0, 0, 1),

  -- Prod 20: Patujú (id var 15)
  (1, 15, 14, 0, 4), (2, 15, 7, 0, 2), (3, 15, 3, 0, 1),
  (1, 62, 9, 0, 3), (2, 62, 5, 0, 2), (3, 62, 2, 0, 1),
  (1, 63, 6, 0, 2), (2, 63, 2, 0, 1), (3, 63, 1, 0, 1),

  -- Prod 21: Ángel Chiquitano (id var 16)
  (1, 16, 15, 0, 5), (2, 16, 8, 0, 3), (3, 16, 4, 0, 1),
  (1, 64, 8, 0, 3), (2, 64, 4, 0, 2), (3, 64, 2, 0, 1),
  (1, 65, 6, 0, 2), (2, 65, 3, 0, 1), (3, 65, 1, 0, 1),

  -- Prod 22: Barroco (id var 17)
  (1, 17, 11, 0, 4), (2, 17, 5, 0, 2), (3, 17, 2, 0, 1),
  (1, 66, 7, 0, 2), (2, 66, 3, 0, 2), (3, 66, 1, 0, 1),
  (1, 67, 4, 0, 2), (2, 67, 2, 0, 1), (3, 67, 0, 0, 1),

  -- Prod 23: Básica Roja (id var 23)
  (1, 23, 13, 0, 4), (2, 23, 7, 0, 2), (3, 23, 3, 0, 1),
  (1, 68, 8, 0, 3), (2, 68, 4, 0, 2), (3, 68, 2, 0, 1),
  (1, 69, 6, 0, 2), (2, 69, 3, 0, 1), (3, 69, 1, 0, 1)

ON CONFLICT (id) DO UPDATE SET
  stockfisico = EXCLUDED.stockfisico,
  stockreservado = EXCLUDED.stockreservado,
  stockminimo = EXCLUDED.stockminimo;

-- 7. Resincronizar secuencia de inventario
SELECT setval('inventario_id_seq', (SELECT MAX(id) FROM public.inventario), true);

COMMIT;
