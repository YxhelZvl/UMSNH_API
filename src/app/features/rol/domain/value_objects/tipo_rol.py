# src/app/features/rol/domain/value_objects/tipo_rol.py
from pydantic import BaseModel, field_validator, model_serializer

class TipoRolValueObject(BaseModel):
    valor: str
    
    @field_validator("valor")
    def validar_tipo_rol(cls, v):
        if not v or not v.strip():
            raise ValueError("El tipo de rol no puede estar vacío")
        if len(v) < 3:
            raise ValueError("El tipo de rol debe tener al menos 3 caracteres")
        if len(v) > 30:
            raise ValueError("El tipo de rol no puede exceder 30 caracteres")
        return v.strip().title()  # Normaliza el formato
    
    @model_serializer(when_used='json')
    def serialize_tipo_rol(self) -> str:
        # Para serialización JSON en FastAPI
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, TipoRolValueObject) and self.valor == other.valor
    
    def __str__(self):
        return self.valor
    
    def __hash__(self):
        return hash(self.valor)