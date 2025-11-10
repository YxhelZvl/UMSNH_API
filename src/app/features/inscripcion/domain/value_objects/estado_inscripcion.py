# src/app/features/inscripcion/domain/value_objects/estado_inscripcion.py
from pydantic import BaseModel, field_validator, model_serializer
from enum import Enum

class EstadoInscripcionEnum(str, Enum):
    ACTIVA = 'activa'
    EN_PROCESO = 'en_proceso'
    FINALIZADA = 'finalizada'

class EstadoInscripcionValueObject(BaseModel):
    valor: EstadoInscripcionEnum

    @field_validator("valor")
    def validar_estado_inscripcion(cls, v):
        return v

    @model_serializer(when_used='json')
    def serialize_estado_inscripcion(self) -> str:
        return self.valor.value

    def __eq__(self, other):
        return isinstance(other, EstadoInscripcionValueObject) and self.valor == other.valor

    def __str__(self):
        return self.valor.value