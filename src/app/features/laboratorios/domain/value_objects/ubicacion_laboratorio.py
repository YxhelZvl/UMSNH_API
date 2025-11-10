# src/app/features/laboratorios/domain/value_objects/ubicacion_laboratorio.py
from pydantic import BaseModel, Field, field_validator, model_serializer

class UbicacionLaboratorio(BaseModel):
    valor: str = Field(..., description="Ubicación del Laboratorio")
    
    @field_validator("valor")
    def validar_ubicacion(cls, v):
        if not v.strip():
            raise ValueError("La ubicación del laboratorio no puede estar vacía")
        
        if len(v) < 5:
            raise ValueError("La ubicación debe ser más específica (mínimo 5 caracteres)")
        
        if len(v) > 250:  # Para coincidir con tu BD
            raise ValueError("La ubicación no puede exceder 250 caracteres")
            
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_ubicacion(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, UbicacionLaboratorio) and self.valor == other.valor
    
    def __str__(self):
        return self.valor