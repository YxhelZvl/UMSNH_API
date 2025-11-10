# src/app/features/user/domain/value_objects/nombre_usuario.py
from pydantic import BaseModel, Field, field_validator, model_serializer

class NombreUsuario(BaseModel):
    valor: str = Field(..., description="Nombre del Usuario")
    
    @field_validator("valor")
    def validator_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        if len(v) < 3:  # Cambié de 5 a 3 para coincidir con tu BD (varchar(40))
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        
        if len(v) > 40:  # Para coincidir con tu BD
            raise ValueError("El nombre no puede exceder 40 caracteres")
            
        return v.strip().title()  # Normalización
        
    @model_serializer(when_used='json')
    def serialize_nombre(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, NombreUsuario) and self.valor == other.valor
    
    def __str__(self):
        return self.valor