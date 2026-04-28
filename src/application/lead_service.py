# src/application/lead_service.py
from typing import Optional, List
from src.domain.lead import Lead
from src.infrastructure.database.repository import LeadRepository

class LeadService:
    """Orquesta la lógica de negocio: validaciones, deduplicación y persistencia."""
    
    def __init__(self):
        self.repo = LeadRepository()

    def create_lead(self, lead_data: dict) -> Optional[int]:
        """Crea un lead validando duplicados y reglas de negocio."""
        if lead_data.get('score_ia', 0) == 0:
            return None

        nombre_norm = Lead.normalizar_nombre(lead_data.get('nombre', ''))
        
        lead = Lead(
            nombre=lead_data.get('nombre', ''),
            telefono=lead_data.get('telefono', '').strip(),
            tipo_negocio=lead_data.get('tipo_negocio'),
            direccion=lead_data.get('direccion'),
            poblacion=lead_data.get('poblacion'),
            estado=lead_data.get('estado'),
            website=lead_data.get('website'),
            calificacion=lead_data.get('calificacion', 0),
            score_ia=lead_data.get('score_ia', 0),
            razon_score=lead_data.get('razon_score'),
            consumo_estimado=lead_data.get('consumo_estimado', 0),
            sistema_recomendado=lead_data.get('sistema_recomendado', 0.0),
            ahorro_mensual=lead_data.get('ahorro_mensual', 0),
            mensaje_generado=lead_data.get('mensaje_generado'),
            enviado=lead_data.get('enviado', 0)
        )

        # Derivar población si falta
        if not lead.poblacion and lead.direccion:
            partes = lead.direccion.split(',')
            lead.poblacion = partes[-2].strip() if len(partes) >= 2 else ''

        # Determinar estado inicial
        lead.estado_pipeline = lead.determinar_estado_inicial()

        # Verificar duplicados
        if self.repo.existe_duplicado(lead.telefono, nombre_norm):
            return None

        return self.repo.save(lead)

    def get_all_leads(self, limit: int = 2000) -> List[dict]:
        """✅ MÉTODO NUEVO: Obtiene todos los leads (con límite) para la UI."""
        return self.repo.get_all(limit=limit)

    def get_dashboard_stats(self) -> dict:
        """Obtiene estadísticas para el Dashboard."""
        return self.repo.get_stats()

    def update_lead_status(self, lead_id: int, new_status: str) -> bool:
        """Actualiza el estado de un lead (para el editor del Pipeline)."""
        return self.repo.update_status(lead_id, new_status)