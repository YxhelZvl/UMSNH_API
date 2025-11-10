# src/app/features/catalogo/domain/value_objects/isbn.py
from pydantic import BaseModel, Field, field_validator, model_serializer
import re

class ISBN(BaseModel):
    valor: str = Field(..., description="ISBN del libro")
    
    @field_validator("valor")
    def validar_isbn(cls, v):
        if not v or not v.strip():
            return None
            
        v = v.strip()
        # Si el valor es "string" (valor por defecto de ejemplo), tratarlo como vacío
        if v.lower() == "string":
            return None
            
        # Validar formato ISBN (10 o 13 dígitos)
        pattern = r'^(?:\d{9}[\dXx]|\d{13})$'
        if not re.match(pattern, v):
            raise ValueError("El formato del ISBN no es válido (debe ser 10 o 13 dígitos)")
        return v
    
    @model_serializer(when_used='json')
    def serialize_isbn(self) -> str:
        return self.valor if self.valor else None
    
    def __eq__(self, other):
        return isinstance(other, ISBN) and self.valor == other.valor
    
    def __str__(self):
        return self.valor if self.valor else ""
    
    def es_valido(self) -> bool:
        """Método para verificar si el ISBN es válido (no None y no vacío)"""
        return bool(self.valor and self.valor.strip())