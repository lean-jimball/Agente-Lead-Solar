# src/domain/lead.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re
import unicodedata

class LeadStatus(Enum):
    NUEVO = "Nuevo"
    SIN_TELEFONO = "Sin teléfono"
    NO_WHATSAPP = "No WhatsApp"
    CONTACTADO = "Contactado"
    CALIFICADO = "Calificado"
    CERRADO_GANADO = "Cerrado ganado"
    CERRADO_PERDIDO = "Cerrado perdido"

@dataclass
class Lead:
    id: Optional[int] = None
    nombre: str = ""
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    poblacion: Optional[str] = None
    estado: Optional[str] = None
    score_ia: int = 0
    ahorro_mensual: int = 0
    sistema_recomendado: float = 0.0
    estado_pipeline: str = LeadStatus.NUEVO.value
    tipo_negocio: Optional[str] = None
    website: Optional[str] = None
    calificacion: float = 0.0
    razon_score: Optional[str] = None
    consumo_estimado: int = 0
    mensaje_generado: Optional[str] = None
    enviado: int = 0
    fecha_creacion: Optional[str] = None
    fecha_ultimo_contacto: Optional[str] = None
    fecha_contacto: Optional[str] = None

    @staticmethod
    def normalizar_nombre(nombre: str) -> str:
        if not nombre:
            return ""
        s = unicodedata.normalize('NFKD', str(nombre).lower().strip())
        s = re.sub(r'["\']', '', s)
        return ''.join([c for c in s if not unicodedata.combining(c)])

    @staticmethod
    def es_numero_whatsapp(telefono: str) -> bool:
        if not telefono:
            return False
        num = re.sub(r'\D', '', str(telefono))
        return len(num) == 10 or (len(num) == 12 and num.startswith('52'))

    def determinar_estado_inicial(self) -> str:
        if not self.telefono or str(self.telefono).strip() == '':
            return LeadStatus.SIN_TELEFONO.value
        if not Lead.es_numero_whatsapp(self.telefono):
            return LeadStatus.NO_WHATSAPP.value
        return LeadStatus.NUEVO.value