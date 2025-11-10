# src/app/features/user/domain/value_objects/matricula.py
from pydantic import BaseModel, field_validator, model_serializer

class MatriculaValueObject(BaseModel):
    valor: str
    
    @field_validator("valor")
    def validar_matricula(cls, v):
        if not v or not v.strip():
            raise ValueError("La matrícula no puede estar vacía")
        if len(v) > 15:
            raise ValueError("La matrícula no puede exceder 15 caracteres")
        return v.strip()
    
    @model_serializer(when_used='json')
    def serialize_matricula(self) -> str:
        return self.valor
    
    def __eq__(self, other):
        return isinstance(other, MatriculaValueObject) and self.valor == other.valor
    
    def __str__(self):
        return self.valor