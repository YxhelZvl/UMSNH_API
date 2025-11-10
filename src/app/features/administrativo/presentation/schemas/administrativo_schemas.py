# src/app/features/administrativo/presentation/schemas/administrativo_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class AdministrativoCreateRequest(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario")
    departamento: str = Field(..., max_length=100, description="Departamento del administrativo")

class AdministrativoUpdateRequest(BaseModel):
    departamento: Optional[str] = Field(None, max_length=100, description="Departamento del administrativo")

# Response Schema básico
class AdministrativoResponse(BaseModel):
    id_administrativo: int
    id_usuario: int
    departamento: str

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

class AdministrativoDetailResponse(BaseModel):
    """Schema detallado con información completa del administrativo"""
    id_administrativo: int
    usuario: UsuarioBasicResponse
    departamento: str

    class Config:
        from_attributes = True

# Generic Responses
AdministrativosListResponse = GenericResponse[List[AdministrativoResponse]]
AdministrativoSingleResponse = GenericResponse[AdministrativoResponse]
AdministrativoDeleteResponse = GenericResponse[None]

# Generic Responses para datos detallados
AdministrativoDetailSingleResponse = GenericResponse[AdministrativoDetailResponse]
AdministrativosDetailListResponse = GenericResponse[List[AdministrativoDetailResponse]]