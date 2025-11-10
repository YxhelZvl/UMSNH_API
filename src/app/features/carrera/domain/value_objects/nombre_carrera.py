# src/app/features/carrera/domain/value_objects/nombre_carrera.py
from pydantic import BaseModel, field_validator, model_serializer

class NombreCarreraValueObject(BaseModel):
    valor: str
    
    @field_validator("valor")
    def validar_nombre_carrera(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre de la carrera no puede estar vacío")
        if len(v) < 5:
            raise ValueError("El nombre de la carrera debe tener al menos 5 caracteres")
        if len(v) > 120:
            raise ValueError("El nombre de la carrera no puede exceder 120 caracteres")
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_nombre_carrera(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, NombreCarreraValueObject) and self.valor == other.valor
    
    def __str__(self):
        return self.valor