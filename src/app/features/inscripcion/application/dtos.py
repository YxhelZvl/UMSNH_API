# src/app/features/inscripcion/application/dtos.py
from pydantic import BaseModel
from typing import Optional
from datetime import date
from src.app.features.inscripcion.domain.value_objects.estado_inscripcion import EstadoInscripcionEnum

class CreateInscripcionDTO(BaseModel):
    id_usuario: int
    id_ciclo: int
    fecha_inscripcion: date
    estado: EstadoInscripcionEnum

class UpdateInscripcionDTO(BaseModel):
    estado: Optional[EstadoInscripcionEnum] = None