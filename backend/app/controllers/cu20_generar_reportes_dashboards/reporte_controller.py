# ==============================================================================
# CU20 - GENERAR REPORTES Y DASHBOARDS -> CAPA CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu20_generar_reportes_dashboards/reporte_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import io
import csv

from app.models.cu14_registrar_ventas_presenciales.venta_presencial_model import (
    VentaModel, DetalleVentaModel, PagoModel, MetodoPagoModel
)
from app.models.cu10_gestionar_reservas_prendas.reserva_model import ReservaModel
from app.models.cu13_gestionar_inventario_movimientos.inventario_model import InventarioModel
from app.models.cu5_gestionar_productos.producto_model import ProductoModel, VarianteProductoModel
from app.models.cu4_gestionar_sucursales.sucursal_model import SucursalModel


class ReporteController:

    @staticmethod
    def obtener_kpis(db: Session, dias: Optional[int] = None) -> Dict[str, Any]:
        """CU20: Retorna los KPIs ejecutivos calculados directamente de las tablas de PostgreSQL"""
        query_ventas = db.query(VentaModel).filter(VentaModel.estado.ilike("%Completada%"))

        if dias:
            fecha_limite = datetime.utcnow() - timedelta(days=dias)
            query_ventas = query_ventas.filter(VentaModel.fecha >= fecha_limite)

        ventas = query_ventas.all()
        total_ingresos = sum([float(v.total or 0) for v in ventas])
        total_transacciones = len(ventas)
        ticket_promedio = (total_ingresos / total_transacciones) if total_transacciones > 0 else 0.0

        # Prendas vendidas
        venta_ids = [v.id for v in ventas]
        prendas_vendidas = 0
        if venta_ids:
            res_cant = db.query(func.sum(DetalleVentaModel.cantidad)).filter(
                DetalleVentaModel.ventaid.in_(venta_ids)
            ).scalar()
            prendas_vendidas = int(res_cant or 0)

        # Reservas activas
        reservas_activas = db.query(ReservaModel).filter(ReservaModel.estado == "PENDIENTE").count()

        # Stock físico total en bodegas y sucursales
        stock_total = db.query(func.sum(InventarioModel.stockfisico)).scalar() or 0

        # Stock crítico (artículos con stock <= stockminimo)
        stock_critico = db.query(InventarioModel).filter(
            InventarioModel.stockfisico <= InventarioModel.stockminimo
        ).count()

        return {
            "total_ingresos_bs": round(total_ingresos, 2),
            "total_transacciones": total_transacciones,
            "ticket_promedio_bs": round(ticket_promedio, 2),
            "prendas_vendidas": prendas_vendidas,
            "reservas_activas": reservas_activas,
            "stock_total_fisico": int(stock_total),
            "articulos_stock_critico": stock_critico,
            "fecha_calculo": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

    @staticmethod
    def obtener_ventas_por_sucursal(db: Session) -> List[Dict[str, Any]]:
        """CU20: Retorna distribución de ingresos y transacciones por sucursal física"""
        sucursales = db.query(SucursalModel).filter(SucursalModel.activo == True).all()
        resultado = []

        for suc in sucursales:
            ventas_suc = db.query(VentaModel).filter(
                VentaModel.sucursalid == suc.id,
                VentaModel.estado.ilike("%Completada%")
            ).all()

            total_monto = sum([float(v.total or 0) for v in ventas_suc])
            resultado.append({
                "sucursal_id": suc.id,
                "sucursal_nombre": suc.nombre,
                "ciudad": suc.ciudad or "Santa Cruz",
                "total_bs": round(total_monto, 2),
                "transacciones": len(ventas_suc)
            })

        return sorted(resultado, key=lambda x: x["total_bs"], reverse=True)

    @staticmethod
    def obtener_ventas_por_canal(db: Session) -> List[Dict[str, Any]]:
        """CU20: Retorna proporción entre ventas Digitales (App/Web) vs Presenciales (Caja/POS)"""
        canales = ["Digital", "Presencial"]
        resultado = []

        for canal in canales:
            ventas_canal = db.query(VentaModel).filter(
                VentaModel.tipoventa.ilike(f"%{canal}%"),
                VentaModel.estado.ilike("%Completada%")
            ).all()

            total_monto = sum([float(v.total or 0) for v in ventas_canal])
            resultado.append({
                "canal": canal,
                "total_bs": round(total_monto, 2),
                "transacciones": len(ventas_canal)
            })

        return resultado

    @staticmethod
    def obtener_ventas_por_metodo_pago(db: Session) -> List[Dict[str, Any]]:
        """CU20: Desglose de ingresos por método de pago (PayPal, QR, Efectivo, Tarjeta)"""
        metodos = db.query(MetodoPagoModel).all()
        resultado = []

        for m in metodos:
            pagos = db.query(PagoModel).filter(
                PagoModel.metodoid == m.id,
                PagoModel.estado.ilike("%Aprobado%")
            ).all()

            total_monto = sum([float(p.monto or 0) for p in pagos])
            resultado.append({
                "metodo_id": m.id,
                "metodo_nombre": m.nombre,
                "total_bs": round(total_monto, 2),
                "cantidad_pagos": len(pagos)
            })

        return sorted(resultado, key=lambda x: x["total_bs"], reverse=True)

    @staticmethod
    def obtener_top_prendas(db: Session, limite: int = 5) -> List[Dict[str, Any]]:
        """CU20: Top 5 de poleras más vendidas con ingresos generados"""
        top_items = db.query(
            DetalleVentaModel.varianteid,
            func.sum(DetalleVentaModel.cantidad).label("unidades_vendidas"),
            func.sum(DetalleVentaModel.subtotal).label("recaudacion_total")
        ).group_by(DetalleVentaModel.varianteid).order_by(
            func.sum(DetalleVentaModel.cantidad).desc()
        ).limit(limite).all()

        resultado = []
        for item in top_items:
            variante = db.query(VarianteProductoModel).filter(VarianteProductoModel.id == item.varianteid).first()
            nombre = "Polera Boutique"
            sku = "TEE-BASE"
            precio = 100.0
            if variante:
                sku = variante.sku or sku
                prod = db.query(ProductoModel).filter(ProductoModel.id == variante.productoid).first()
                if prod:
                    nombre = prod.nombre
                    precio = float(prod.preciobase or 100.0)

            resultado.append({
                "variante_id": item.varianteid,
                "sku": sku,
                "nombre_producto": nombre,
                "precio_unitario": precio,
                "unidades_vendidas": int(item.unidades_vendidas or 0),
                "recaudacion_bs": round(float(item.recaudacion_total or 0), 2)
            })

        return resultado

    @staticmethod
    def exportar_ventas_csv(db: Session) -> str:
        """CU20: Genera archivo CSV descargable con todas las transacciones del sistema"""
        ventas = db.query(VentaModel).order_by(VentaModel.id.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")

        writer.writerow([
            "ID VENTA",
            "CODIGO VENTA",
            "TIPO VENTA",
            "ESTADO",
            "SUCURSAL",
            "SUBTOTAL BS",
            "DESCUENTO BS",
            "TOTAL BS",
            "FECHA REGISTRO"
        ])

        for v in ventas:
            suc = db.query(SucursalModel).filter(SucursalModel.id == v.sucursalid).first()
            suc_nombre = suc.nombre if suc else "Sucursal Central"
            fecha_str = v.fecha.strftime("%d/%m/%Y %H:%M") if v.fecha else ""

            writer.writerow([
                v.id,
                v.codigoventa,
                v.tipoventa,
                v.estado,
                suc_nombre,
                f"{float(v.subtotal or 0):.2f}",
                f"{float(v.descuento or 0):.2f}",
                f"{float(v.total or 0):.2f}",
                fecha_str
            ])

        return output.getvalue()
