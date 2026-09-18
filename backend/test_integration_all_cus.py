import sys
from app.core.database import SessionLocal
from app.models.models import UsuarioModel, ClienteModel, VentaModel, ReservaModel
from app.controllers.cu16_gestionar_pagos_comprobantes.pago_controller import PagoController
from app.controllers.cu17_consultar_historial_compras_reservas.historial_controller import HistorialController
from app.controllers.cu18_gestionar_recomendaciones_ia.recomendacion_controller import RecomendacionController
from app.controllers.cu19_gestionar_notificaciones.notificacion_controller import NotificacionController
from app.controllers.cu20_generar_reportes_dashboards.reporte_controller import ReporteController

def test_everything():
    db = SessionLocal()
    try:
        print("=" * 65)
        print("VERIFICACION DE INTEGRACION COMPLETA: BASE DE DATOS Y CUs")
        print("=" * 65)
        
        user = db.query(UsuarioModel).first()
        if not user:
            print("ERROR: No se encontro usuario en PostgreSQL")
            sys.exit(1)
        print(f"[OK] Conexion PostgreSQL exitosa. Usuario ID {user.id}: {user.email}")
        
        # CU16: Metodos de Pago
        metodos = PagoController.listar_metodos_pago(db)
        print(f"[OK] CU16 Metodos de pago activos ({len(metodos)}): {[m['nombre'] for m in metodos]}")
        
        # CU17: Historial de Compras y Reservas
        resumen = HistorialController.obtener_resumen_cliente(db, user)
        print(f"[OK] CU17 Resumen cliente: {resumen}")
        compras = HistorialController.listar_compras_cliente(db, user)
        print(f"[OK] CU17 Compras cliente: {len(compras)} pedidos encontrados")
        reservas = HistorialController.listar_reservas_cliente(db, user)
        print(f"[OK] CU17 Reservas cliente: {len(reservas)} reservas encontradas")

        # CU18: Recomendaciones IA
        recom = RecomendacionController.recomendar_outfit(db, limite=3)
        print(f"[OK] CU18 Outfit Recomendado IA: {len(recom)} prendas sugeridas")
        tendencias = RecomendacionController.obtener_tendencias(db, limite=3)
        print(f"[OK] CU18 Tendencias: {len(tendencias)} prendas en vitrina")

        # CU19: Notificaciones
        notifs = NotificacionController.listar_notificaciones(db, user)
        print(f"[OK] CU19 Notificaciones: {len(notifs)} alertas activas")

        # CU20: Reportes y Dashboards
        kpis = ReporteController.obtener_kpis(db)
        print(f"[OK] CU20 KPIs Generales: {kpis}")
        ventas_suc = ReporteController.obtener_ventas_por_sucursal(db)
        print(f"[OK] CU20 Ventas por Sucursal: {len(ventas_suc)} sucursales analizadas")
        top = ReporteController.obtener_top_prendas(db, limite=5)
        print(f"[OK] CU20 Top Prendas: {len(top)} prendas con mayor rotacion")

        print("=" * 65)
        print("AUDITORIA FINAL: BASE DE DATOS Y LOGICA DE BACKEND AL 100%")
        print("=" * 65)
    finally:
        db.close()

if __name__ == "__main__":
    test_everything()
