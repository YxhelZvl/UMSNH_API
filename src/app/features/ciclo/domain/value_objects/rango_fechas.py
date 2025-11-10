# src/app/features/ciclo/domain/value_objects/rango_fechas.py
from pydantic import BaseModel, field_validator, model_serializer
from datetime import date
from typing import Tuple

class RangoFechasValueObject(BaseModel):
    fecha_inicio: date
    fecha_final: date
    
    @field_validator("fecha_final")
    def validar_rango_fechas(cls, v, info):
        if 'fecha_inicio' in info.data and v <= info.data['fecha_inicio']:
            raise ValueError("La fecha final debe ser posterior a la fecha de inicio")
        return v
    
    def obtener_duracion_dias(self) -> int:
        return (self.fecha_final - self.fecha_inicio).days
    
    
    
    
    class Config:
        arbitrary_types_allowed = True