# src/app/features/user/domain/value_objects/email.py
from pydantic import BaseModel, field_validator, model_serializer
import re

class EmailValueObject(BaseModel):
    valor: str
    
    @field_validator("valor")
    def validar_email(cls, v):
        if not v or not v.strip():
            raise ValueError("El email no puede estar vacío")
        
        # Validación básica de formato email
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, v):
            raise ValueError("El formato del email no es válido")
            
        return v.strip().lower()
    
    @model_serializer(when_used='json')
    def serialize_email(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, EmailValueObject) and self.valor == other.valor
    
    def __str__(self):
        return self.valor