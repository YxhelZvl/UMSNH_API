# src/app/features/catalogo/presentation/schemas/catalogo_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class CatalogoCreateRequest(BaseModel):
    tipo: str = Field(..., description="Tipo de item: herramienta, libro, equipo")
    nombre: str = Field(..., max_length=200, description="Nombre del item")
    autor: Optional[str] = Field(None, max_length=200, description="Autor del libro (solo para libros)")
    isbn: Optional[str] = Field(None, max_length=30, description="ISBN del libro (solo para libros)")
    descripcion: Optional[str] = Field(None, description="Descripción del item")

class CatalogoUpdateRequest(BaseModel):
    tipo: Optional[str] = Field(None, description="Tipo de item: herramienta, libro, equipo")
    nombre: Optional[str] = Field(None, max_length=200, description="Nombre del item")
    autor: Optional[str] = Field(None, max_length=200, description="Autor del libro (solo para libros)")
    isbn: Optional[str] = Field(None, max_length=30, description="ISBN del libro (solo para libros)")
    descripcion: Optional[str] = Field(None, description="Descripción del item")

# Response Schema
class CatalogoResponse(BaseModel):
    id_catalogo: int
    tipo: str
    nombre: str
    autor: Optional[str] = None
    isbn: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

# Generic Responses
CatalogosListResponse = GenericResponse[List[CatalogoResponse]]
CatalogoSingleResponse = GenericResponse[CatalogoResponse]
CatalogoDeleteResponse = GenericResponse[None]