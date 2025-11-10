# src/app/features/prestamos/domain/value_objects/estado_prestamo.py
from pydantic import BaseModel, Field, field_validator, model_serializer
from enum import Enum

class EstadoPrestamoEnum(str, Enum):
    ACTIVO = "activo"
    COMPLETADO = "completado"
    RETRASADO = "retrasado"

class EstadoPrestamo(BaseModel):
    valor: EstadoPrestamoEnum = Field(default=EstadoPrestamoEnum.ACTIVO, description="Estado del préstamo")

    @field_validator("valor", mode="before")
    def validar_estado(cls, v):
        if isinstance(v, str):
            v = v.lower()
            if v not in ["activo", "completado", "retrasado"]:
                raise ValueError("El estado debe ser: activo, completado o retrasado")
            return EstadoPrestamoEnum(v)
        return v

    @model_serializer(when_used='json')
    def serialize_estado(self) -> str:
        return self.valor.value

    def __eq__(self, other):
        return isinstance(other, EstadoPrestamo) and self.valor == other.valor

    def __str__(self):
        return self.valor.value

    def esta_activo(self) -> bool:
        return self.valor == EstadoPrestamoEnum.ACTIVO

    def esta_completado(self) -> bool:
        return self.valor == EstadoPrestamoEnum.COMPLETADO

    def esta_retrasado(self) -> bool:
        return self.valor == EstadoPrestamoEnum.RETRASADO