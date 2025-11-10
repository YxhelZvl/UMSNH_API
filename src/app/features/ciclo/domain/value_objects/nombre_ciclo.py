# src/app/features/ciclo/domain/value_objects/nombre_ciclo.py
from pydantic import BaseModel, field_validator, model_serializer
import re

class NombreCicloValueObject(BaseModel):
    valor: str
    
    @field_validator("valor")
    def validar_nombre_ciclo(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre del ciclo no puede estar vacío")
        
        # Validar formato: por ejemplo "2024-2025"
        if not re.match(r'^\d{4}-\d{4}$', v.strip()):
            raise ValueError("El formato del ciclo debe ser 'YYYY-YYYY'")
        
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_nombre_ciclo(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, NombreCicloValueObject) and self.valor == other.valor
    
    def __str__(self):
        return self.valor