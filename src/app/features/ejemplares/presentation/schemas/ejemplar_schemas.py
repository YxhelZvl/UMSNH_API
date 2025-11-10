# src/app/features/ejemplares/presentation/schemas/ejemplar_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class EjemplarCreateRequest(BaseModel):
    id_catalogo: int = Field(..., description="ID del catálogo al que pertenece el ejemplar")
    codigo_inventario: str = Field(..., max_length=50, description="Código único de inventario del ejemplar")
    ubicacion: str = Field(..., description="Ubicación del ejemplar: laboratorio o biblioteca")
    id_laboratorio: Optional[int] = Field(None, description="ID del laboratorio si la ubicación es laboratorio")
    id_biblioteca: Optional[int] = Field(None, description="ID de la biblioteca si la ubicación es biblioteca")
    estado: str = Field(default="disponible", description="Estado del ejemplar")

class EjemplarUpdateRequest(BaseModel):
    id_catalogo: Optional[int] = Field(None, description="ID del catálogo al que pertenece el ejemplar")
    codigo_inventario: Optional[str] = Field(None, max_length=50, description="Código único de inventario del ejemplar")
    ubicacion: Optional[str] = Field(None, description="Ubicación del ejemplar: laboratorio o biblioteca")
    id_laboratorio: Optional[int] = Field(None, description="ID del laboratorio si la ubicación es laboratorio")
    id_biblioteca: Optional[int] = Field(None, description="ID de la biblioteca si la ubicación es biblioteca")
    estado: Optional[str] = Field(None, description="Estado del ejemplar")

# Response Schema básico
class EjemplarResponse(BaseModel):
    id_ejemplar: int
    id_catalogo: int
    codigo_inventario: str
    ubicacion: str
    id_laboratorio: Optional[int] = None
    id_biblioteca: Optional[int] = None
    estado: str

    class Config:
        from_attributes = True

# Schemas para datos detallados
class CatalogoBasicResponse(BaseModel):
    id_catalogo: int
    tipo: str
    nombre: str
    autor: Optional[str] = None
    isbn: Optional[str] = None
    descripcion: Optional[str] = None

class BibliotecaBasicResponse(BaseModel):
    id_biblioteca: int
    nombre: str
    ubicacion: str

class LaboratorioBasicResponse(BaseModel):
    id_laboratorio: int
    nombre: str
    ubicacion: str
    responsable_id: Optional[int] = None

class EjemplarDetailResponse(BaseModel):
    id_ejemplar: int
    catalogo: CatalogoBasicResponse
    codigo_inventario: str
    ubicacion: str
    biblioteca: Optional[BibliotecaBasicResponse] = None
    laboratorio: Optional[LaboratorioBasicResponse] = None
    estado: str

    class Config:
        from_attributes = True

# Generic Responses
EjemplaresListResponse = GenericResponse[List[EjemplarResponse]]
EjemplarSingleResponse = GenericResponse[EjemplarResponse]
EjemplarDeleteResponse = GenericResponse[None]

# Generic Responses para datos detallados
EjemplarDetailSingleResponse = GenericResponse[EjemplarDetailResponse]
EjemplaresDetailListResponse = GenericResponse[List[EjemplarDetailResponse]]
EjemplaresDisponiblesListResponse = GenericResponse[List[EjemplarDetailResponse]]