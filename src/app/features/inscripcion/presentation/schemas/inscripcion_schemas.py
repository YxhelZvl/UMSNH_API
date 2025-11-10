# src/app/features/inscripcion/presentation/schemas/inscripcion_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from src.app.shared.schemas.generic_response import GenericResponse
from src.app.features.inscripcion.domain.value_objects.estado_inscripcion import EstadoInscripcionEnum

class InscripcionCreateRequest(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario")
    id_ciclo: int = Field(..., description="ID del ciclo")
    fecha_inscripcion: date = Field(..., description="Fecha de inscripción")
    estado: EstadoInscripcionEnum = Field(..., description="Estado de la inscripción")

class InscripcionUpdateRequest(BaseModel):
    estado: Optional[EstadoInscripcionEnum] = Field(None, description="Estado de la inscripción")

class InscripcionResponse(BaseModel):
    id_inscripcion: int
    id_usuario: int
    id_ciclo: int
    fecha_inscripcion: date
    estado: str

    class Config:
        from_attributes = True

InscripcionesListResponse = GenericResponse[List[InscripcionResponse]]
InscripcionSingleResponse = GenericResponse[InscripcionResponse]
InscripcionDeleteResponse = GenericResponse[None]