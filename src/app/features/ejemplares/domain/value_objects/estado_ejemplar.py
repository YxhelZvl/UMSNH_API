# src/app/features/ejemplares/domain/value_objects/estado_ejemplar.py
from pydantic import BaseModel, Field, field_validator, model_serializer
from enum import Enum

class EstadoEjemplarEnum(str, Enum):
    NO_DISPONIBLE = "no_disponible"
    DISPONIBLE = "disponible"
    PRESTADO = "prestado"
    MANTENIMIENTO = "mantenimiento"
    PERDIDO = "perdido"

class EstadoEjemplar(BaseModel):
    valor: EstadoEjemplarEnum = Field(default=EstadoEjemplarEnum.DISPONIBLE, description="Estado del ejemplar")
    
    @field_validator("valor", mode="before")
    def validar_estado(cls, v):
        if isinstance(v, str):
            v = v.lower()
            if v not in ["no_disponible", "disponible", "prestado", "mantenimiento", "perdido"]:
                raise ValueError("El estado debe ser: no_disponible, disponible, prestado, mantenimiento o perdido")
            return EstadoEjemplarEnum(v)
        return v
    
    @model_serializer(when_used='json')
    def serialize_estado(self) -> str:
        return self.valor.value
    
    def __eq__(self, other):
        return isinstance(other, EstadoEjemplar) and self.valor == other.valor
    
    def __str__(self):
        return self.valor.value
    
    def esta_disponible(self) -> bool:
        return self.valor == EstadoEjemplarEnum.DISPONIBLE
    
    def puede_prestarse(self) -> bool:
        return self.valor in [EstadoEjemplarEnum.DISPONIBLE]