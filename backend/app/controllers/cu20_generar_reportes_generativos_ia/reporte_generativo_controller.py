# ==============================================================================
# CU20 - GENERAR REPORTES GENERATIVOS CON IA -> CONTROLADOR (MVC - CONTROLLER)
# Ubicación: backend/app/controllers/cu20_generar_reportes_generativos_ia/reporte_generativo_controller.py
# ==============================================================================

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.services.cu20_generar_reportes_generativos_ia.reporte_generativo_service import ReporteGenerativoService


class ReporteGenerativoController:
    """
    Controlador para coordinar la generación, consulta, alternancia de favoritos
    y exportación de reportes analíticos generativos asistidos por IA.
    """

    @staticmethod
    def generar_reporte(
        db: Session,
        tenant_id: int,
        usuario_id: Optional[int],
        prompt: str,
        filtros: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ejecuta la síntesis de datos en lenguaje natural y persiste el reporte."""
        if not prompt or len(prompt.strip()) < 3:
            raise ValueError("La consulta en lenguaje natural debe tener al menos 3 caracteres.")
        return ReporteGenerativoService.generar_reporte_ia(
            db=db,
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            prompt=prompt.strip(),
            filtros=filtros
        )

    @staticmethod
    def listar_historial(db: Session, tenant_id: int, limite: int = 20) -> List[Dict[str, Any]]:
        """Devuelve el registro histórico de consultas y reportes generados."""
        return ReporteGenerativoService.listar_historial(db=db, tenant_id=tenant_id, limite=limite)

    @staticmethod
    def obtener_reporte(db: Session, reporte_id: int, tenant_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un reporte específico con su estructura completa."""
        return ReporteGenerativoService.obtener_detalle(db=db, reporte_id=reporte_id, tenant_id=tenant_id)

    @staticmethod
    def alternar_favorito(db: Session, reporte_id: int, tenant_id: int) -> Dict[str, Any]:
        """Marca o desmarca el reporte como favorito."""
        nuevo_estado = ReporteGenerativoService.alternar_favorito(db=db, reporte_id=reporte_id, tenant_id=tenant_id)
        return {"reporte_id": reporte_id, "es_favorito": nuevo_estado}

    @staticmethod
    def obtener_consultas_sugeridas() -> List[Dict[str, str]]:
        """Retorna las plantillas y prompts sugeridos."""
        return ReporteGenerativoService.consultas_sugeridas()
