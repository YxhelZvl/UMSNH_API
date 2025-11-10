# src/app/features/prestamos/domain/value_objects/fechas_prestamo.py
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, date
from typing import Optional

class FechasPrestamo(BaseModel):
    fecha_prestamo: datetime = Field(default_factory=datetime.now, description="Fecha y hora del préstamo")
    fecha_devolucion_esperada: date = Field(..., description="Fecha esperada de devolución")
    fecha_devolucion_real: Optional[datetime] = Field(None, description="Fecha real de devolución")

    @field_validator("fecha_devolucion_esperada", mode="before")
    def validar_fecha_devolucion_esperada(cls, v):
        if isinstance(v, str):
            v = date.fromisoformat(v)
        if v < date.today():
            raise ValueError("La fecha de devolución esperada no puede ser en el pasado")
        return v

    @model_validator(mode='after')
    def validar_fechas(self):
        if self.fecha_devolucion_real and self.fecha_devolucion_real < self.fecha_prestamo:
            raise ValueError("La fecha de devolución real no puede ser anterior a la fecha de préstamo")
        return self

    def calcular_dias_retraso(self) -> int:
        if self.fecha_devolucion_real:
            # Si ya se devolvió, calcular retraso al momento de la devolución
            if self.fecha_devolucion_real.date() > self.fecha_devolucion_esperada:
                return (self.fecha_devolucion_real.date() - self.fecha_devolucion_esperada).days
            return 0
        else:
            # Si no se ha devuelto, calcular retraso hasta hoy
            if date.today() > self.fecha_devolucion_esperada:
                return (date.today() - self.fecha_devolucion_esperada).days
            return 0

    def esta_vencido(self) -> bool:
        return self.calcular_dias_retraso() > 0

    def se_puede_renovar(self) -> bool:
        # Se puede renovar si no está vencido y no se ha devuelto
        return not self.esta_vencido() and not self.fecha_devolucion_real