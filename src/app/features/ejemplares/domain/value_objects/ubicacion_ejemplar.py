# src/app/features/ejemplares/domain/value_objects/ubicacion_ejemplar.py
from pydantic import BaseModel, Field, field_validator, model_serializer
from enum import Enum

class TipoUbicacionEnum(str, Enum):
    LABORATORIO = "laboratorio"
    BIBLIOTECA = "biblioteca"

class UbicacionEjemplar(BaseModel):
    valor: TipoUbicacionEnum = Field(..., description="Tipo de ubicación del ejemplar")
    
    @field_validator("valor", mode="before")
    def validar_ubicacion(cls, v):
        if isinstance(v, str):
            v = v.lower()
            if v not in ["laboratorio", "biblioteca"]:
                raise ValueError("La ubicación debe ser 'laboratorio' o 'biblioteca'")
            return TipoUbicacionEnum(v)
        return v
    
    @model_serializer(when_used='json')
    def serialize_ubicacion(self) -> str:
        return self.valor.value
    
    def __eq__(self, other):
        return isinstance(other, UbicacionEjemplar) and self.valor == other.valor
    
    def __str__(self):
        return self.valor.value
    
    def es_laboratorio(self) -> bool:
        return self.valor == TipoUbicacionEnum.LABORATORIO
    
    def es_biblioteca(self) -> bool:
        return self.valor == TipoUbicacionEnum.BIBLIOTECA