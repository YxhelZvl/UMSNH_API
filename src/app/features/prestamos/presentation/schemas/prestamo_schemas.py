# src/app/features/prestamos/presentation/schemas/prestamo_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class PrestamoCreateRequest(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario que realiza el préstamo")
    id_ejemplar: int = Field(..., description="ID del ejemplar a prestar")
    fecha_devolucion_esperada: date = Field(..., description="Fecha esperada para la devolución")
    estado: str = Field(default="activo", description="Estado del préstamo")

class PrestamoUpdateRequest(BaseModel):
    id_usuario: Optional[int] = Field(None, description="ID del usuario que realiza el préstamo")
    id_ejemplar: Optional[int] = Field(None, description="ID del ejemplar a prestar")
    fecha_devolucion_esperada: Optional[date] = Field(None, description="Fecha esperada para la devolución")
    estado: Optional[str] = Field(None, description="Estado del préstamo")

class PrestamoDevolverRequest(BaseModel):
    fecha_devolucion_real: Optional[date] = Field(None, description="Fecha real de devolución (opcional)")

class PrestamoRenovarRequest(BaseModel):
    nueva_fecha_devolucion: date = Field(..., description="Nueva fecha de devolución para la renovación")

# Response Schema básico
class PrestamoResponse(BaseModel):
    id_prestamo: int
    id_usuario: int
    id_ejemplar: int
    fecha_prestamo: datetime
    fecha_devolucion_esperada: date
    fecha_devolucion_real: Optional[datetime] = None
    estado: str

    class Config:
        from_attributes = True

# Schemas para datos detallados
class UsuarioBasicResponse(BaseModel):
    id_usuario: int
    nombre: str
    apellidoP: str
    apellidoM: str
    matricula: str
    email: str

class EjemplarBasicResponse(BaseModel):
    id_ejemplar: int
    codigo_inventario: str
    ubicacion: str
    estado: str

class CatalogoBasicResponse(BaseModel):
    id_catalogo: int
    tipo: str
    nombre: str
    autor: Optional[str] = None
    isbn: Optional[str] = None

class PrestamoDetailResponse(BaseModel):
    id_prestamo: int
    usuario: UsuarioBasicResponse
    ejemplar: EjemplarBasicResponse
    catalogo: CatalogoBasicResponse
    fecha_prestamo: datetime
    fecha_devolucion_esperada: date
    fecha_devolucion_real: Optional[datetime] = None
    estado: str
    dias_retraso: Optional[int] = None

    class Config:
        from_attributes = True

# Generic Responses
PrestamosListResponse = GenericResponse[List[PrestamoResponse]]
PrestamoSingleResponse = GenericResponse[PrestamoResponse]
PrestamoDeleteResponse = GenericResponse[None]

# Generic Responses para datos detallados
PrestamoDetailSingleResponse = GenericResponse[PrestamoDetailResponse]
PrestamosDetailListResponse = GenericResponse[List[PrestamoDetailResponse]]