# src/app/features/bibliotecas/presentation/schemas/biblioteca_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class BibliotecaCreateRequest(BaseModel):
    nombre: str = Field(..., max_length=150, description="Nombre de la biblioteca")
    ubicacion: str = Field(..., max_length=250, description="Ubicación de la biblioteca")

class BibliotecaUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150, description="Nombre de la biblioteca")
    ubicacion: Optional[str] = Field(None, max_length=250, description="Ubicación de la biblioteca")

# Response Schema
class BibliotecaResponse(BaseModel):
    id_biblioteca: int
    nombre: str
    ubicacion: str

    class Config:
        from_attributes = True

# Generic Responses
BibliotecasListResponse = GenericResponse[List[BibliotecaResponse]]
BibliotecaSingleResponse = GenericResponse[BibliotecaResponse]
BibliotecaDeleteResponse = GenericResponse[None]