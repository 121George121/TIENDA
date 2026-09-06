-- ==============================================================================
-- Resincroniza las secuencias SERIAL de todas las tablas con el MAX(id) real.
-- Necesario cuando se insertan filas con id explicito (seeds, migraciones
-- manuales) sin actualizar la secuencia: el proximo INSERT sin id explicito
-- choca con una llave primaria ya existente (fue el caso real de rol,
-- categoria y producto en esta base de datos). Seguro de re-ejecutar.
-- ==============================================================================

SELECT setval('public.sucursal_id_seq', COALESCE((SELECT MAX(id) FROM sucursal), 1), true);
SELECT setval('public.rol_id_seq', COALESCE((SELECT MAX(id) FROM rol), 1), true);
SELECT setval('public.cliente_id_seq', COALESCE((SELECT MAX(id) FROM cliente), 1), true);
SELECT setval('public.usuario_id_seq', COALESCE((SELECT MAX(id) FROM usuario), 1), true);
SELECT setval('public.direccioncliente_id_seq', COALESCE((SELECT MAX(id) FROM direccioncliente), 1), true);
SELECT setval('public.carrito_id_seq', COALESCE((SELECT MAX(id) FROM carrito), 1), true);
SELECT setval('public.temporada_id_seq', COALESCE((SELECT MAX(id) FROM temporada), 1), true);
SELECT setval('public.coleccion_id_seq', COALESCE((SELECT MAX(id) FROM coleccion), 1), true);
SELECT setval('public.categoria_id_seq', COALESCE((SELECT MAX(id) FROM categoria), 1), true);
SELECT setval('public.producto_id_seq', COALESCE((SELECT MAX(id) FROM producto), 1), true);
SELECT setval('public.proveedor_id_seq', COALESCE((SELECT MAX(id) FROM proveedor), 1), true);
SELECT setval('public.variante_producto_id_seq', COALESCE((SELECT MAX(id) FROM variante_producto), 1), true);
SELECT setval('public.color_id_seq', COALESCE((SELECT MAX(id) FROM color), 1), true);
SELECT setval('public.talla_id_seq', COALESCE((SELECT MAX(id) FROM talla), 1), true);
SELECT setval('public.inventario_id_seq', COALESCE((SELECT MAX(id) FROM inventario), 1), true);
SELECT setval('public.reserva_id_seq', COALESCE((SELECT MAX(id) FROM reserva), 1), true);
SELECT setval('public.movimiento_inventario_id_seq', COALESCE((SELECT MAX(id) FROM movimiento_inventario), 1), true);
SELECT setval('public.venta_id_seq', COALESCE((SELECT MAX(id) FROM venta), 1), true);
SELECT setval('public.pago_id_seq', COALESCE((SELECT MAX(id) FROM pago), 1), true);
SELECT setval('public.recibo_id_seq', COALESCE((SELECT MAX(id) FROM recibo), 1), true);
SELECT setval('public.metodo_pago_id_seq', COALESCE((SELECT MAX(id) FROM metodo_pago), 1), true);
SELECT setval('public.prueba_virtual_id_seq', COALESCE((SELECT MAX(id) FROM prueba_virtual), 1), true);
SELECT setval('public.evento_cliente_id_seq', COALESCE((SELECT MAX(id) FROM evento_cliente), 1), true);
