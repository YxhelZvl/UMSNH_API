# src/app/features/maestros/presentation/schemas/maestro_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class MaestroCreateRequest(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario")

class MaestroUpdateRequest(BaseModel):
    # No hay campos para actualizar en esta versión simple
    pass

# Response Schema básico
class MaestroResponse(BaseModel):
    id_maestro: int
    id_usuario: int

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

class MaestroDetailResponse(BaseModel):
    """Schema detallado con información completa del maestro"""
    id_maestro: int
    usuario: UsuarioBasicResponse

    class Config:
        from_attributes = True

# Generic Responses
MaestrosListResponse = GenericResponse[List[MaestroResponse]]
MaestroSingleResponse = GenericResponse[MaestroResponse]
MaestroDeleteResponse = GenericResponse[None]

# Generic Responses para datos detallados
MaestroDetailSingleResponse = GenericResponse[MaestroDetailResponse]
MaestrosDetailListResponse = GenericResponse[List[MaestroDetailResponse]]