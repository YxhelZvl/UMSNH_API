# src/app/features/rol/presentation/schemas/rol_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class RolCreateRequest(BaseModel):
    """Schema para crear un rol (input del API)"""
    tipo_rol: str = Field(
        ..., 
        min_length=3, 
        max_length=30,
        description="Tipo de rol: Estudiante, Maestro, Administrativo, Bibliotecario"
    )

class RolUpdateRequest(BaseModel):
    """Schema para actualizar un rol (input del API)"""
    tipo_rol: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=30,
        description="Tipo de rol: Estudiante, Maestro, Administrativo, Bibliotecario"
    )

# Response Schema
class RolResponse(BaseModel):
    """Schema para respuesta de rol (output del API)"""
    id_rol: int
    tipo_rol: str

    class Config:
        from_attributes = True

# Generic Responses
RolesListResponse = GenericResponse[List[RolResponse]]
RolSingleResponse = GenericResponse[RolResponse]
RolDeleteResponse = GenericResponse[None]