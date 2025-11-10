# src/app/features/laboratorios/presentation/schemas/laboratorio_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class LaboratorioCreateRequest(BaseModel):
    nombre: str = Field(..., max_length=150, description="Nombre del laboratorio")
    ubicacion: str = Field(..., max_length=250, description="Ubicación del laboratorio")
    responsable_id: Optional[int] = Field(None, description="ID del usuario responsable")

class LaboratorioUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150, description="Nombre del laboratorio")
    ubicacion: Optional[str] = Field(None, max_length=250, description="Ubicación del laboratorio")
    responsable_id: Optional[int] = Field(None, description="ID del usuario responsable (0 para remover)")

# Response Schema básico
class LaboratorioResponse(BaseModel):
    id_laboratorio: int
    nombre: str
    ubicacion: str
    responsable_id: Optional[int]

    class Config:
        from_attributes = True

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

class LaboratorioDetailResponse(BaseModel):
    """Schema detallado con información completa del laboratorio"""
    id_laboratorio: int
    nombre: str
    ubicacion: str
    responsable: Optional[UsuarioBasicResponse] = None

    class Config:
        from_attributes = True

# Generic Responses
LaboratoriosListResponse = GenericResponse[List[LaboratorioResponse]]
LaboratorioSingleResponse = GenericResponse[LaboratorioResponse]
LaboratorioDeleteResponse = GenericResponse[None]

# Generic Responses para datos detallados
LaboratorioDetailSingleResponse = GenericResponse[LaboratorioDetailResponse]
LaboratoriosDetailListResponse = GenericResponse[List[LaboratorioDetailResponse]]