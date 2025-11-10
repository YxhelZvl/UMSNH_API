# src/app/features/catalogo/domain/value_objects/tipo_item.py
from pydantic import BaseModel, Field, field_validator, model_serializer
from enum import Enum

class TipoItemEnum(str, Enum):
    HERRAMIENTA = "herramienta"
    LIBRO = "libro"
    EQUIPO = "equipo"

class TipoItem(BaseModel):
    valor: TipoItemEnum = Field(..., description="Tipo de item del catálogo")
    
    @field_validator("valor", mode="before")
    def validar_tipo(cls, v):
        if isinstance(v, str):
            v = v.lower()
            if v not in ["herramienta", "libro", "equipo"]:
                raise ValueError("El tipo debe ser 'herramienta', 'libro' o 'equipo'")
            return TipoItemEnum(v)
        return v
    
    @model_serializer(when_used='json')
    def serialize_tipo(self) -> str:
        return self.valor.value
    
    def __eq__(self, other):
        return isinstance(other, TipoItem) and self.valor == other.valor
    
    def __str__(self):
        return self.valor.value
    
    def es_libro(self) -> bool:
        return self.valor == TipoItemEnum.LIBRO
    
    def es_herramienta(self) -> bool:
        return self.valor == TipoItemEnum.HERRAMIENTA
    
    def es_equipo(self) -> bool:
        return self.valor == TipoItemEnum.EQUIPO