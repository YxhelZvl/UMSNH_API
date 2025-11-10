# src/app/features/carrera/domain/value_objects/facultad.py
from pydantic import BaseModel, field_validator, model_serializer

class FacultadValueObject(BaseModel):
    valor: str
    
    @field_validator("valor")
    def validar_facultad(cls, v):
        if not v or not v.strip():
            raise ValueError("La facultad no puede estar vacía")
        if len(v) < 3:
            raise ValueError("La facultad debe tener al menos 3 caracteres")
        if len(v) > 250:
            raise ValueError("La facultad no puede exceder 250 caracteres")
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_facultad(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, FacultadValueObject) and self.valor == other.valor
    
    def __str__(self):
        return self.valor