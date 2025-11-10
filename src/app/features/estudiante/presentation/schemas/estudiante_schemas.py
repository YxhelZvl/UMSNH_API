# src/app/features/estudiante/presentation/schemas/estudiante_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

class EstudianteCreateRequest(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario")
    id_carrera: int = Field(..., description="ID de la carrera")

class EstudianteUpdateRequest(BaseModel):
    id_carrera: Optional[int] = Field(None, description="ID de la carrera")

class EstudianteResponse(BaseModel):
    id_estudiante: int
    id_usuario: int
    id_carrera: int
    
# Schemas para datos detallados
class UsuarioBasicResponse(BaseModel):
    """Schema básico de usuario para respuestas detalladas"""
    id_usuario: int
    nombre: str
    apellidoP: str
    apellidoM: str
    matricula: str
    email: str
    id_rol: int
    status: str

class CarreraBasicResponse(BaseModel):
    """Schema básico de carrera para respuestas detalladas"""
    id_carrera: int
    carrera: str
    facultad: str

class EstudianteDetailResponse(BaseModel):
    """Schema detallado con información completa del estudiante"""
    id_estudiante: int
    usuario: UsuarioBasicResponse
    carrera: CarreraBasicResponse


    class Config:
        from_attributes = True

EstudiantesListResponse = GenericResponse[List[EstudianteResponse]]
EstudianteSingleResponse = GenericResponse[EstudianteResponse]
EstudianteDetailSingleResponse = GenericResponse[EstudianteDetailResponse]
EstudiantesDetailListResponse = GenericResponse[List[EstudianteDetailResponse]]
EstudianteDeleteResponse = GenericResponse[None]