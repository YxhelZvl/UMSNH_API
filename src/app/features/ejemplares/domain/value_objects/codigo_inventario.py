# src/app/features/ejemplares/domain/value_objects/codigo_inventario.py
from pydantic import BaseModel, Field, field_validator, model_serializer
import re

class CodigoInventario(BaseModel):
    valor: str = Field(..., description="Código único de inventario del ejemplar")
    
    @field_validator("valor")
    def validar_codigo_inventario(cls, v):
        if not v.strip():
            raise ValueError("El código de inventario no puede estar vacío")
        
        if len(v) < 3:
            raise ValueError("El código de inventario debe tener al menos 3 caracteres")
        
        if len(v) > 50:
            raise ValueError("El código de inventario no puede exceder 50 caracteres")
            
        return v.strip().upper()
    
    @model_serializer(when_used='json')
    def serialize_codigo(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, CodigoInventario) and self.valor == other.valor
    
    def __str__(self):
        return self.valor