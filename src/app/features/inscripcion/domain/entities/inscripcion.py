# src/app/features/inscripcion/domain/entities/inscripcion.py
from pydantic import BaseModel
from typing import Optional
from datetime import date
from src.app.features.inscripcion.domain.value_objects.estado_inscripcion import EstadoInscripcionValueObject, EstadoInscripcionEnum

class Inscripcion(BaseModel):
    id_inscripcion: Optional[int] = None
    id_usuario: int
    id_ciclo: int
    fecha_inscripcion: date
    estado: EstadoInscripcionValueObject

    def cambiar_estado(self, nuevo_estado: EstadoInscripcionEnum):
        """Método de negocio para cambiar el estado de la inscripción"""
        self.estado = EstadoInscripcionValueObject(valor=nuevo_estado)

    def es_activa(self) -> bool:
        """Método de negocio: verificar si la inscripción está activa"""
        return self.estado.valor == EstadoInscripcionEnum.ACTIVA

    def puede_ser_modificada(self) -> bool:
        """Método de negocio: verificar si la inscripción puede ser modificada"""
        return self.estado.valor in [EstadoInscripcionEnum.ACTIVA, EstadoInscripcionEnum.EN_PROCESO]

    class Config:
        arbitrary_types_allowed = True