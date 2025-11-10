# src/app/features/laboratorios/domain/value_objects/nombre_laboratorio.py
from pydantic import BaseModel, Field, field_validator, model_serializer

class NombreLaboratorio(BaseModel):
    valor: str = Field(..., description="Nombre del Laboratorio")
    
    @field_validator("valor")
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre del laboratorio no puede estar vacío")
        
        if len(v) < 3:
            raise ValueError("El nombre del laboratorio debe tener al menos 3 caracteres")
        
        if len(v) > 150:  # Para coincidir con tu BD
            raise ValueError("El nombre del laboratorio no puede exceder 150 caracteres")
            
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_nombre(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, NombreLaboratorio) and self.valor == other.valor
    
    def __str__(self):
        return self.valor