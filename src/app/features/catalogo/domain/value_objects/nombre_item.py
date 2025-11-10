# src/app/features/catalogo/domain/value_objects/nombre_item.py
from pydantic import BaseModel, Field, field_validator, model_serializer

class NombreItem(BaseModel):
    valor: str = Field(..., description="Nombre del Item del Catálogo")
    
    @field_validator("valor")
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre del item no puede estar vacío")
        
        if len(v) < 2:
            raise ValueError("El nombre del item debe tener al menos 2 caracteres")
        
        if len(v) > 200:  # Para coincidir con tu BD
            raise ValueError("El nombre del item no puede exceder 200 caracteres")
            
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_nombre(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, NombreItem) and self.valor == other.valor
    
    def __str__(self):
        return self.valor